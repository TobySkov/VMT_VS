"""
Description:

"""

import numpy as np
import cupy as cp
import time

no_sensor_points_list = np.array([1,10,100,1000,10000,50000,80000,90000])
#no_sensor_points_list = np.array([1,10,100,1000])



def benchmark(no_sensor_points):
    
    dc_matrix = np.ones((no_sensor_points,146))
    sky_matrix = np.ones((146,8760))

    start = time.time()
    result_matrix = np.matmul(dc_matrix,sky_matrix)
    end = time.time()
    duration_numpy = end - start
    
    
    start = time.time()
    dc_matrix_gpu = cp.asarray(dc_matrix)
    sky_matrix_gpu = cp.asarray(sky_matrix)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_copy1 = end - start

    #GPU (cuBLAS) matmul
    start = time.time()
    result_matrix_gpu = cp.matmul(dc_matrix_gpu, sky_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_matmul = end - start

    #Copy to device from host (from GPU to CPU) 
    start = time.time()
    result_matrix = cp.asnumpy(result_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_copy_2 = end - start

    gpu_sum = duration_gpu_copy1 + duration_gpu_matmul + duration_gpu_copy_2
    problem_size = dc_matrix.nbytes + sky_matrix.nbytes + result_matrix.nbytes
    
    return [duration_numpy, gpu_sum, duration_gpu_copy1, duration_gpu_matmul, duration_gpu_copy_2, problem_size]

#%%
output = []
for i in range(len(no_sensor_points_list)):
    output.append(benchmark(no_sensor_points_list[i]))
    
output = np.array(output)

#%%

print(cp.get_default_memory_pool().get_limit())



#%%

mempool = cp.get_default_memory_pool()



#%%
#benchmark dctimestep and rmtxop:
# Create random scene, and random output from rfluxmtx, with proper size matrix.

