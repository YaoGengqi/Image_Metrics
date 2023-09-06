# -*- coding: GBK -*-
# @Time    : 2021/11/28 13:51
# @Author  : GQ
# @FileName: main2.py
# @Software: PyCharm
# @Description: This file is used to calculate the metrics.
# python main2.py --log_name TTSR --GTRoot "F:\TT_SR\data\GT" --SRRoot "F:\TT_SR\data\exp01\RFDN"

# TODO: 为了节省计算指标时间，这里只计算超分比较相关的指标（NIQE等），因此修改了代码
# TODO: 只计算超分比较相关的指标：PSNR、SSIM、PI、NIQE、LPIPS
import shutil
import datetime
from evaluate_sr_results import *
import time

import argparse

parser = argparse.ArgumentParser(description="Initial the test setting.")

# the model would to be trained or tested.
# parser.add_argument("--log_name", type=str, default="TT_SR", help="保存的log文件名")
parser.add_argument("--log_name", type=str, default="TTSR0830-test", help="保存的log文件名")
# 需要GT文件夹和SR文件夹的图片同名才能对应，而且同名图片大小须相等
parser.add_argument("--GTRoot", type=str, default=r"D:\TT_SR\01data\Datasets2023\GTmod12", help="GT文件夹")
parser.add_argument("--SRRoot", type=str, default=r"D:\TT_SR\02exp\4090\230905\LBNet_x4_t1_SwinIR_t2_EdgeSRN_L1_0.1Lpts_Set14_psnr_28.505_ssim_0.779_epoch_92", help="SR文件夹")
# parser.add_argument("--GTRoot", type=str, default=r"F:\TT_SR\data\Datasets2023\GTmod12", help="GT文件夹")
# parser.add_argument("--SRRoot", type=str, default=r"F:\TT_SR\data\2023-07-28-10-19-v100\LBNet_x4_t1_SwinIR_t2_EdgeSRN_L1_0.1Lpts_Set14_psnr_28.409_ssim_0.777_epoch_783", help="SR文件夹")
# parser.add_argument("--checkpoint", type=str, default=None)

args = parser.parse_args()

# setting the arguments.
Metric = ['PI', 'Ma', 'NIQE', 'MSE', 'RMSE', 'PSNR', 'SSIM', 'LPIPS', 'BIQME', 'FADE', 'AG', 'IE', 'VAR', 'LPIPS', 'FID']

# Metric = ['PI', 'Ma', 'NIQE']

# TODO: 这里填充数据集名字，即你输入的 SRRoot 和 GTRoot 下应该有这一部分的子文件夹，如果没有，设为空列表
# Datasets = ['Vid4', 'REDS4']
# Datasets = ['Set14']
Datasets = ['Set5', 'Set14', 'BSD100', 'Urban100', 'Manga109']
# Datasets = ['Set5', 'Set14', 'BSD100', 'urban100', 'manga109']

# TODO: 这里需要输入你的备注，保存的log文件会以此命名。
Name = args.log_name

# TODO: 在这里输入你的数据集的参考图（原图）和结果图的路径，注意的是这里的路径下的应该还有datasets的文件夹
# TODO: 如果Root路径下没有数据集而是图片的话，可以将Datasets设为空list。
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