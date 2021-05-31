"""
Description:

"""

import numpy as np
import matplotlib.pyplot as plt

#%% Reading 2PM timings

path = "2PM\\timings_2PM.txt"
with open(path, "r") as infile:
    content = infile.readlines()

timings_2PM = []
timings_2PM.append(float(content[0].replace("rfluxmtx wall time: ","").replace(" [s]\n","")))
timings_2PM.append(float(content[1].replace("dctimestep wall time: ","").replace(" [s]\n","")))
timings_2PM.append(float(content[2].replace("rmtxop wall time: ","").replace(" [s]\n","")))

timings_2PM = np.array(timings_2PM)

#%%

path = "3PM\\timings_3PM.txt"
with open(path, "r") as infile:
    content = infile.readlines()
    
timings_3PM = []
for i in range(len(content)):
    list_ini = content[i].split(",\t")
    list_float = []
    for number in list_ini:
        list_float.append(float(number))
        
    timings_3PM.append(list_float)

timings_3PM = np.array(timings_3PM)

#%%


timings_2PM.flatten().sum()
timings_3PM.flatten().sum()

timings_3PM.sum(axis=0)

#%%
path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_versions\2PM"


#%%

plt.figure(figsize=(6,3),dpi=500)
plt.plot(timings_3PM[:,0], label = "rfluxmtx, vmx")
plt.plot(timings_3PM[:,2], label = "dctimestep")
plt.plot(timings_3PM[:,3], label = "rmtxop")
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Window index", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.legend()
plt.title("Three phase method timings", fontsize=14)
plt.savefig(path + "\\" + "version_timing1.png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
plt.show()


#%%
plt.figure(figsize=(6,3),dpi=500)
plt.plot(timings_3PM[:,0], label = "rfluxmtx, vmx")
plt.plot(timings_3PM[:,1], label = "rfluxmtx, dmx")
plt.plot(timings_3PM[:,2], label = "dctimestep")
plt.plot(timings_3PM[:,3], label = "rmtxop")
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Window index", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.legend()
plt.title("Three phase method timings", fontsize=14)
plt.savefig(path + "\\" + "version_timing2.png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
plt.show()