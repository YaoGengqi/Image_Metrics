import os
import logging
import pandas as pd
import pathlib
from PIL import Image
import LPIPS as models
import matlab.engine
import torch
from logging import handlers
import numpy as np


from FID.fid_score import *
from FID.inception import *


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

def CheckImage(image):
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
        image = np.concatenate((image, image, image), axis=2)
    return image

class ImagePathDataset(torch.utils.data.Dataset):
    def __init__(self, files, transforms=None):
        self.files = files
        self.transforms = transforms

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        path = self.files[i]
        img = Image.open(path).convert('RGB')
        if self.transforms is not None:
            img = self.transforms(img)
        return img

def calculate_activation_statistics(files, model, batch_size=50, dims=2048,
                                    device='cpu', num_workers=1):
    act = get_activations(files, model, batch_size, dims, device, num_workers)
    mu = np.mean(act, axis=0)
    sigma = np.cov(act, rowvar=False)
    return mu, sigma

def get_activations(files, model, batch_size=50, dims=2048, device='cpu',
                    num_workers=1):
    model.eval()

    if batch_size > len(files):
        print(('Warning: batch size is bigger than the data size. '
               'Setting batch size to data size'))
        batch_size = len(files)

    dataset = ImagePathDataset(files, transforms=TF.ToTensor())
    dataloader = torch.utils.data.DataLoader(dataset,
                                             batch_size=batch_size,
                                             shuffle=False,
                                             drop_last=False,
                                             num_workers=num_workers)

    pred_arr = np.empty((len(files), dims))

    start_idx = 0

    for batch in dataloader:
        batch = batch.to(device)

        with torch.no_grad():
            pred = model(batch)[0]

        # If model output is not scalar, apply global spatial average pooling.
        # This happens if you choose a dimensionality not equal 2048.
        if pred.size(2) != 1 or pred.size(3) != 1:
            pred = adaptive_avg_pool2d(pred, output_size=(1, 1))

        pred = pred.squeeze(3).squeeze(2).cpu().numpy()

        pred_arr[start_idx:start_idx + pred.shape[0]] = pred

        start_idx = start_idx + pred.shape[0]

    return pred_arr



def CalMATLAB(SRFolder, GTFolder):
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath(eng.fullfile(os.getcwd(), 'MetricEvaluation')))
    res = eng.evaluate_results(SRFolder, GTFolder)
    res = np.array(res)
    res = res.squeeze()
    return res

def CalMATLAB2(SRFolder, GTFolder):
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath(eng.fullfile(os.getcwd(), 'MetricEvaluation')))
    res = eng.evaluate_results2(SRFolder, GTFolder)
    res = np.array(res)
    res = res.squeeze()
    return res



def CalLPIPS(SRFolder, GTFolder):

    all = pd.read_excel(os.path.join(SRFolder, 'AllMetrics.xlsx'))

    # idx = GTFolder.split('/')[-1]
    # record = pd.DataFrame(columns=('ImgName','LPIPS'))

    nameList = os.listdir(GTFolder)
    res = []
    model = models.PerceptualLoss(model='net-lin', net='alex', use_gpu=False)
    j = 0
    sum = 0

    for i in nameList:
        imageA = os.path.join(SRFolder, i)
        imageB = os.path.join(GTFolder, i)

        imageA = CheckImage(np.array(Image.open(imageA)))
        imageB = CheckImage(np.array(Image.open(imageB)))

        imageA = torch.Tensor((imageA / 127.5 - 1)[:, :, :, np.newaxis].transpose((3, 2, 0, 1)))
        imageB = torch.Tensor((imageB / 127.5 - 1)[:, :, :, np.newaxis].transpose((3, 2, 0, 1)))

        dist = model.forward(imageA, imageB).detach().squeeze().numpy()

        res.append(dist)

        # record_data = dict()
        # record_data['ImgName'] = i
        # record_data['LPIPS'] = dist.item()
        # record_data = pd.DataFrame(record_data, index=[idx])
        # record = record.append(record_data)

        all.loc[j, 'LPIPS'] = dist.item()
        sum += dist.item()
        j = j + 1

    all.loc[j, 'LPIPS'] = sum / j
    res = np.array(res)
    res = res.squeeze()

    all.to_excel(os.path.join(SRFolder, 'AllMetrics.xlsx'), index=None)
    # record.to_excel(os.path.join(SRFolder, 'LPIPS.xlsx'), header=True, index=True)

    return np.mean(res)



def CalFID(SRFolder, GTFolder):

    all = pd.read_excel(os.path.join(SRFolder, 'AllMetrics.xlsx'))
    j = 0
    sum = 0

    device = torch.device('cuda' if (torch.cuda.is_available()) else 'cpu')
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[2048]
    model = InceptionV3([block_idx]).to(device)

    nameList = os.listdir(GTFolder)

    for i in nameList:
        imageA = os.path.join(SRFolder, i)
        imageB = os.path.join(GTFolder, i)

        m1, s1 = calculate_activation_statistics([imageA], model, 1, 2048, device, 1)
        m2, s2 = calculate_activation_statistics([imageB], model, 1, 2048, device, 1)
        fid_value = calculate_frechet_distance(m1, s1, m2, s2)

        all.loc[j, 'FID'] = fid_value
        sum += fid_value
        j = j + 1

    all.loc[j, 'FID'] = sum / j
    all.to_excel(os.path.join(SRFolder, 'AllMetrics.xlsx'), index=None)

    return sum/j