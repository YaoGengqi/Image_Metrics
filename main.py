# -*- coding: GBK -*-
# @Time    : 2021/11/28 13:51
# @Author  : GQ
# @FileName: main.py.py
# @Software: PyCharm
# @Description: This file is used to calculate the metrics.

import shutil
import datetime
from evaluate_sr_results import *

# setting the arguments.
Metric = ['PI', 'Ma', 'NIQE', 'MSE', 'RMSE', 'PSNR', 'SSIM', 'LPIPS', 'BIQME', 'FADE', 'AG', 'IE', 'VAR', 'LPIPS', 'FID']
Datasets = ['Set5']  # 'Set14', 'Urban100', 'Manga109', 'BSD100'

# TODO: ������Ҫ������ı�ע�������log�ļ����Դ�������
Name = 'Test'

# TODO: ����������������ݼ��Ĳο�ͼ��ԭͼ���ͽ��ͼ��·����ע����������·���µ�Ӧ�û���datasets���ļ���
# TODO: ���Root·����û�����ݼ�����ͼƬ�Ļ������Խ�Datasets��Ϊ��list��
GTRoot = r'Test/GTROOT'
SRRoot = r'Test/SRROOT'
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
        MATLAB = CalMATLAB(j, k)
        LPIPS = CalLPIPS(j, k)
        FID = CalFID(j, k)

        log.logger.info('[' + i + ']  PSNR  - ' + str(MATLAB[5]))
        log.logger.info('[' + i + ']  SSIM  - ' + str(MATLAB[6]))
        log.logger.info('[' + i + ']  LPIPS - ' + str(LPIPS))
        log.logger.info('[' + i + ']  PI    - ' + str(MATLAB[0]))
        log.logger.info('[' + i + ']  FID   - ' + str(FID))
        log.logger.info('[' + i + ']  BIQME - ' + str(MATLAB[7]))
        log.logger.info('[' + i + ']  FADE  - ' + str(MATLAB[8]))
        log.logger.info('[' + i + ']  AG    - ' + str(MATLAB[9]))
        log.logger.info('[' + i + ']  IE    - ' + str(MATLAB[10]))
        log.logger.info('[' + i + ']  VAR   - ' + str(MATLAB[11]))
        log.logger.info('[' + i + ']  Ma    - ' + str(MATLAB[1]))
        log.logger.info('[' + i + ']  NIQE  - ' + str(MATLAB[2]))
        log.logger.info('[' + i + ']  MSE   - ' + str(MATLAB[3]))
        log.logger.info('[' + i + ']  RMSE  - ' + str(MATLAB[4]))

    log.logger.info('Done.')

if __name__ == '__main__':
    main()