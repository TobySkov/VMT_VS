import time
import numpy as np
import cupy as cp
from io_module import read_text_matrix, timer
import pickle
from itertools import chain


def raytracing_postprocessing(info):

    #Daylight matmul and calc_DA
    daylight(info)

    #Energy matmul 
    energy(info)

    #Energy matmul 
    energy_outside(info)


def energy_outside(info):

    if info["raytracing_output"] == "text":
        #Reading dc matrix
        energy_dc_matrix = timer(read_text_matrix, info["energy_outside_dc_matrix"])
        #Reading sky matrix
        energy_sky_matrix = timer(read_text_matrix, info["energy_sky_matrix"])

    elif info["raytracing_output"] == "binary":
        energy_dc_matrix = info["energy_outside_dc_matrix"]
        energy_sky_matrix = info["energy_sky_matrix"]


    if info["matmul_hardware"] == "cpu":
        #CPU (BLAS) matmul
        Phi_sol_2d_Wm2 = timer(np.matmul, energy_dc_matrix, energy_sky_matrix)


    #Multiplying with relevant window areas
    Phi_sol_2d_W = np.zeros((info["no_energy_outside_sensorpoints"], 8760))

    aperture_areas = []
    for room in info["room_info"]:
        aperture_areas.extend(list(chain.from_iterable(room["aperture_areas_list"])))
    aperture_areas = np.array(aperture_areas)

    for i in range(8760):
        Phi_sol_2d_W[:,i] = np.multiply(Phi_sol_2d_Wm2[:,i],aperture_areas)

    info["Phi_sol_2d_W_outside"] = Phi_sol_2d_W


        




def energy(info):

    if info["raytracing_output"] == "text":
        #Reading dc matrix
        energy_dc_matrix = timer(read_text_matrix, info["energy_inside_dc_matrix"])
        #Reading sky matrix
        energy_sky_matrix = timer(read_text_matrix, info["energy_sky_matrix"])

    elif info["raytracing_output"] == "binary":
        energy_dc_matrix = info["energy_inside_dc_matrix"]
        energy_sky_matrix = info["energy_sky_matrix"]


    if info["matmul_hardware"] == "cpu":
        #CPU (BLAS) matmul
        Phi_sol_2d_Wm2 = timer(np.matmul, energy_dc_matrix, energy_sky_matrix)


    #Multiplying with relevant window areas
    Phi_sol_2d_W = np.zeros((info["no_energy_inside_sensorpoints"], 8760))

    aperture_areas = []
    for room in info["room_info"]:
        #print(room["aperture_identifiers_list"])
        #print(list(chain.from_iterable(room["aperture_areas_list"])))
        aperture_areas.extend(list(chain.from_iterable(room["aperture_areas_list"])))
    aperture_areas = np.array(aperture_areas)

    for i in range(8760):
        Phi_sol_2d_W[:,i] = np.multiply(Phi_sol_2d_Wm2[:,i],aperture_areas)
        
    info["Phi_sol_2d_W"] = Phi_sol_2d_W


def daylight(info):

    if info["raytracing_output"] == "text":
        #Reading dc matrix
        daylight_dc_matrix = timer(read_text_matrix, info["daylight_dc_matrix"])
        #Reading sky matrix
        daylight_sky_matrix = timer(read_text_matrix, info["daylight_sky_matrix"])

    elif info["raytracing_output"] == "binary":
        daylight_dc_matrix = info["daylight_dc_matrix"]
        daylight_sky_matrix = info["daylight_sky_matrix"]

    if info["matmul_hardware"] == "cpu":
        #CPU (BLAS) matmul
        result_matrix = timer(np.matmul, daylight_dc_matrix, daylight_sky_matrix)

        calc_da_cpu(info, result_matrix)

    elif info["matmul_hardware"] == "gpu":
        #Copy to host from device (from CPU to GPU)
        start = time.time()
        daylight_dc_matrix_gpu = cp.asarray(daylight_dc_matrix)
        daylight_sky_matrix_gpu = cp.asarray(daylight_sky_matrix)
        end = time.time()
        print(f"+++++ CPU to GPU copy: {(end-start)} [s] +++++")

        #GPU (cuBLAS) matmul
        start = time.time()
        result_matrix_gpu = cp.matmul(daylight_dc_matrix_gpu, daylight_sky_matrix_gpu)
        end = time.time()
        print(f"+++++ GPU matmul: {(end-start)} [s] +++++")

        #Copy to device from host (from GPU to CPU) 
        start = time.time()
        result_matrix = cp.asnumpy(result_matrix_gpu)
        end = time.time()
        print(f"+++++ GPU to CPU copy: {(end-start)} [s] +++++")
    
    #print(f"Problem memory size in kbytes: {(daylight_dc_matrix.nbytes + daylight_sky_matrix.nbytes + result_matrix.nbytes)/1000}")

    
def calc_da_cpu(info, result_matrix):

    occ_sch = gen_occ_sch()
    sch_idx = occ_sch == 1

    #Calculate DA on all
    data = result_matrix[:,sch_idx]
    above_300 = (data*179) >= 300 #179 lm/W; above 300 lux
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