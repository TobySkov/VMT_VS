"""
Description: Convergence testing of Radiance ambient parameters run using
Accelerad. 

Source:
https://unmethours.com/question/40179/radiance-convergence-simulation-parameters/

"""
import os
from subprocess import Popen, PIPE


#Setting enviromental variable PATH
os.environ["PATH"] = "C:\\Accelerad\\bin;" + \
    "C:\\Radiance\\bin;" + \
    "{}".format(os.environ["PATH"])
    
#Setting enviromental variable RAYPATH
os.environ["RAYPATH"] = ".;" + \
    "C:\\Accelerad\\lib;" + \
    "C:\\Radiance\\lib"


ab_list = [6, 8, 10, 12] # 4 different
ad_list = [1024, 4096, 16384, 65536, 262142] # 5 different
lw_power_list = [1, 1.5, 2, 2.5, 3] # 5 different
#4*5*5 = 100 options

no_sensor_points = 1
rfluxsky_file = r""
context_rad = r""
grids_files_list = []


for i in range(len(ab_list)):
    for j in range(len(ad_list)):
        for k in range(len(lw_power_list)):
            ab = ab_list[i]
            ad = ad_list[j]
            lw = 1/(ad**lw_power_list[k])
            
            
            cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                        "-y", f"{no_sensor_points}",
                        "-I", "-",
                        f"{rfluxsky_file}",
                        f"{context_rad}"]
            
            #Run 1
            output_filename = f"run1__ab_{ab}__ad_{ad}__"
            
            
            #Run 2

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