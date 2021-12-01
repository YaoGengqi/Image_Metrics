# Evaluation Toolbox

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

##### 2. Go to the Python API folder

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


### Evaluation

#### a. Manual

edit yourself configuration

- edit the datasets.
- edit the SRROOT and GTROOT in the main.py.
- edit the log name.

Run `main.py`

### Results

The results will be generated in the `../Result/` folder as a log file and a excel file in your SRROOT/datasets.

## Reference

The code is based on [MA](https://github.com/chaoma99/sr-metric), [NIQE](https://github.com/csjunxu/Bovik_NIQE_SPL2013), [PI](https://github.com/roimehrez/PIRM2018), [SSIM](https://ece.uwaterloo.ca/~z70wang/research/ssim) and [LPIPS](https://github.com/richzhang/PerceptualSimilarity). 
