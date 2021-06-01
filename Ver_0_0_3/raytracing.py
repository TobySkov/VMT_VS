import os
import time
from subprocess import Popen, PIPE
import numpy as np
from io_module import timer

def raytracing(info):

    #Creating skies
    timer(run_epw2wea, info)
    timer(run_gendaymtx, info, "daylight")
    timer(run_gendaymtx, info, "energy")

    #Run daylight raytracing command
    timer(run_rfluxmtx, info, info["raytracing_resolution"], "daylight")

    #Run energy inside raytracing command
    timer(run_rfluxmtx, info, info["raytracing_resolution"], "energy_inside")

    #Run energy outside raytracing command
    #timer(run_rfluxmtx, info, info["raytracing_resolution"], "energy_outside")



def run_epw2wea(info):

    info["wea_file"] = info["epw_file"].with_suffix(".wea")

    cmd_list = [str(info["radiance_folder"].joinpath("bin\\epw2wea")),
                str(info["epw_file"]), 
				str(info["wea_file"])]

    #Setting enviromental variable PATH
    os.environ["PATH"] = str(info["radiance_bin"]) + ";{};".format(os.environ["PATH"])
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = ".;" + str(info["radiance_lib"]) + ";"

	# Run process
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))





def run_gendaymtx(info,
				  type,
				  sky_resolution = 1):

    ###Prepare cmd list
    cmd_list = [str(info["radiance_folder"].joinpath("bin\\gendaymtx"))]

    if type == "daylight":
        spektrum_cmd = "0"

    elif type == "energy":
        spektrum_cmd = "1"

    cmd_list.extend([f"-O{spektrum_cmd}",
                     "-m", f"{sky_resolution}",
                     "-r", "0.0",
                     "-c", "1", "1", "1",
                     str(info["wea_file"])])

    ###Run command
	#Setting enviromental variable PATH
    os.environ["PATH"] = str(info["radiance_bin"]) + ";{}".format(os.environ["PATH"])
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = ".;" + str(info["radiance_lib"])

	# Run process
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))


	#Saving output in plain text
    if info["raytracing_output"] == "text":
        print("START - Writing ASCII data")
        with open(info[f"{type}_sky_matrix"], "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")

    elif info["raytracing_output"] == "binary":
        print("START - Saving binary output")
        sky_matrix = np.zeros((146,8760), dtype = np.float64)
        all_data = output.decode().split("\r\n\r\n")
        del all_data[0]
        del all_data[-1]
        for i, patch_year in enumerate(all_data):
            patch_year_split = patch_year.split("\r\n")
            for j, hour in enumerate(patch_year_split):
                sky_matrix[i][j] = hour.split(" ")[0] #Only reading one channel
        info[f"{type}_sky_matrix"] = sky_matrix
        print("DONE - Saving binary output")
        





def run_rfluxmtx(info, resolution, type):
       
    cmd_list = [str(info["accelerad_folder"].joinpath("bin\\accelerad_rfluxmtx"))]

    cmd_list.extend(["-faa", "-y", str(info[f"no_{type}_sensorpoints"]),"-I"])

    cmd_list.extend(rtrace_parameters(resolution))

    cmd_list.extend(["-",   #This specifies that sender is from stdin
                     str(info["rfluxsky"])] + \
                     find_rad_files(info, type))

    ###Run command
	#Setting enviromental variable PATH
    os.environ["PATH"] = str(info["accelerad_bin"]) + ";" + str(info["radiance_bin"]) + ";{}".format(os.environ["PATH"])
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = ".;" + str(info["accelerad_lib"]) + ";" + str(info["radiance_lib"])

    
	# Run process
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(info[f"grid_files_{type}"]))
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))


	#Saving output in plain text
    if info["raytracing_output"] == "text":
        print("START - Writing ASCII data")
        with open(info[f"{type}_dc_matrix"], "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")

    elif info["raytracing_output"] == "binary":
        print("START - Saving binary output")
        dc_matrix = np.zeros((info[f"no_{type}_sensorpoints"],146), dtype = np.float64)
        all_data = output.decode().split("\r\n\r\n")[1].split("\r\n")
        del all_data[-1]
        for i, pts in enumerate(all_data):
            pts_split = pts.split("\t")
            del pts_split[-1]
            for j in range(146):
                dc_matrix[i][j] = pts_split[j*3]
        info[f"{type}_dc_matrix"] = dc_matrix
        print("DONE - Saving binary output")

    





def find_rad_files(info, type):

    model_folder = info["sim_folder"].joinpath(f"Raytracing\\{type}\\Radiance\\model")

    scene_ini = [model_folder.joinpath("scene\\envelope.mat"),
                model_folder.joinpath("scene\\shades.mat"),
                model_folder.joinpath("aperture\\aperture.mat"),
                model_folder.joinpath("scene\\envelope.rad"),
                model_folder.joinpath("scene\\shades.rad"),
                model_folder.joinpath("aperture\\aperture.rad")]

    scene = []
    for path in scene_ini:
        if os.path.isfile(path):
            scene.append(str(path))

    return scene



def read_stdin(input_files_list):
    
    string = ""
    for file_path in input_files_list:
        with open(file_path, "r") as infile:
            for line in infile:
                string = string + line
            
    bytes_input = string.encode()
    
    return bytes_input





def rtrace_parameters(resolution):
	##Most important Radiance parameters:
    #   https://unmethours.com/question/40179/radiance-convergence-simulation-parameters/
    
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41 example only using lw, ab and ad
    
    ##Discourse: lw = 1/ad or lower
    #https://discourse.ladybug.tools/t/5-phase-method-simulation-times/2891/6

    if resolution == "default":
        rtrace_cmd = ["-ab", "6", "-ad", "65536", "-lw", f"{1/65536}"]

    elif resolution == -1:
        rtrace_cmd = ["-ab", "1"]
    #From HB+ for RADIATION
    elif resolution == 0:
        rtrace_cmd = ["-ab", "3", "-ad", "5000", "-lw", f"{1/5000}"]
    
    elif resolution == 1:
        rtrace_cmd = ["-ab", "5", "-ad", "15000", "-lw", f"{1/15000}"]

    elif resolution == 2:
        rtrace_cmd = ["-ab", "7", "-ad", "25000", "-lw", f"{1/(25000)}"]

    elif resolution == 3:
        rtrace_cmd = ["-ab", "10", "-ad", "100000", "-lw", f"{1/(100000)}"]


    return rtrace_cmd

