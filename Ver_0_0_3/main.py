import os 
import sys
import time
import shutil
from pathlib import Path
from raytracing import raytracing
#from ISO13790 import run_ISO13790
from postprocessing import postprocessing
from io_module import find_grid_files

def main():

    print(" +++++ VMT backend - start +++++")
    start = time.time()


    #Reading command line inputs
    cmd = Path(sys.argv[0])
    vmt_folder = cmd.parent
    print(f"VMT folder: {vmt_folder}\n")

    sim_folder = Path(sys.argv[1])
    print(f"Simulation folder: {sim_folder}\n")

    radiance_folder = Path(sys.argv[2])
    print(f"Radiance folder: {radiance_folder}\n")

    accelerad_folder = Path(sys.argv[3])
    print(f"Accelerad folder: {accelerad_folder}\n")

    epw_file = Path(sys.argv[4])
    print(f"EPW file: {epw_file}\n")

    no_daylight_sensorpoints = int(sys.argv[5])
    no_energy_sensorpoints = int(sys.argv[6])

    src = vmt_folder.joinpath("rfluxsky.rad")
    dst = epw_file.with_name("rfluxsky.rad")
    shutil.copy(src,dst)

    info = {"vmt_folder": vmt_folder,
            "sim_folder": sim_folder,
            "radiance_folder": radiance_folder,
            "accelerad_folder": accelerad_folder,
            "epw_file": epw_file,
            "rfluxsky": dst,
            "no_daylight_sensorpoints": no_daylight_sensorpoints,
            "no_energy_sensorpoints": no_energy_sensorpoints}

    info["daylight_dc"] = info["sim_folder"].joinpath(f"output\\daylight_dc.txt")
    info["energy_dc"] = info["sim_folder"].joinpath(f"output\\energy_dc.txt")
    if not os.path.exists(info["daylight_dc"].parent):
        os.makedirs(info[f"daylight_dc"].parent)

    info["smx_O0_file"] = info["epw_file"].with_suffix(".smx_O0")
    info["smx_O1_file"] = info["epw_file"].with_suffix(".smx_O1")

    find_grid_files(info, type = "Daylight")
    find_grid_files(info, type = "Energy")

    if not os.path.exists(info["sim_folder"].joinpath(f"output\\da")):
        os.makedirs(info["sim_folder"].joinpath(f"output\\da"))

    #Running raytracing
    raytracing(info)

    #Running ISO13790
    #run_ISO13790(info)

    #Running postprocessing
    postprocessing(info)
    
    end = time.time()
    print("+++++ VMT backend - done +++++")
    print(f"+++++ Wall time: {(end-start)/60} [min] +++++")


if __name__ == "__main__":
    main()