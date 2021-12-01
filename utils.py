import os
import logging
import pandas as pd
from PIL import Image
import LPIPS as models
import matlab.engine
import torch
from logging import handlers
import numpy as np

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

def CalMATLAB(SRFolder, GTFolder):
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath(eng.fullfile(os.getcwd(), 'MetricEvaluation')))
    res = eng.evaluate_results(SRFolder, GTFolder)
    res = np.array(res)
    res = res.squeeze()
    return res

def CheckImage(image):
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]
        image = np.concatenate((image, image, image), axis=2)
    return image

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

        if not i.endswith(('.png', '.PNG')):
            continue

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

