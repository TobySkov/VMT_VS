# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from subprocess import Popen, PIPE
import time

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_raytracing"
print(os.getcwd())
os.chdir(path)
print(os.getcwd())

#%%

#Setting enviromental variable PATH
os.environ["PATH"] = "C:\\Accelerad\\bin;" + \
    "C:\\Radiance\\bin;" + \
    "{}".format(os.environ["PATH"])
    
#Setting enviromental variable RAYPATH
os.environ["RAYPATH"] = ".;" + \
    "C:\\Accelerad\\lib;" + \
    "C:\\Radiance\\lib"
    
rfluxsky_file = "rfluxsky.rad"
#%%
def run_oconv(no_triangles, no_points):

    cmd_list = [r"C:\\Radiance\\bin\\oconv.exe",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\aperture\\aperture.mat",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\aperture\\aperture.rad",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\scene\\envelope.mat",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\scene\\envelope.rad",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\scene\\shades.mat",
                f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\\model\\scene\\shades.rad"
                ]
    
    
    output_filename = f"output\\Triangles_{no_triangles}__Points_{no_points}__geo.oct"
    

    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"This is stdin")
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    print("START - Writing ASCII data")
    with open(output_filename, "wb") as outfile:
        outfile.write(output)
    print("DONE  - Writing ASCII data")
    
    return output_filename

#%%

def run_rfluxmtx(cmd_list, stdin_bytes, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(stdin_bytes)
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

no_triangles_list = []
no_points_list = []
for i in range(5):
    for j in range(10):
        no_triangles_list.append(3500*4**i)
        no_points_list.append(4**(j+1))
    

#%%        

for i in range(48,50,1):
    no_triangles = no_triangles_list[i]
    no_points = no_points_list[i]
    
    #Find gridfile
    input_files_list = []
    grid_files_folder = f"Triangles_{no_triangles}__Points_{no_points}\\Radiance\model\grid"
    for file in os.listdir(grid_files_folder):
        if ".pts" in file:
            input_files_list.append(grid_files_folder + "\\" + file)
        
    #Run oconv
    start = time.time()
    current_oconv_file = run_oconv(no_triangles, no_points)
    end = time.time()
    oconv_timing = end-start
    
    #Run read gridfiles
    start = time.time()
    stdin_bytes = read_stdin(input_files_list)
    end = time.time()
    read_stdin_timing = end-start
    
    #Run rfluxmtx
    cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                        "-y", f"{no_points}",
                        "-ab", "6", "-ad", "65536", "-lw", f"{1/65536}",
                        "-I", "-",
                        f"{rfluxsky_file}",
                        "-i", f"{current_oconv_file}"]
    
    output_filename = f"output\\\\Triangles_{no_triangles}__Points_{no_points}__output.dc"
    start = time.time()
    run_rfluxmtx(cmd_list, stdin_bytes, output_filename)
    end = time.time()
    run_rfluxmtx_timing = end-start
    
    #Save timings
    path = f"output\\Triangles_{no_triangles}__Points_{no_points}__timings.txt"
    with open(path, "w") as outfile:
        outfile.write(f"oconv_timing [s]: {oconv_timing}\n")
        outfile.write(f"read_stdin_timing [s]: {read_stdin_timing}\n")
        outfile.write(f"run_rfluxmtx_timing [s]: {run_rfluxmtx_timing}\n")