"""
Description: gendaymtx, text readers and sDA calculation

"""

import os
from subprocess import Popen, PIPE
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import time
import numpy as np
import pickle
#%%
wea_file_path = "C:\\Users\\Pedersen_Admin\\OneDrive - Perkins and Will\\Documents\\GitHub\\VMT_VS\\Tests_convergence\\DNK_Copenhagen.061800_IWEC.wea"
output_filename = "C:\\Users\\Pedersen_Admin\\OneDrive - Perkins and Will\\Documents\\GitHub\\VMT_VS\\Tests_convergence\\DNK_Copenhagen.061800_IWEC.smx"

#%%

#Setting enviromental variable PATH
os.environ["PATH"] = "C:\\Accelerad\\bin;" + \
    "C:\\Radiance\\bin;" + \
    "{}".format(os.environ["PATH"])
    
#Setting enviromental variable RAYPATH
os.environ["RAYPATH"] = ".;" + \
    "C:\\Accelerad\\lib;" + \
    "C:\\Radiance\\lib"
    

#%%

#gendaymtx

###Prepare cmd list
cmd_list = ["c:\\Radiance\\bin\\gendaymtx"]

cmd_list.extend(["-O0",
                 "-m", "1",
                 "-r", "0.0",
                 "-c", "1", "1", "1",
                 wea_file_path])


print("START - Subprocess: {}".format(cmd_list[0]))
p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"this is stdin")
rc = p.returncode
if rc != 0:
    print(f"Error code: \n {err}")
print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))

print("START - Writing ASCII data")
with open(output_filename, "wb") as outfile:
    outfile.write(output)
print("DONE  - Writing ASCII data")

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


#%% read dc matrices

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\output\run1__ab_6__ad_16384__lwpower_1__run1.txt"
prospect1_dc = read_text_matrix(path) 

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\output\run1__ab_6__ad_65536__lwpower_1__run1.txt"
prospect2_dc = read_text_matrix(path)

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\output\run1__ab_6__ad_262142__lwpower_1__run1.txt"
prospect3_dc = read_text_matrix(path)

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\output\run1__ab_12__ad_262142__lwpower_3__run1.txt"
max_res_dc = read_text_matrix(path)


#%%
path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\DNK_Copenhagen.061800_IWEC.smx"
sky_matrix = read_text_matrix(path)

#%%

prospect1_result_matrix = np.matmul(prospect1_dc,sky_matrix)
prospect2_result_matrix = np.matmul(prospect2_dc,sky_matrix)
prospect3_result_matrix = np.matmul(prospect3_dc,sky_matrix)
max_res_result_matrix = np.matmul(max_res_dc,sky_matrix)

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

prospect1_da = calc_da_cpu(prospect1_result_matrix)
prospect2_da = calc_da_cpu(prospect2_result_matrix)
prospect3_da = calc_da_cpu(prospect3_result_matrix)
max_res_da = calc_da_cpu(max_res_result_matrix)

#%%
r2 = r2_score(max_res_da, prospect1_da)
    
plt.figure()
plt.plot(max_res_da,prospect1_da,"o")
plt.plot([87,93.6],[87,93.6],c="black")
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Max resolution, daylight autonomy", fontsize=12)
plt.ylabel("Prospect 1, daylight autonomy", fontsize=12)
plt.title(f"Daylight autonomy. R2 = {r2:.6f}", fontsize=14)
plt.show

#%%
r2 = r2_score(max_res_da, prospect2_da)
    
plt.figure()
plt.plot(max_res_da,prospect2_da,"o")
plt.plot([87,93.6],[87,93.6],c="black")
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Max resolution, daylight autonomy", fontsize=12)
plt.ylabel("Prospect 2, daylight autonomy", fontsize=12)
plt.title(f"Daylight autonomy. R2 = {r2:.6f}", fontsize=14)
plt.show

#%%
r2 = r2_score(max_res_da, prospect3_da)
    
plt.figure()
plt.plot(max_res_da,prospect3_da,"o")
plt.plot([87,93.6],[87,93.6],c="black")
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Max resolution, daylight autonomy", fontsize=12)
plt.ylabel("Prospect 3, daylight autonomy", fontsize=12)
plt.title(f"Daylight autonomy. R2 = {r2:.6f}", fontsize=14)
plt.show


#%%
path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\prospect2_da.pkl"
with open(path, 'wb') as outfile:
    pickle.dump(prospect2_da.tolist(), outfile, protocol=2) #Protocol 2 needed for GHpython to read it





