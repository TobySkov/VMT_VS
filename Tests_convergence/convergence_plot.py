"""
Description: Plot of convergence testing 
"""
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objects as go
import pandas as pd
from plotly.offline import plot

#%%
ab_list = [6, 8, 10, 12] # 4 different
ad_list = [1024, 4096, 16384, 65536, 262142] # 5 different
lw_power_list = [1, 1.5, 2, 2.5, 3] # 5 different
#4*5*5 = 100 options

#%% Delete indicies
delete_idx = []
for i in range(438):
    if i%3!=0:
        delete_idx.append(i)
        
#%%
#Interesting parameters to calculate
#Average of all coefficients
#Maximum of all coefficients
#R2 between run 1 and 2
#Mean squared error
#root Mean squared error
#Runtime

mean_coef = np.zeros((100))
max_coef = np.zeros((100))

r2 = np.zeros((100))
mse = np.zeros((100))
rmse = np.zeros((100))

runtime = np.zeros((100))

#%%
ab_plot = np.zeros((100))
ad_plot = np.zeros((100))
lw_power_plot = np.zeros((100))

#%%
count = 0
for i in range(len(ab_list)):
    for j in range(len(ad_list)):
        for k in range(len(lw_power_list)):
            ab = ab_list[i]
            ad = ad_list[j]
            lw = 1/(ad**lw_power_list[k])
            
            ab_plot[count] = ab
            ad_plot[count] = ad
            lw_power_plot[count] = lw_power_list[k]
            
            #Run 1 name
            output_filename1 = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__run1.txt"
            
            #Run 2 name
            output_filename2 = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__run2.txt"

            #Loading data
            run1_ini = np.loadtxt(output_filename1, skiprows = 11)
            run1 = np.delete(run1_ini, delete_idx, axis=1)
            
            run2_ini = np.loadtxt(output_filename2, skiprows = 11)
            run2 = np.delete(run2_ini, delete_idx, axis=1)
            
            
            combined = np.concatenate((run1, run2), axis = 1)
            
            #Calculating metrics
            mean_coef[count] = np.mean(combined)
            max_coef[count] = np.max(combined)            
            
            r2[count] = r2_score(run1, run2)
            mse[count] = mean_squared_error(run1, run2)
            rmse[count] = np.sqrt(mse[count])
            
            #Read timings
            timing_filename = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[k]}__timings.txt"
            with open(timing_filename, "r") as infile:
                line_ini = infile.readline()
                time1 = float(line_ini.split("Wall time, run1: ")[1].split(" [s]")[0])
                line_ini = infile.readline()
                time2 = float(line_ini.split("Wall time, run2: ")[1].split(" [s]")[0])
            
                runtime[count] = (time1 + time2)/2
            
            
            print(f"Round: {count + 1}/100")
            count += 1


#%% Convert data structure to matrices

results = {}
count = 0
for i in range(len(ab_list)):
    
    r2_matrix = np.zeros((5,5))
    runtime_matrix = np.zeros((5,5))
    
    for j in range(len(ad_list)):
        for k in range(len(lw_power_list)):
            r2_matrix[j][k] = r2[count]
            runtime_matrix[j][k] = runtime[count]
            count += 1
            

    results[f"ab_{ab_list[i]}__r2_matrix"] = r2_matrix
    results[f"ab_{ab_list[i]}__runtime_matrix"] = runtime_matrix







#%%
#Visualize results

color = np.ones((5,5))


fig = go.Figure(data=[go.Surface(z=np.log(results["ab_6__r2_matrix"]), 
                                 x=lw_power_list, 
                                 y=ad_list),
                      go.Surface(z=np.log(results["ab_8__r2_matrix"]), 
                                 x=lw_power_list, 
                                 y=ad_list),
                      go.Surface(z=np.log(results["ab_10__r2_matrix"]), 
                                 x=lw_power_list, 
                                 y=ad_list),
                      go.Surface(z=np.log(results["ab_12__r2_matrix"]), 
                                 x=lw_power_list, 
                                 y=ad_list)])
"""
fig = go.Figure(data=[go.Surface(z=results["ab_6__r2_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 surfacecolor = color),
                      go.Surface(z=results["ab_8__r2_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 surfacecolor = color*2),
                      go.Surface(z=results["ab_10__r2_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 surfacecolor = color*3),
                      go.Surface(z=results["ab_12__r2_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 surfacecolor = color*4)])
"""
#fig.update_layout(title='Mt Bruno Elevation', autosize=False,
#                  width=500, height=500,
#                  margin=dict(l=65, r=50, b=65, t=90))
plot(fig, auto_open=True)


#%%
#https://stackoverflow.com/questions/53992606/plotly-different-color-surfaces



colorscale = [[0.1,"blue"], [0.4,"black"], [0.6,"green"] ,[0.9,"red"]]

fig = go.Figure(data=[go.Surface(z=results["ab_6__runtime_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 cmin = 0,
                                 cmax = 1,
                                 surfacecolor = color*0.1,
                                 showscale = False,
                                 colorscale = colorscale),
                      go.Surface(z=results["ab_8__runtime_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 cmin = 0,
                                 cmax = 1,
                                 surfacecolor = color*0.4,
                                 showscale = False,
                                 colorscale = colorscale),
                      go.Surface(z=results["ab_10__runtime_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 cmin = 0,
                                 cmax = 1,
                                 surfacecolor = color*0.6,
                                 showscale = False,
                                 colorscale = colorscale),
                      go.Surface(z=results["ab_12__runtime_matrix"], 
                                 x=lw_power_list, 
                                 y=ad_list,
                                 cmin = 0,
                                 cmax = 1,
                                 surfacecolor = color*0.9,
                                 showscale = False,
                                 colorscale = colorscale)])

plot(fig, auto_open=True)


#%%

np.sum(runtime)*2/3600




#%%
ab_list = [6,6,6,12] 
ad_list = [16384, 65536, 262142,262142] 
lw_power_list = [1,1,1,3] 
#4*5*5 = 100 options


for i in range(4):

    ab = ab_list[i]
    ad = ad_list[i]
    lw = 1/(ad**lw_power_list[i])
    

    #Run 1 name
    output_filename1 = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[i]}__run1.txt"
    
    #Run 2 name
    output_filename2 = f"output\\run1__ab_{ab}__ad_{ad}__lwpower_{lw_power_list[i]}__run2.txt"


    #Loading data
    run1_ini = np.loadtxt(output_filename1, skiprows = 11)
    run1 = np.delete(run1_ini, delete_idx, axis=1)
    
    run2_ini = np.loadtxt(output_filename2, skiprows = 11)
    run2 = np.delete(run2_ini, delete_idx, axis=1)

    r2 = r2_score(run1, run2)
    
    plt.figure()
    plt.plot(run1,run2,"o")
    plt.plot([0,0.032],[0,0.032],c="black")
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("Run 1, daylight coefficients", fontsize=12)
    plt.ylabel("Run 2, daylight coefficients", fontsize=12)
    plt.title(f"-ab {ab}, ad {ad}, lw power {lw_power_list[i]}. R2 = {r2:.6f}", fontsize=14)
    plt.show
            
            
            