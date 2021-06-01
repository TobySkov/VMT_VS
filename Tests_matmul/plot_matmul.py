"""
Description:

"""

import numpy as np
import cupy as cp
import time
from subprocess import Popen, PIPE
import os
import matplotlib.pyplot as plt

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_matmul"
print(os.getcwd())
os.chdir(path)
print(os.getcwd())

#%% read results

radiance_timings = np.loadtxt("radiance_timings.txt",delimiter = ",\t", skiprows = 1)
numpy_timings = np.loadtxt("numpy_timings.txt",delimiter = ",\t", skiprows = 1)
cupy_timings = np.loadtxt("cupy_timings_old3.txt",delimiter = ",\t", skiprows = 1)
binary_timings = np.loadtxt("binary_timings.txt",delimiter = ",\t", skiprows = 1)

#%%
no_sensor_points_list = np.array([9, 36, 64, 100, 144, 225, 400, 900, 
                                  1600, 2500, 3481, 5625, 10000, 14400,
                                  22500, 40000, 62500, 90000])

#%% radiance timings
#path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_raytracing\plots"
#plt.savefig(path + "\\" + "rfluxmtx.png", dpi=500, bbox_inches = 'tight', pad_inches = 0)


x = list(range(17))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(radiance_timings[:,0], label = "dctimestep")
plt.plot(radiance_timings[:,1], label = "rmtxop")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Radiance native functions runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:17], rotation = 70, fontsize=12)
plt.show()

#%% numpy

x = list(range(18))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(numpy_timings[:,0], label = "reading dc matrix")
plt.plot(numpy_timings[:,1], label = "reading sky matrix")
plt.plot(numpy_timings[:,2], label = "matmul")
plt.plot(numpy_timings[:,3], label = "scale")
plt.plot(numpy_timings[:,4], label = "save result matrix")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("numpy runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:18], rotation = 70, fontsize=12)
plt.show()

#%% numpy without save results

x = list(range(18))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(numpy_timings[:,0], label = "reading dc matrix")
plt.plot(numpy_timings[:,1], label = "reading sky matrix")
plt.plot(numpy_timings[:,2], label = "matmul")
plt.plot(numpy_timings[:,3], label = "scale")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("numpy runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:18], rotation = 70, fontsize=12)
plt.show()


#%% cupy

x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(cupy_timings[:,0], label = "reading dc matrix")
plt.plot(cupy_timings[:,1], label = "reading sky matrix")
plt.plot(cupy_timings[:,2], label = "copy dc matrix")
plt.plot(cupy_timings[:,3], label = "copy sky matrix")
plt.plot(cupy_timings[:,4], label = "matmul")
plt.plot(cupy_timings[:,5], label = "scale")
plt.plot(cupy_timings[:,6], label = "copy results matrix")
plt.plot(cupy_timings[:,7], label = "save result matrix")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("cupy runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()

#%% cupy without save results

x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(cupy_timings[:,0], label = "reading dc matrix")
plt.plot(cupy_timings[:,1], label = "reading sky matrix")
plt.plot(cupy_timings[:,2], label = "copy dc matrix")
plt.plot(cupy_timings[:,3], label = "copy sky matrix")
plt.plot(cupy_timings[:,4], label = "matmul")
plt.plot(cupy_timings[:,5], label = "scale")
plt.plot(cupy_timings[:,6], label = "copy results matrix")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("cupy runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()


#%% cupy vs numpy 


x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(cupy_timings[:,2], label = "cupy - copy dc matrix")
plt.plot(cupy_timings[:,3], label = "cupy - copy sky matrix")
plt.plot(cupy_timings[:,4], label = "cupy - matmul")
plt.plot(cupy_timings[:,5], label = "cupy - scale")
plt.plot(cupy_timings[:,6], label = "cupy - copy results matrix")
plt.plot(numpy_timings[:16,2], label = "numpy - matmul")
plt.plot(numpy_timings[:16,3], label = "numpy - scale")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("cupy vs numpy runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()


#%%


x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(radiance_timings.sum(axis=1)[:16], label = "Radiance total runtime")
plt.plot(numpy_timings.sum(axis=1)[:16], label = "numpy total runtime")
plt.plot(cupy_timings.sum(axis=1), label = "cupy total runtime")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Total runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()


#%%


x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(numpy_timings.sum(axis=1)[:16], label = "numpy total runtime")
plt.plot(cupy_timings.sum(axis=1), label = "cupy total runtime")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Total runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()


#%%

cupy_short = cupy_timings[:,2] + cupy_timings[:,3] + cupy_timings[:,4] + cupy_timings[:,5] + cupy_timings[:,6]
numpy_short = numpy_timings[:16,2] + numpy_timings[:16,3]


x = list(range(16))

plt.figure(figsize=(6,3),dpi=500)
plt.plot(numpy_short, label = "numpy total runtime")
plt.plot(cupy_short, label = "cupy total runtime")
plt.xlabel("Number of sensor points", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Total runtime", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=no_sensor_points_list[0:16], rotation = 70, fontsize=12)
plt.show()

