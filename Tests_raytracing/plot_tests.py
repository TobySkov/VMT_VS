
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot

path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_raytracing"
print(os.getcwd())
os.chdir(path)
print(os.getcwd())

#%%
#plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)


no_triangles_list = []
no_points_list = []
for i in range(5):
    for j in range(10):
        no_triangles_list.append(3500*4**i)
        no_points_list.append(4**(j+1))


no_triangles_list = np.array(no_triangles_list)
no_points_list = np.array(no_points_list)


#%% Read results
oconv_timing_list = []
read_stdin_timing_list = []
run_rfluxmtx_timing_list = []

for i in range(50):
    file = f"output\\Triangles_{no_triangles_list[i]}__Points_{no_points_list[i]}__timings.txt"
    with open(file, "r") as infile:
        oconv_timing = float(infile.readline().split(
            "oconv_timing [s]: ")[1])
        read_stdin_timing = float(infile.readline().split(
            "read_stdin_timing [s]: ")[1])
        run_rfluxmtx_timing = float(infile.readline().split(
            "run_rfluxmtx_timing [s]:")[1])

    oconv_timing_list.append(oconv_timing)
    read_stdin_timing_list.append(read_stdin_timing)
    run_rfluxmtx_timing_list.append(run_rfluxmtx_timing)


oconv_timing_list = np.array(oconv_timing_list)
read_stdin_timing_list = np.array(read_stdin_timing_list)
run_rfluxmtx_timing_list = np.array(run_rfluxmtx_timing_list)


#%% Plot oconv

data = (oconv_timing_list[0:10],
        oconv_timing_list[10:20],
        oconv_timing_list[20:30],
        oconv_timing_list[30:40],
        oconv_timing_list[40:50])
    
log_data = (np.log(oconv_timing_list[0:10]),
            np.log(oconv_timing_list[10:20]),
            np.log(oconv_timing_list[20:30]),
            np.log(oconv_timing_list[30:40]),
            np.log(oconv_timing_list[40:50]))



plt.figure(figsize=(6,3),dpi=500)
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Number of triangles in scene", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Oconv function calls benchmark", fontsize=14)
plt.boxplot(data,labels=["3500", "14000", "56000", "224000", "896000"])
plt.show()



plt.figure(figsize=(6,3),dpi=500)
plt.grid()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Number of triangles in scene", fontsize=12)
plt.ylabel("Natural logarithm of walltime [ln(s)]", fontsize=12)
plt.title("Oconv function calls benchmark", fontsize=14)
plt.boxplot(log_data,labels=["3500", "14000", "56000", "224000", "896000"])
plt.show()

#%% Plot read stdin

data = (read_stdin_timing_list[no_points_list == 4],
        read_stdin_timing_list[no_points_list == 16],
        read_stdin_timing_list[no_points_list == 64],
        read_stdin_timing_list[no_points_list == 256],
        read_stdin_timing_list[no_points_list == 1024],
        read_stdin_timing_list[no_points_list == 4096],
        read_stdin_timing_list[no_points_list == 16384],
        read_stdin_timing_list[no_points_list == 65536],
        read_stdin_timing_list[no_points_list == 262144],
        read_stdin_timing_list[no_points_list == 1048576])

log_data = (np.log(read_stdin_timing_list[no_points_list == 4]),
            np.log(read_stdin_timing_list[no_points_list == 16]),
            np.log(read_stdin_timing_list[no_points_list == 64]),
            np.log(read_stdin_timing_list[no_points_list == 256]),
            np.log(read_stdin_timing_list[no_points_list == 1024]),
            np.log(read_stdin_timing_list[no_points_list == 4096]),
            np.log(read_stdin_timing_list[no_points_list == 16384]),
            np.log(read_stdin_timing_list[no_points_list == 65536]),
            np.log(read_stdin_timing_list[no_points_list == 262144]),
            np.log(read_stdin_timing_list[no_points_list == 1048576]))


plt.figure(figsize=(6,3),dpi=500)
plt.grid()
plt.xticks(rotation = 70, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Number of sensor points in scene", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Read stdin function calls benchmark", fontsize=14)
plt.boxplot(data,labels=["4", "16", "64", "256", "1024", "4096",
                         "16384", "65536", "262144", "1048576"])
plt.show()



plt.figure(figsize=(6,3),dpi=500)
plt.grid()
plt.xticks(rotation = 70, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("Number of sensor points in scene", fontsize=12)
plt.ylabel("Natural logarithm of walltime [ln(s)]", fontsize=12)
plt.title("Read stdin function calls benchmark", fontsize=14)
plt.boxplot(log_data,labels=["4", "16", "64", "256", "1024", "4096",
                         "16384", "65536", "262144", "1048576"])
plt.show()


#%%



#%% 

data = np.zeros((5,10))
k = 0
for i in range(5):
    for j in range(10):
        data[i][j] = run_rfluxmtx_timing_list[k]
        k += 1
        

"""       
fig = go.Figure(data=[go.Surface(z=data, 
                                 x=[4**(j+1) for j in range(10)], 
                                 y=[3500*4**i for i in range(5)])])
plot(fig, auto_open=True)
"""

#%%
x = list(range(10))


plt.figure(figsize=(6,3),dpi=500)
plt.plot(x,run_rfluxmtx_timing_list[0:10], label = "3500 \u25b2")
plt.plot(x,run_rfluxmtx_timing_list[10:20], label = "14000 \u25b2")
plt.plot(x,run_rfluxmtx_timing_list[20:30], label = "56000 \u25b2")
plt.plot(x,run_rfluxmtx_timing_list[30:40], label = "224000 \u25b2")
plt.plot(x,run_rfluxmtx_timing_list[40:50], label = "896000 \u25b2")
plt.xlabel("Number of sensor points in scene", fontsize=12)
plt.ylabel("Walltime [s]", fontsize=12)
plt.title("Rfluxmtx function calls benchmark", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=["4", "16", "64", "256", "1024", "4096", "16384", "65536", "262144", "1048576"], rotation = 70, fontsize=12)
plt.show()


plt.figure(figsize=(6,3),dpi=500)
plt.plot(x,np.log(run_rfluxmtx_timing_list[0:10]), label = "3500 \u25b2")
plt.plot(x,np.log(run_rfluxmtx_timing_list[10:20]), label = "14000 \u25b2")
plt.plot(x,np.log(run_rfluxmtx_timing_list[20:30]), label = "56000 \u25b2")
plt.plot(x,np.log(run_rfluxmtx_timing_list[30:40]), label = "224000 \u25b2")
plt.plot(x,np.log(run_rfluxmtx_timing_list[40:50]), label = "896000 \u25b2")
plt.xlabel("Number of sensor points in scene", fontsize=12)
plt.ylabel("Natural logarithm of walltime [ln(s)]", fontsize=12)
plt.title("Rfluxmtx function calls benchmark", fontsize=14)
plt.grid()
plt.legend()
plt.xticks(x, labels=["4", "16", "64", "256", "1024", "4096", "16384", "65536", "262144", "1048576"], rotation = 70, fontsize=12)
plt.show()



#%%