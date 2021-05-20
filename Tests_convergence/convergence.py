"""
Description: Convergence testing of Radiance ambient parameters run using
Accelerad. 

Source:
https://unmethours.com/question/40179/radiance-convergence-simulation-parameters/

"""
import os
from subprocess import Popen, PIPE
import time

base = os.path.dirname(__file__)

#Setting enviromental variable PATH
os.environ["PATH"] = "C:\\Accelerad\\bin;" + \
    "C:\\Radiance\\bin;" + \
    "{}".format(os.environ["PATH"])
    
#Setting enviromental variable RAYPATH
os.environ["RAYPATH"] = ".;" + \
    "C:\\Accelerad\\lib;" + \
    "C:\\Radiance\\lib"


#%%
#ab_list = [6, 8, 10, 12] # 4 different
#ad_list = [1024, 4096, 16384, 65536, 262142] # 5 different
#lw_power_list = [1, 1.5, 2, 2.5, 3] # 5 different
#4*5*5 = 100 options

#Missing simulations
ab_list = [12] # 4 different
ad_list = [262142] # 5 different
lw_power_list = [2, 2.5, 3] # 5 different
#4*5*5 = 100 options

#%%
no_sensor_points = 4096
rfluxsky_file = "rfluxsky.rad"
geo_oct = "convergence_geo.oct"
grids_files_list = [base + "\\Triangles_3500__Points_4096\\Radiance\\model\\grid\\SensorGrid_75e894a0.pts"]

#%%

def run_rfluxmtx(cmd_list, grids_files_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
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
for i in range(len(ab_list)):
    for j in range(len(ad_list)):
        for k in range(len(lw_power_list)):
            ab = ab_list[i]
            ad = ad_list[j]
            lw = 1/(ad**lw_power_list[k])
            
            
            cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                        "-y", f"{no_sensor_points}",
                        "-ab", f"{ab}",
                        "-ad", f"{ad}",
                        "-lw", f"{lw}",
                        "-I", "-",
                        f"{rfluxsky_file}",
                        "-i", f"{geo_oct}"]
            
            #Run 1
            start = time.time()
            output_filename = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__run1.txt"
            run_rfluxmtx(cmd_list, grids_files_list, output_filename)
            end = time.time()
            run_1_duration = end-start
            
            #Run 2
            start = time.time()
            output_filename = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__run2.txt"
            run_rfluxmtx(cmd_list, grids_files_list, output_filename)
            end = time.time()
            run_2_duration = end-start

            #Write timings
            with open(f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__timings.txt", "w") as outfile:
                outfile.write(f"Wall time, run1: {run_1_duration} [s]\n")
                outfile.write(f"Wall time, run2: {run_2_duration} [s]\n")



