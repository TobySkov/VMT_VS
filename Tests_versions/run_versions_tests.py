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
    above_300 = (data*179) >= 300 #179 lm/W; above 300 lux
    da = (((above_300).sum(axis=1))/above_300.shape[1])*100

    return da

#%%

def run_oconv(files_list, output_filename):

    cmd_list = [r"C:\\Radiance\\bin\\oconv.exe"] + files_list

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
    


#%% Run 2PM
"""
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


duration_2PM = run_rfluxmtx(cmd_list, grids_files_list, 
                        output_filename = "2PM\\2PM_output.dc")


two_pm_dc = read_text_matrix(path = "2PM\\2PM_output.dc") 
sky_matrix = read_text_matrix(path = "DNK_Copenhagen.061800_IWEC.smx")
two_pm_result_matrix = np.matmul(two_pm_dc,sky_matrix)
two_pm_da = calc_da_cpu(two_pm_result_matrix)


with open("2PM_da.pkl", "wb") as outfile:
    pickle.dump(two_pm_da.tolist(), outfile, protocol=2)


"""

#%% run 3PM

material = """
void glass Glass_rad_mat_daylight
0
0
3 0.882402016636 0.882402016636 0.882402016636

"""

#Perpare geometry
path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_versions\3PM\Raytracing\Daylight\Radiance\model\aperture\aperture.rad"
with open(path, "r") as infile:
    content = infile.readlines()

files_list = []
files_only = []
for i, line in enumerate(content):
    if "Glz" in line:
        glz_no = int(line.split("Glz")[1])
        face_no = int(line.split("Face")[1].split("_Glz")[0])
        path = f"3PM\\Raytracing\\Daylight\\Radiance\\model\\aperture\\face_{face_no}__glz_{glz_no}.rad"
        files_only.append("face_{face_no}__glz_{glz_no}.rad")
        files_list.append(path)
        with open(path, "w") as outfile:
            outfile.write(material)
            outfile.write("#@rfluxmtx h=kf u=Z\n")
            outfile.write(f"Glass_rad_mat_daylight polygon Face{face_no}_Glz{glz_no}\n")
            outfile.write(content[i+1])
            outfile.write(content[i+2])
            outfile.write(content[i+3])
    

#%%



path = "3PM\\Raytracing\\Daylight\\Radiance\\model\\aperture\\vmx_recievers.rad"
with open(path, "w") as outfile:
    for i in range(len(files_list)):
        vmx_file = files_list[i].replace(".rad",".vmx")
        outfile.write(f"#@rfluxmtx o={vmx_file}\n")
        outfile.write(f"!xform {files_list[i]}\n\n")
        
vmx_recievers_file = path



#%% Compute V-matrices

files_list = ["3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.mat",
         "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\envelope.rad",
         "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.mat",
         "3PM\\Raytracing\\Daylight\\Radiance\\model\\scene\\shades.rad"
         ]

run_oconv(files_list, output_filename = "3PM\\vmx_octree.oct")

grids_files_list = ["3PM\\Raytracing\\Daylight\\Radiance\\model\\grid\\Room_14.pts"]

cmd_list = ["C:\\Accelerad\\bin\\accelerad_rfluxmtx.exe",
                        "-y", "900",
                        "-ab", "6", "-ad", "65536", "-lw", f"{1/65536}",
                        "-I", "-",
                        f"{vmx_recievers_file}",
                        "-i", "3PM\\vmx_octree.oct"]


duration_3PM = run_rfluxmtx(cmd_list, grids_files_list, 
                        output_filename = False)
