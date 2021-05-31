"""
Description:

"""

import os
from subprocess import Popen, PIPE
import time
import numpy as np
import pickle

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_versions"
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

def run_rfluxmtx(cmd_list, grids_files_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start
    
#%%

def run_rfluxmtx_dmx(cmd_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"this is stdin")
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start

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

#%%

def run_dctimestep(cmd_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start

#%%

def run_rmtxop(cmd_list, output_filename):
    
    print("START - Subprocess: {}".format(cmd_list[0]))
    start = time.time()
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(read_stdin(grids_files_list))
    end = time.time()
    rc = p.returncode
    if rc != 0:
        print(f"Error code: \n {err}")
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    if output_filename:
        print("START - Writing ASCII data")
        with open(output_filename, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
    
    return end-start

#%%

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


def calc_da_cpu(result_matrix):

    occ_sch = gen_occ_sch()
    sch_idx = occ_sch == 1

    #Calculate DA on all
    data = result_matrix[:,sch_idx]
    above_300 = (data) >= 300 #179 lm/W; above 300 lux
    da = (((above_300).sum(axis=1))/above_300.shape[1])*100

    return da




#%% Run 2PM

grids_files_list = ["2PM\\Raytracing\\Daylight\\Radiance\\model\\grid\\Room_14.pts"]

cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                        "-y", "900",
                        "-ab", "6", "-ad", "65536", "-lw", f"{1/65536}",
                        "-I", "-",
                        f"{rfluxsky_file}"]

cmd_list = cmd_list +\
        ["2PM\\Raytracing\\Daylight\\Radiance\\model\\aperture\\aperture.mat",
         "2PM\\Raytracing\\Daylight\\Radiance\\model\\aperture\\aperture.rad",
         "2PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.mat",
         "2PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.rad",
         "2PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.mat",
         "2PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.rad"
         ]


duration_2PM_rfluxmtx = run_rfluxmtx(cmd_list, grids_files_list, 
                        output_filename = "2PM\\2PM_output.dc")

cmd_list_dctimestep = ["C:\\Radiance\\bin\\dctimestep",
                       "2PM\\2PM_output.dc",
                       "DNK_Copenhagen.061800_IWEC.smx"] 

duration_2PM_dctimestep = run_dctimestep(cmd_list_dctimestep, 
                                         output_filename = "2PM\\output.rgb")


cmd_list_rmtxop = ["C:\\Radiance\\bin\\rmtxop",
                   "-c", "47.435", "119.93", "11.635", "-fa",
                   "2PM\\output.rgb"]

duration_2PM_rmtxop = run_rmtxop(cmd_list_rmtxop, 
                                 output_filename = "2PM\\output.ill")


#Save timings
with open("2PM\\timings_2PM.txt", "w") as outfile:
    outfile.write(f"rfluxmtx wall time: {duration_2PM_rfluxmtx} [s]\n")
    outfile.write(f"dctimestep wall time: {duration_2PM_dctimestep} [s]\n")
    outfile.write(f"rmtxop wall time: {duration_2PM_rmtxop} [s]\n")

    
#Matrix multiplication in numpy:
#two_pm_dc = read_text_matrix(path = "2PM\\2PM_output.dc") 
#sky_matrix = read_text_matrix(path = "DNK_Copenhagen.061800_IWEC.smx")
#two_pm_result_matrix = np.matmul(two_pm_dc,sky_matrix)
#two_pm_da = calc_da_cpu(two_pm_result_matrix)

#%% 2PM 
#Calculate and save DA
two_pm_result_matrix = read_text_matrix(path = "2PM\\output.ill")
two_pm_da = calc_da_cpu(two_pm_result_matrix)

with open("2PM_da.pkl", "wb") as outfile:
    pickle.dump(two_pm_da.tolist(), outfile, protocol=2)



#%%  3PM

material_glow = """
#@rfluxmtx h=kf u=Z
void glow glow_mat
0
0
4 1 1 1 0

"""

material_black = """
void plastic black_mat
0
0
5 0.0 0.0 0.0 0.0 0.0

"""

#Perpare geometry
path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_versions\3PM\Raytracing\Daylight\Radiance\model\aperture\aperture.rad"
with open(path, "r") as infile:
    content = infile.readlines()

files_list = []
files_only = []
for i in range(24): #24 windows total
    current_window_start_line = i * 5
    vmx_window = material_glow
    other_windows = material_black
    for j, line in enumerate(content):
        if j == current_window_start_line:
            vmx_window += line.replace("replace_mat", "glow_mat")
            vmx_window += content[j+1]
            vmx_window += content[j+2]
            vmx_window += content[j+3]
            vmx_window += "\n"
            
        elif "polygon" in line:
            other_windows += line.replace("replace_mat", "black_mat")
            other_windows += content[j+1]
            other_windows += content[j+2]
            other_windows += content[j+3]
            other_windows += "\n"
            
    try:
        os.makedirs(f"3PM//simulation_{i}")
    except:
        pass
    
    with open(f"3PM//simulation_{i}//window.rad", "w") as outfile:
        outfile.write(vmx_window)
        
    with open(f"3PM//simulation_{i}//other_windows.rad", "w") as outfile:
        outfile.write(other_windows)
        
        
        
        
#%% Compute V matrices

walltime_3PM_vmx_list = []

grids_files_list = ["3PM\\Raytracing\\Daylight\\Radiance\\model\\grid\\Room_14.pts"]

for i in range(24): #24 windows total
    cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                "-y", "900",
                "-ab", "6", "-ad", "65536", "-lw", f"{1/65536}",
                "-I", "-",
                f"3PM//simulation_{i}//window.rad", #Reciever
                f"3PM//simulation_{i}//other_windows.rad", #Scene
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.mat", #Scene
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.rad"] #Scene
        

    duration_3PM = run_rfluxmtx(cmd_list, grids_files_list,
                                output_filename = f"3PM\\simulation_{i}\\vmx.mtx")
    
    walltime_3PM_vmx_list.append(duration_3PM)

    print(f"{i+1}/24")
    

#%% Compute D matrices

walltime_3PM_dmx_list = []


for i in range(24): #24 windows total
    cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                "-ab", "6", "-ad", "65536", "-lw", f"{1/65536}",
                f"3PM//simulation_{i}//window.rad", #Sender
                "rfluxsky.rad", #Reciever
                f"3PM//simulation_{i}//other_windows.rad", #Scene
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.mat", #Scene
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.rad",
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.mat",
                "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.rad"] #Scene
        

    duration_3PM = run_rfluxmtx_dmx(cmd_list, 
                                    output_filename = f"3PM\\simulation_{i}\\dmx.mtx")

    
    walltime_3PM_dmx_list.append(duration_3PM)

    print(f"{i+1}/24")
    
#%% dctimestep and rmtxop

walltime_3PM_dctimestep_list = []
walltime_3PM_rmtxop_list = []

for i in range(24): #24 windows total
    cmd_list = ["C:\\Radiance\\bin\\dctimestep",
                f"3PM\\simulation_{i}\\vmx.mtx",
                "00002.xml",
                f"3PM\\simulation_{i}\\dmx.mtx",
                "DNK_Copenhagen.061800_IWEC.smx"] 

    duration_3PM = run_dctimestep(cmd_list, output_filename = f"3PM\\simulation_{i}\\output.rgb")
    walltime_3PM_dctimestep_list.append(duration_3PM)
    
    cmd_list = ["C:\\Radiance\\bin\\rmtxop",
                "-c", "47.435", "119.93", "11.635", "-fa",
                f"3PM\\simulation_{i}\\output.rgb"]
    
    duration_3PM = run_rmtxop(cmd_list, output_filename = f"3PM\\simulation_{i}\\output.ill")
    walltime_3PM_rmtxop_list.append(duration_3PM)
    

#Save 3PM timings
#%%
with open("3PM\\timings_3PM.txt", "w") as outfile:
    for i in range(24):
        string = f"{walltime_3PM_vmx_list[i]},\t{walltime_3PM_dmx_list[i]},\t" +\
            f"{walltime_3PM_dctimestep_list[i]},\t{walltime_3PM_rmtxop_list[i]}\n"
        outfile.write(string)

#%% Compute DA

cumm_result_3PM = np.zeros((900,8760))

for i in range(24):
    current_ill = read_text_matrix(path = f"3PM\\simulation_{i}\\output.ill")
    
    with open(f"3PM\\simulation_{i}\\da.pkl", "wb") as outfile:
        pickle.dump(calc_da_cpu(current_ill).tolist(), outfile, protocol=2)
        
    cumm_result_3PM += current_ill
    print(f"{i+1}/24")
    
three_pm_da = calc_da_cpu(cumm_result_3PM)

#%%
with open("3PM_da.pkl", "wb") as outfile:
    pickle.dump(three_pm_da.tolist(), outfile, protocol=2)