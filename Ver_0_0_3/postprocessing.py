import time
import pycuda.gpuarray as gpuarray
import numpy as np
import skcuda.cublas as cublas

def postprocessing(info):

    #Daylight matmul
    daylight_matmul(info)

    #Energy matmul

    pass


def read_binary_matrix(path):
    with open(path, 'rb') as reader:


        #Reading header
        for binary_line in reader:
            line = binary_line.decode()
            if "NROWS" in line:
                nrows = int(line.split("=")[-1])
            elif "NCOLS" in line:
                ncols = int(line.split("=")[-1])
            elif "NCOMP" in line:
                ncomp = int(line.split("=")[-1])
            elif "FORMAT" in line:
                break

        #Reading data
        #https://stackoverflow.com/questions/11760095/convert-binary-string-to-numpy-array
        data = np.fromfile(reader, dtype=np.dtype('>f4')).reshape(nrows, ncols, ncomp)
        #data = np.fromfile(reader, dtype=np.float32).reshape(nrows, ncols, ncomp)

    return data


def read_text_dc_matrix(path):
    with open(path, 'r') as infile:
        #Reading header
        count = 0
        for line in infile:

            if "NROWS" in line:
                nrows = int(line.split("=")[-1])
            elif "NCOLS" in line:
                ncols = int(line.split("=")[-1])
            elif "NCOMP" in line:
                ncomp = int(line.split("=")[-1])
            elif "FORMAT" in line:
                skiplines = count + 1
                break
            count += 1

    data = np.loadtxt(path, skiprows = skiplines).reshape(nrows, ncols, ncomp)

    #Taking out all but one color channel
    stripped_data = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            stripped_data[i][j] = data[i][j][0]

    return stripped_data


def read_text_sky_matrix(path):
    with open(path, 'r') as infile:
        #Reading header
        count = 0
        for line in infile:

            if "NROWS" in line:
                nrows = int(line.split("=")[-1])
            elif "NCOLS" in line:
                ncols = int(line.split("=")[-1])
            elif "NCOMP" in line:
                ncomp = int(line.split("=")[-1])
            elif "FORMAT" in line:
                skiplines = count + 1
                break
            count += 1

    data = np.loadtxt(path, skiprows = skiplines).reshape(nrows, ncols, ncomp)

    #Taking out all but one color channel
    stripped_data = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            stripped_data[i][j] = data[i][j][0]

    return stripped_data


def daylight_matmul(info):

    dc_matrix = read_text_dc_matrix(path = info["daylight_dc"])
    #print(dc_matrix)
    #print(dc_matrix.shape)

    sky_matrix = read_text_sky_matrix(path = info["smx_O0_file"])

    start = time.time()
    result = np.matmul(dc_matrix, sky_matrix)
    end = time.time()
    print(result.shape)
    print(f"+++++ CPU matmul wall time: {(end-start)} [s] +++++")

    #https://vitalitylearning.medium.com/a-short-notice-on-performing-matrix-multiplications-in-pycuda-cbfb00cf1450
    start = time.time()
    result = np.matmul(dc_matrix, sky_matrix)
    end = time.time()
    print(result.shape)
    print(f"+++++ CPU matmul wall time: {(end-start)} [s] +++++")
    
