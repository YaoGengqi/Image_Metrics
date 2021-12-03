# Image-Metrics Evaluation Direction.

## Directions

This project is mainly used to test the reference or non-reference indicators of various images.

The indicators supported so far are as follows:

- PI
- Ma
- NIQE
- MSE
- RMSE
- PSNR
- SSIM
- LPIPS
- BIQME
- FADE
- AG
- IE
- VAR
- LPIPS
- FID



## Dependencies

- Python3
- MATLAB Engine API for Python



## Installation

### A. Install MATLAB Engine API for Python

#### a. Windows

##### 1. Find your MATLAB root

```bash
where matlab
```

For example:

```bash
C:\Program Files\MATLAB\R2019b\bin\matlab.exe
```

##### 2. Go to the Python API folder in Matlab root path.

```bash
cd matlabroot\extern\engines\python
```

For example:

```bash
cd C:\Program Files\MATLAB\R2019b\extern\engines\python
```

##### 3. Install MATLAB Engine API for Python

```bash
python setup.py install
```

#### b. Ubuntu

##### 1. Find your MATLAB root

```bash
sudo find / -name MATLAB
```

For example:

```bash
# default MATLAB root
/usr/local/MATLAB/R2016b
```

##### 2. Go to Python API folder

```bash
cd matlabroot/extern/engines/python
```

For example:

```bash
cd /usr/local/MATLAB/R2016b/extern/engines/python
```

##### 3. Install MATLAB Engine API for Python

```bash
python setup.py install
```

### B. Install Required Modules



## Evaluation 

#### a. Manual

Please edit your configuration in the main.py.

- To edit the datasets.
- To edit the SRROOT and GTROOT in the main.py.
- To edit the log Name.

Run `main.py`

### Results

The .log results will be generated in the [Result/Name.log](Results/20211203-Test.log).

The table of Metrics will be save as a excel file in the [SRROOT/Datasets/AllMetrics.xlsx](Test/SRROOT/Set5/AllMetrics.xlsx).

## Reference

The code is based on [MA](https://github.com/chaoma99/sr-metric), [NIQE](https://github.com/csjunxu/Bovik_NIQE_SPL2013), [PI](https://github.com/roimehrez/PIRM2018), [SSIM](https://ece.uwaterloo.ca/~z70wang/research/ssim), [LPIPS](https://github.com/richzhang/PerceptualSimilarity) and else, We will add these references in the future.

Some quotations are not yet indicated.
