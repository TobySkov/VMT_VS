import os 
import sys
import time
from pathlib import Path
from raytracing import raytracing
from ISO13790 import ISO13790
from postprocessing import raytracing_postprocessing
from io_module import define_dict


def main():

    print(" +++++ VMT backend - start +++++")
    start = time.time()


    #Reading command line inputs
    cmd = Path(sys.argv[0])
    vmt_folder = cmd.parent
    sim_folder = Path(sys.argv[1])
    radiance_folder = Path(sys.argv[2])
    accelerad_folder = Path(sys.argv[3])

    #Defining info dictionary
    info = define_dict(vmt_folder, sim_folder, 
                       radiance_folder, accelerad_folder)

    info["raytracing_output"] = "binary" #Options: "binary"/"text"
    info["matmul_hardware"] = "cpu" #Options: "cpu"/"gpu"
    info["raytracing_resolution"] = 2 #Options 0/1/2

    #Running raytracing
    raytracing(info)

    #Running postprocessing
    raytracing_postprocessing(info)

    #Running ISO13790
    ISO13790(info)
    
    end = time.time()
    print("+++++ VMT backend - done +++++")
    print(f"+++++ Wall time: {(end-start)/60} [min] +++++")


if __name__ == "__main__":
    main()