"""
Description:

"""

import numpy as np
import cupy as cp
import time
from subprocess import Popen, PIPE


#%%
def run_rfluxmtx(cmd_list, grids_files_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")


#%%
def read_stdin(input_files_list):
    
    string = ""
    for file_path in input_files_list:
        with open(file_path, "r") as infile:
            for line in infile:
                string = string + line
            
    bytes_input = string.encode()
    
    return bytes_input

#%%

def read_text_matrix(path):

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

#%%

def run_dctimestep(cmd_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"this is stdin")
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start

#%%

def run_rmtxop(cmd_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"this is stdin")
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start

#%%


no_sensor_points_list = np.array([9, 36, 64, 100, 144, 225, 400, 900, 
                                  1600, 2500, 3481, 5625, 10000, 14400,
                                  22500, 40000, 62500, 90000])

#%%
#f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\aperture\\aperture.mat",
#f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\aperture\\aperture.rad",
#f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\scene\\envelope.mat",
#f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\scene\\envelope.rad"

#%% run rluxmtx
for i in range(len(no_sensor_points_list)):
    grids_files_list = [f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\grid\\Room_6.pts"]
    
    cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                "-y", f"{no_sensor_points_list[i]}",
                "-ab", "0", "-ad", "4", "-lw", "0.25",
                "-I", "-",
                "rfluxsky.rad" 
                ]

    run_rfluxmtx(cmd_list, grids_files_list, 
                 output_filename = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.dc")
    
    print(f"{i+1}/{len(no_sensor_points_list)}")

    
#%% Comparing dctimestep 
    
duration_dctimestep_list = []
duration_rmtxop_list = []
for i in range(len(no_sensor_points_list)):
    
    dc_filename = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.dc"
    sky_filename = "DNK_Copenhagen.061800_IWEC.smx"
    
    #Dctimestep and rmtxop
    rgb_path = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.rgb"
    ill_path = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.ill"
    
    cmd_list = ["C:\\Radiance\\bin\\dctimestep",
                dc_filename,
                sky_filename] 
    
    duration_dctimestep = run_dctimestep(cmd_list, output_filename = rgb_path)
    duration_dctimestep_list.append(duration_dctimestep)
    
    cmd_list = ["C:\\Radiance\\bin\\rmtxop",
                "-c", "47.435", "119.93", "11.635", "-fa",
                rgb_path]
    
    duration_rmtxop = run_rmtxop(cmd_list, output_filename = ill_path)
    duration_rmtxop_list.append(duration_rmtxop)
    print(f"{i+1}/{len(no_sensor_points_list)}")
    
    
#%% Save dctimestep results

with open("radiance_timings.txt","w") as outfile:
    outfile.write("dctimestep wall time [s],\trmtxop wall time [s]\n")
    for i in range(len(duration_dctimestep_list)):
        outfile.write(f"{duration_dctimestep_list[i]},\t{duration_rmtxop_list[i]}\n")



#%% with numpy 

numpy_reading_dc_matrix_list = []
numpy_reading_sky_matrix_list = []
numpy_matmul_list = []
numpy_scale_list = []
numpy_write_results_matrix_list = []

for i in range(len(no_sensor_points_list)):
    dc_filename = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.dc"
    sky_filename = "DNK_Copenhagen.061800_IWEC.smx"
    
    ill_path = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output_numpy.ill"
    
    start = time.time()
    dc_matrix = read_text_matrix(dc_filename)
    end = time.time()
    numpy_reading_dc_matrix_list.append((end-start))
    
    start = time.time()
    sky_matrix = read_text_matrix(sky_filename)
    end = time.time()
    numpy_reading_sky_matrix_list.append((end-start))
    
    start = time.time()
    result_matrix = np.matmul(dc_matrix,sky_matrix)
    end = time.time()
    numpy_matmul_list.append((end-start))
    
    start = time.time()
    result_matrix = result_matrix*179
    end = time.time()
    numpy_scale_list.append((end-start))
    
    start = time.time()
    np.savetxt(ill_path,result_matrix)
    end = time.time()
    numpy_write_results_matrix_list.append((end-start))
    
#%%
with open("numpy_timings.txt","w") as outfile:
    outfile.write("reading_dc_matrix [s],\treading_sky_matrix [s],\tmatmul [s],\tscale [s],\tsave [s]\n")
    for i in range(len(duration_dctimestep_list)):
        outfile.write(f"{numpy_reading_dc_matrix_list[i]},\t" +\
                      f"{numpy_reading_sky_matrix_list[i]},\t" +\
                      f"{numpy_matmul_list[i]},\t" +\
                      f"{numpy_scale_list[i]},\t" +\
                      f"{numpy_write_results_matrix_list[i]}\n"
                      )
        
#%% and with cupy

cupy_reading_dc_matrix_list = []
cupy_reading_sky_matrix_list = []
cupy_copy_dc_matrix_list = []
cupy_copy_sky_matrix_list = []
cupy_matmul_list = []
cupy_scale_list = []
cupy_copy_results_matrix_list = []
cupy_write_results_matrix_list = []

for i in range(len(no_sensor_points_list)):
    dc_filename = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output.dc"
    sky_filename = "DNK_Copenhagen.061800_IWEC.smx"
    
    ill_path = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\output_cupy.ill"
    
    #Read dc matrix to numpy
    start = time.time()
    dc_matrix = read_text_matrix(dc_filename)
    end = time.time()
    cupy_reading_dc_matrix_list.append((end-start))
    
    #Read sky matrix to numpy
    start = time.time()
    sky_matrix = read_text_matrix(sky_filename)
    end = time.time()
    cupy_reading_sky_matrix_list.append((end-start))
    
    #Copy dc matrix to cupy
    start = time.time()
    dc_matrix_gpu = cp.asarray(dc_matrix)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    cupy_copy_dc_matrix_list.append((end-start))
    
    #Copy sky matrix to cupy
    start = time.time()
    sky_matrix_gpu = cp.asarray(sky_matrix)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    cupy_copy_sky_matrix_list.append((end-start))
    
    #Cupy matmul
    start = time.time()
    result_matrix_gpu = cp.matmul(dc_matrix_gpu, sky_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    cupy_matmul_list.append((end-start))
    
    #Cupy scaling
    start = time.time()
    result_matrix_gpu = result_matrix_gpu*179
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    cupy_scale_list.append((end-start))
    
    #Copy to device from host (from GPU to CPU) 
    start = time.time()
    result_matrix = cp.asnumpy(result_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    cupy_copy_results_matrix_list.append((end-start))
    
    #Save numpy to text
    start = time.time()
    np.savetxt(ill_path,result_matrix)
    end = time.time()
    cupy_write_results_matrix_list.append((end-start))

#%%
with open("cupy_timings.txt","w") as outfile:
    outfile.write("reading_dc_matrix [s],\treading_sky_matrix [s],\tcopy_dc_matrix [s],\tcopy_sky_matrix [s],\tmatmul [s],\tscale [s],\tcopy_results_matrix [s],\tsave [s]\n")
    for i in range(len(duration_dctimestep_list)):
        outfile.write(f"{cupy_reading_dc_matrix_list[i]},\t" +\
                      f"{cupy_reading_sky_matrix_list[i]},\t" +\
                      f"{cupy_copy_dc_matrix_list[i]},\t" +\
                      f"{cupy_copy_sky_matrix_list[i]},\t" +\
                      f"{cupy_matmul_list[i]},\t" +\
                      f"{cupy_scale_list[i]},\t" +\
                      f"{cupy_copy_results_matrix_list[i]},\t" +\
                      f"{cupy_write_results_matrix_list[i]}\n"
                      )
    
#%% binary reader and saver


def run_rfluxmtx_binary(cmd_list, grids_files_list):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    start = time.time()
    #Reading header
    for binary_line in output:
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
    data = np.fromfile(output, dtype=np.dtype('>f4')).reshape(nrows, ncols, ncomp)
    #data = np.fromfile(reader, dtype=np.float32).reshape(nrows, ncols, ncomp)
    end = time.time()
    duration = end-start
    
    return data, duration

#%%
bytes_read_list = []
binary_write_list = []

sky_filename = "DNK_Copenhagen.061800_IWEC.smx"
sky_matrix = read_text_matrix(sky_filename)

for i in range(len(no_sensor_points_list)):
    grids_files_list = [f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\Daylight\\Radiance\\model\\grid\\Room_6.pts"]
    
    cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                "-y", f"{no_sensor_points_list[i]}",
                "-ab", "0", "-ad", "4", "-lw", "0.25",
                "-I", "-",
                "rfluxsky.rad" 
                ]

    dc_matrix, duration = run_rfluxmtx_binary(cmd_list, grids_files_list)
    bytes_read_list.append(duration)


    
    result_matrix = np.matmul(dc_matrix,sky_matrix)

    path = f"Geometry\\Sensorpoints__{no_sensor_points_list[i]}\\binary_numpy.npy"
    start = time.time()
    np.save(path, result_matrix)
    end = time.time()
    binary_write_list.append((end-start))


#%%


with open("binary_timings.txt","w") as outfile:
    outfile.write("parse bytes [s],\twrite binary [s]\n")
    for i in range(len(duration_dctimestep_list)):
        outfile.write(f"{bytes_read_list[i]},\t{binary_write_list[i]}\n")











#%%

"""
#%% comparing only matmul computations
def benchmark(no_sensor_points):
    
    dc_matrix = np.ones((no_sensor_points,146))
    sky_matrix = np.ones((146,8760))

    start = time.time()
    result_matrix = np.matmul(dc_matrix,sky_matrix)
    end = time.time()
    duration_numpy = end - start
    
    print("Checkpoint 1")
    
    start = time.time()
    dc_matrix_gpu = cp.asarray(dc_matrix)
    sky_matrix_gpu = cp.asarray(sky_matrix)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_copy1 = end - start
    
    print("Checkpoint 2")

    #GPU (cuBLAS) matmul
    start = time.time()
    result_matrix_gpu = cp.matmul(dc_matrix_gpu, sky_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_matmul = end - start

    print("Checkpoint 3")

    #Copy to device from host (from GPU to CPU) 
    start = time.time()
    result_matrix = cp.asnumpy(result_matrix_gpu)
    cp.cuda.Stream.null.synchronize()
    end = time.time()
    duration_gpu_copy_2 = end - start
    
    print("Checkpoint 4")

    gpu_sum = duration_gpu_copy1 + duration_gpu_matmul + duration_gpu_copy_2
    problem_size = dc_matrix.nbytes + sky_matrix.nbytes + result_matrix.nbytes
    
    del dc_matrix_gpu
    del sky_matrix_gpu
    del result_matrix_gpu
    cp._default_memory_pool.free_all_blocks()
    cp._default_pinned_memory_pool.free_all_blocks()
    
    return [duration_numpy, gpu_sum, duration_gpu_copy1, duration_gpu_matmul, duration_gpu_copy_2, problem_size]


#%%
output = []
for i in range(len(no_sensor_points_list)):
    output.append(benchmark(no_sensor_points_list[i]))
    print(f"{i+1}/{len(no_sensor_points_list)}")
    
output = np.array(output)

#%%



#%%




#%%
#benchmark dctimestep and rmtxop:
# Create random scene, and random output from rfluxmtx, with proper size matrix.
"""
