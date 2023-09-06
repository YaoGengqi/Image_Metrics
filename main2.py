# -*- coding: GBK -*-
# @Time    : 2021/11/28 13:51
# @Author  : GQ
# @FileName: main2.py
# @Software: PyCharm
# @Description: This file is used to calculate the metrics.
# python main2.py --log_name TTSR --GTRoot "F:\TT_SR\data\GT" --SRRoot "F:\TT_SR\data\exp01\RFDN"

# TODO: Ϊ�˽�ʡ����ָ��ʱ�䣬����ֻ���㳬�ֱȽ���ص�ָ�꣨NIQE�ȣ�������޸��˴���
# TODO: ֻ���㳬�ֱȽ���ص�ָ�꣺PSNR��SSIM��PI��NIQE��LPIPS
import shutil
import datetime
from evaluate_sr_results import *
import time

import argparse

parser = argparse.ArgumentParser(description="Initial the test setting.")

# the model would to be trained or tested.
# parser.add_argument("--log_name", type=str, default="TT_SR", help="�����log�ļ���")
parser.add_argument("--log_name", type=str, default="TTSR0830-test", help="�����log�ļ���")
# ��ҪGT�ļ��к�SR�ļ��е�ͼƬͬ�����ܶ�Ӧ������ͬ��ͼƬ��С�����
parser.add_argument("--GTRoot", type=str, default=r"D:\TT_SR\01data\Datasets2023\GTmod12", help="GT�ļ���")
parser.add_argument("--SRRoot", type=str, default=r"D:\TT_SR\02exp\4090\230905\LBNet_x4_t1_SwinIR_t2_EdgeSRN_L1_0.1Lpts_Set14_psnr_28.505_ssim_0.779_epoch_92", help="SR�ļ���")
# parser.add_argument("--GTRoot", type=str, default=r"F:\TT_SR\data\Datasets2023\GTmod12", help="GT�ļ���")
# parser.add_argument("--SRRoot", type=str, default=r"F:\TT_SR\data\2023-07-28-10-19-v100\LBNet_x4_t1_SwinIR_t2_EdgeSRN_L1_0.1Lpts_Set14_psnr_28.409_ssim_0.777_epoch_783", help="SR�ļ���")
# parser.add_argument("--checkpoint", type=str, default=None)

args = parser.parse_args()

# setting the arguments.
Metric = ['PI', 'Ma', 'NIQE', 'MSE', 'RMSE', 'PSNR', 'SSIM', 'LPIPS', 'BIQME', 'FADE', 'AG', 'IE', 'VAR', 'LPIPS', 'FID']

# Metric = ['PI', 'Ma', 'NIQE']

# TODO: ����������ݼ����֣���������� SRRoot �� GTRoot ��Ӧ������һ���ֵ����ļ��У����û�У���Ϊ���б�
# Datasets = ['Vid4', 'REDS4']
# Datasets = ['Set14']
Datasets = ['Set5', 'Set14', 'BSD100', 'Urban100', 'Manga109']
# Datasets = ['Set5', 'Set14', 'BSD100', 'urban100', 'manga109']

# TODO: ������Ҫ������ı�ע�������log�ļ����Դ�������
Name = args.log_name

# TODO: ����������������ݼ��Ĳο�ͼ��ԭͼ���ͽ��ͼ��·����ע����������·���µ�Ӧ�û���datasets���ļ���
# TODO: ���Root·����û�����ݼ�����ͼƬ�Ļ������Խ�Datasets��Ϊ��list��
GTRoot = args.GTRoot
SRRoot = args.SRRoot
GTFolder = []
SRFolder = []

if len(Datasets) > 0:
    for dataset in Datasets:
        GTFolder.append(GTRoot + '/' + dataset)
        SRFolder.append(SRRoot + '/' + dataset)
else:
    GTFolder.append(GTRoot)
    SRFolder.append(SRRoot)

output = datetime.datetime.now().strftime('%Y%m%d') + '-' + Name

if not os.path.isdir('./Results'):
    os.mkdir('./Results')


def main():

    log = Logger(os.path.join('./Results/', output + '.log'), level='info')
    log.logger.info('Init...')
    log.logger.info('Datasets - ' + str(Datasets))
    log.logger.info('GTFolder - ' + str(GTFolder))
    log.logger.info('SRFolder - ' + str(SRFolder))
    log.logger.info('Metric   - ' + str(Metric))
    log.logger.info('Name     - ' + Name)

    res = pd.DataFrame( columns=('PI',  'Ma',   'NIQE',  'MSE',  'RMSE',
                                 'PSNR','SSIM', 'LPIPS', 'BIQME','FADE',
                                 'AG',  'IE',   'VAR',   'LPIPS','FID'
                                 ))

    for i, j, k in zip(Datasets, SRFolder, GTFolder):
        # create the xlsx table.
        shutil.copy('demo.xlsx', j + r'\AllMetrics.xlsx')
        log.logger.info('The metrics will save in the file: ' + j + '\\AllMetrics.xlsx')
        log.logger.info('Calculating ' + i + '...')

        # cal the metrics.
        MATLAB = CalMATLAB2(j, k)
        LPIPS = CalLPIPS(j, k)
        # FID = CalFID(j, k)

        log.logger.info('[' + i + ']  PSNR  - ' + str(MATLAB[5]))
        log.logger.info('[' + i + ']  SSIM  - ' + str(MATLAB[6]))
        log.logger.info('[' + i + ']  LPIPS - ' + str(LPIPS))
        log.logger.info('[' + i + ']  PI    - ' + str(MATLAB[0]))
        # log.logger.info('[' + i + ']  FID   - ' + str(FID))
        # log.logger.info('[' + i + ']  BIQME - ' + str(MATLAB[7]))
        # log.logger.info('[' + i + ']  FADE  - ' + str(MATLAB[8]))
        # log.logger.info('[' + i + ']  AG    - ' + str(MATLAB[9]))
        # log.logger.info('[' + i + ']  IE    - ' + str(MATLAB[10]))
        # log.logger.info('[' + i + ']  VAR   - ' + str(MATLAB[11]))
        log.logger.info('[' + i + ']  Ma    - ' + str(MATLAB[1]))
        log.logger.info('[' + i + ']  NIQE  - ' + str(MATLAB[2]))
        # log.logger.info('[' + i + ']  MSE   - ' + str(MATLAB[3]))
        # log.logger.info('[' + i + ']  RMSE  - ' + str(MATLAB[4]))

    log.logger.info('Done.')

if __name__ == '__main__':
    start_time = time.time()
    main()
    work_time = time.time()-start_time
    m, s = divmod(work_time, 60)
    print("Calculate time: {} min {} second".format(m,s))

    log = Logger(os.path.join('./Results/', output + '.log'), level='info')
    log.logger.info("Calculate time: {} min {} second".format(m,s))