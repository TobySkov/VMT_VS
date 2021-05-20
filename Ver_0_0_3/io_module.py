import os
import shutil
import pickle
import time
import numpy as np
from pathlib import Path

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



#https://stackoverflow.com/questions/803616/passing-functions-with-arguments-to-another-function-in-python
def timer(func, *args):
    start = time.time()
    out = func(*args)
    end = time.time()
    print(f"+++++ {func.__name__}, wall time: {end-start} [s] +++++")
    return out




def find_grid_files(info, type):

    grid_folder = info["sim_folder"].joinpath(f"Raytracing\\{type}\\Radiance\\model\\grid")

    grid_files = []

    if type == "Daylight":
        for room in info["room_info"]:
            a = room["name"].split("_")
            grid_files.append(grid_folder.joinpath(f"{a[0]}_{a[1]}.pts"))

    elif "Energy" in type:
        for room in info["room_info"]:
            for aperture in room["aperture_identifiers_list"]:
                a = grid_folder.joinpath(aperture + "_SensorGrid.pts")
                grid_files.append(a)

    info[f"grid_files_{type.lower()}"] = grid_files


def read_latitude(info):
    with open(info["epw_file"], "r") as infile:
        line = infile.readline()
        latitude = float(line.split(",")[6])
    if latitude >= 0:
        info["hemisphere"] = "northern"
    elif latitude < 0:
        info["hemisphere"] = "southern"






def define_dict(vmt_folder, sim_folder, radiance_folder, accelerad_folder):

    info_pkl = sim_folder.joinpath("info.pkl")
    with open(info_pkl, 'rb') as pkl_file:
        info_ini = pickle.load(pkl_file)

    src = vmt_folder.joinpath("rfluxsky.rad")
    dst = Path(info_ini["epw_file"]).with_name("rfluxsky.rad")
    shutil.copy(src,dst)

    info = {"vmt_folder": vmt_folder,
            "sim_folder": sim_folder,
            "radiance_folder": radiance_folder,
            "accelerad_folder": accelerad_folder,
            "epw_file": Path(info_ini["epw_file"]),
            "rfluxsky": dst,
            "no_daylight_sensorpoints": int(info_ini["no_daylight_sensorpoints"]),
            "no_energy_inside_sensorpoints": int(info_ini["no_energy_inside_sensorpoints"]),
            "no_energy_outside_sensorpoints": int(info_ini["no_energy_outside_sensorpoints"])}

    info["daylight_dc_matrix"] = info["sim_folder"].joinpath(f"output\\daylight_dc.txt")
    info["energy_inside_dc_matrix"] = info["sim_folder"].joinpath(f"output\\energy_inside_dc.txt")
    info["energy_outside_dc_matrix"] = info["sim_folder"].joinpath(f"output\\energy_outside_dc.txt")

    if not os.path.exists(info["daylight_dc_matrix"].parent):
        os.makedirs(info[f"daylight_dc_matrix"].parent)

    info["daylight_sky_matrix"] = info["epw_file"].with_suffix(".smx_O0")
    info["energy_sky_matrix"] = info["epw_file"].with_suffix(".smx_O1")

    if not os.path.exists(info["sim_folder"].joinpath("output\\da")):
        os.makedirs(info["sim_folder"].joinpath("output\\da"))

    if not os.path.exists(info["sim_folder"].joinpath("output\\ISO13790")):
        os.makedirs(info["sim_folder"].joinpath("output\\ISO13790"))

    info["room_info_pkl"] = info["sim_folder"].joinpath("ISO13790\\rooms_info.pkl")
    with open(info["room_info_pkl"], 'rb') as pkl_file:
        info["room_info"] = pickle.load(pkl_file)

    info["theta__e_pkl"] = info["sim_folder"].joinpath("ISO13790\\theta__e.pkl")
    with open(info["theta__e_pkl"], 'rb') as pkl_file:
        info["theta__e"] = pickle.load(pkl_file)

    find_grid_files(info, type = "Daylight")
    find_grid_files(info, type = "Energy_inside")
    find_grid_files(info, type = "Energy_outside")

    read_latitude(info)

    info["radiance_bin"] = info["radiance_folder"].joinpath("bin")
    info["radiance_lib"] = info["radiance_folder"].joinpath("lib")
    info["accelerad_bin"] = info["accelerad_folder"].joinpath("bin")
    info["accelerad_lib"] = info["accelerad_folder"].joinpath("lib")

    return info