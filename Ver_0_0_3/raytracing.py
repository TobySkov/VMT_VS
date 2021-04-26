import os
import time
from subprocess import Popen, PIPE
import numpy as np
from io_module import timer

def raytracing(info):

    #Creating skies
    timer(run_epw2wea, info)
    timer(run_gendaymtx, info, "visible spektrum")
    timer(run_gendaymtx, info, "full spektrum")

    #Run daylight raytracing command
    timer(run_rfluxmtx, info, 2, "Daylight")

    #Run energy raytracing command
    timer(run_rfluxmtx, info, 2, "Energy")




def run_epw2wea(info):

    info["wea_file"] = info["epw_file"].with_suffix(".wea")

    cmd_list = [str(info["radiance_folder"].joinpath("bin\\epw2wea")),
                str(info["epw_file"]), 
				str(info["wea_file"])]

    run_command(info, cmd_list)


def run_gendaymtx(info,
				  spektrum,
				  sky_resolution = 1):

    cmd_list = [str(info["radiance_folder"].joinpath("bin\\gendaymtx"))]

    if spektrum == "visible spektrum":
        spektrum_cmd = "0"
        output_file_path = info["smx_O0_file"]

    elif spektrum == "full spektrum":
        spektrum_cmd = "1"
        output_file_path = info["smx_O1_file"]


    cmd_list.extend([f"-O{spektrum_cmd}",
                     "-m", f"{sky_resolution}",
                     "-r", "0.0",
                     "-c", "1", "1", "1",
                     str(info["wea_file"])])
    #"-of" gives binary output but manual says that it is not working on Windows OS

    run_command(info, cmd_list, output_file_path)


def rtrace_parameters(resolution):
	##Most important Radiance parameters:
    #   https://unmethours.com/question/40179/radiance-convergence-simulation-parameters/
    
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41 example only using lw, ab and ad
    
    ##Discourse: lw = 1/ad or lower
    #https://discourse.ladybug.tools/t/5-phase-method-simulation-times/2891/6
    if resolution == -1:
        rtrace_cmd = ["-ab", "1"]
    
    #From HB+ for RADIATION
    elif resolution == 0:
        rtrace_cmd = ["-ab", "3", "-ad", "5000", "-lw", f"{1/5000}"]
    
    elif resolution == 1:
        rtrace_cmd = ["-ab", "5", "-ad", "15000", "-lw", f"{1/15000}"]

    elif resolution == 2:
        rtrace_cmd = ["-ab", "7", "-ad", "25000", "-lw", f"{1/(25000)}"]

    return rtrace_cmd


def find_rad_files(info, type):

    model_folder = info["sim_folder"].joinpath(f"Raytracing\\{type}\\Radiance\\model")

    scene = [str(model_folder.joinpath("scene\\envelope.mat")),
             str(model_folder.joinpath("scene\\shades.mat")),
             str(model_folder.joinpath("aperture\\aperture.mat")),
             str(model_folder.joinpath("scene\\envelope.rad")),
             str(model_folder.joinpath("scene\\shades.rad")),
             str(model_folder.joinpath("aperture\\aperture.rad"))]

    return scene







def run_rfluxmtx(info, resolution, type):
       
    cmd_list = [str(info["accelerad_folder"].joinpath("bin\\accelerad_rfluxmtx"))]
    
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41
    # - denotes that sender will be given through standard input
    cmd_list.extend(["-faa", "-y", str(info[f"no_{type.lower()}_sensorpoints"]),"-I"])
    #"-faf" yields float binary output 

    cmd_list.extend(rtrace_parameters(resolution))

    cmd_list.extend(["-",   #This specifies that sender is from stdin
                     str(info["rfluxsky"])] + \
                     find_rad_files(info, type))

    run_command(info,
                cmd_list, 
				output_file_path = info[f"{type.lower()}_dc"],
                input_files_list = info[f"grid_files_{type.lower()}"])


def read_stdin(input_files_list):
    
    string = ""
    for file_path in input_files_list:
        with open(file_path, "r") as infile:
            for line in infile:
                string = string + line
            
    bytes_input = string.encode()
    
    return bytes_input



def run_command(info,
                cmd_list, 
                output_file_path = False,
                input_files_list = False,
                output_numpy = False):
    
    radiance_bin = info["radiance_folder"].joinpath("bin")
    accelerad_bin = info["accelerad_folder"].joinpath("bin")
    radiance_lib = info["radiance_folder"].joinpath("lib")
    accelerad_lib = info["accelerad_folder"].joinpath("lib")

	#Setting enviromental variable PATH
    os.environ["PATH"] = f"{radiance_bin};{accelerad_bin};" + "{}".format(os.environ["PATH"])

	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = f".;{radiance_lib};{accelerad_lib};"

    print("START - Subprocess: {}".format(cmd_list[0]))

	# Run process
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if input_files_list != False:
        output, err = p.communicate(read_stdin(input_files_list))
    else:
        output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    
    if rc != 0:
        print(f"Error code: \n {err}")

    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))


	#Saving output in plain text
    if output_file_path != False:
        print("START - Writing ASCII data")
        with open(output_file_path, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")

