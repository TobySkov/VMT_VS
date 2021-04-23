import os
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


def find_grid_files(info, type):

    grid_folder = info["sim_folder"].joinpath(f"Raytracing\\{type}\\Radiance\\model\\grid")

    grid_files = []

    if type == "Daylight":
        for room in info["room_info"]:
            a = room["name"].split("_")
            grid_files.append(grid_folder.joinpath(f"{a[0]}_{a[1]}.pts"))

    elif type == "Energy":
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