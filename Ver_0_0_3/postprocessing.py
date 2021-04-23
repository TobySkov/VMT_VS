import time
import numpy as np
import cupy as cp
from io_module import read_text_matrix
import pickle



def raytracing_postprocessing(info):

    #Daylight matmul and calc_DA
    #daylight(info, 
    #         reader = "Text",
    #         matmul = "CPU")


    #Energy matmul
    energy(info, 
             reader = "Text",
             matmul = "CPU")




def energy(info, reader, matmul):

    if reader == "Text":
        #Reading dc matrix
        start = time.time()
        dc_matrix = read_text_matrix(path = info["energy_dc"])
        end = time.time()
        print(f"+++++ dc_matrix reading time: {(end-start)} [s] +++++\n")

        #Reading sky matrix
        start = time.time()
        sky_matrix = read_text_matrix(path = info["smx_O1_file"])
        end = time.time()
        print(f"+++++ sky_matrix reading time: {(end-start)} [s] +++++\n")

    if matmul == "CPU":
        #CPU (BLAS) matmul
        start = time.time()
        Phi_sol_2d_Wm2 = np.matmul(dc_matrix, sky_matrix)
        end = time.time()
        print(f"+++++ CPU matmul wall time: {(end-start)} [s] +++++\n")

    Phi_sol_2d_W = np.zeros((info["no_energy_sensorpoints"], 8760))

    aperture_areas = []
    for room in info["room_info"]:
        aperture_areas.extend(room["aperture_areas_list"])
        
    aperture_areas = np.array(aperture_areas)

    for i in range(8760):
        Phi_sol_2d_W[:,i] = np.dot(Phi_sol_2d_Wm2[:,i],aperture_areas)

    info["Phi_sol_2d_W"] = Phi_sol_2d_W


def daylight(info, reader, matmul):

    if reader == "Text":
        #Reading dc matrix
        start = time.time()
        dc_matrix = read_text_matrix(path = info["daylight_dc"])
        end = time.time()
        print(f"+++++ dc_matrix reading time: {(end-start)} [s] +++++\n")

        #Reading sky matrix
        start = time.time()
        sky_matrix = read_text_matrix(path = info["smx_O0_file"])
        end = time.time()
        print(f"+++++ sky_matrix reading time: {(end-start)} [s] +++++\n")

    if matmul == "CPU":
        #CPU (BLAS) matmul
        start = time.time()
        result_matrix = np.matmul(dc_matrix, sky_matrix)
        end = time.time()
        print(f"+++++ CPU matmul wall time: {(end-start)} [s] +++++\n")

        calc_da_cpu(info, result_matrix)

    elif matmul == "GPU":
        #Copy to host from device (from CPU to GPU)
        start = time.time()
        dc_matrix_gpu = cp.asarray(dc_matrix)
        sky_matrix_gpu = cp.asarray(sky_matrix)
        end = time.time()
        print(f"+++++ CPU to GPU copy: {(end-start)} [s] +++++")

        #GPU (cuBLAS) matmul
        start = time.time()
        result_matrix_gpu = cp.matmul(dc_matrix_gpu,sky_matrix_gpu)
        end = time.time()
        print(f"+++++ GPU matmul: {(end-start)} [s] +++++")

        #Copy to device from host (from GPU to CPU) 
        start = time.time()
        result_matrix = cp.asnumpy(result_matrix_gpu)
        end = time.time()
        print(f"+++++ GPU to CPU copy: {(end-start)} [s] +++++")
    
    print(f"Problem memory size in kbytes: {(dc_matrix.nbytes + sky_matrix.nbytes + result_matrix.nbytes)/1000}")

    
def calc_da_cpu(info, result_matrix):

    occ_sch = gen_occ_sch()
    sch_idx = occ_sch == 1

    #Calculate DA on all
    data = result_matrix[:,sch_idx]
    above_300 = (data*179) > 300 #179 lm/W; above 300 lux
    da = (((above_300).sum(axis=1))/above_300.shape[1])*100

    start_idx = 0
    end_idx = 0
    #For each room
    for file in info["grid_files_daylight"]:

        len_file = file_len(file)

        end_idx += len_file

        file_name = file.with_suffix(".pkl").name
        with open(info["sim_folder"].joinpath(f"output\\da\\{file_name}"), 'wb') as outfile:
            pickle.dump(da[start_idx:end_idx].tolist(), outfile, protocol=2) #Protocol 2 needed for GHpython to read it

        start_idx += len_file

        


def file_len(fname):
    #Count lenght of file (i.e. numbers of points in file)
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



def gen_occ_sch():
    occ_sch = []
    weekday = [0]*8 + [1]*9 + [0]*7
    weekendday = [0]*24
    for i in range(52):
        for j in range(5):
            occ_sch.extend(weekday)
        for j in range(2):
            occ_sch.extend(weekendday)
    occ_sch.extend(weekendday)

    assert len(occ_sch) == 8760

    return np.array(occ_sch)