"""
Description:

"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

#%%
#FACE0 = South
#FACE1 = East
#FACE2 = North
#FACE3 = West

#%%

def r2_plot(data_EP, data_ISO, title):

    both_data = np.concatenate((data_EP, data_ISO))
    min_val = np.min(both_data)
    max_val = np.max(both_data)
    
    r2 = r2_score(data_EP, data_ISO)
    
    plt.figure(figsize=(6,3),dpi=500)
    plt.plot(data_EP, data_ISO,"o")
    plt.plot([min_val, max_val],[min_val, max_val],c="black")
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("EnergyPlus", fontsize=12)
    plt.ylabel("ISO13790", fontsize=12)
    plt.title(f"{title}. R2 = {r2:.6f}", fontsize=14)
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\plots"
    plt.savefig(path + "\\" + title.replace(" [W]",".png"), dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()


#%%
def plot_annual_data(data, title):
    
    data_2d = np.zeros((24,365))
    k = 0
    for i in range(365):
        for j in range(24):
            data_2d[j][i] = data[k]
            k+=1
    
    plt.figure(dpi=500)
    plt.imshow(data_2d, aspect = 5, cmap= "rainbow")
    plt.colorbar(shrink=0.4)
    plt.title(title)
    plt.xlabel("Days in year")
    plt.ylabel("Hours in day")
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\plots"
    plt.savefig(path + "\\" + title.replace(" [W]",".png"), dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()
    



#%%
def load_and_plot():
    openstudio_folder = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1"
    results = {}
    
    for i in range(6):
        file = openstudio_folder + f"\\ROOM_3_69A20C51..FACE{i}__Surface Heat Storage Rate.pkl"
        with open(file, 'rb') as pkl_file:
            output = np.array(pickle.load(pkl_file))
        title = f"Face {i}, Heat Storage Rate [W]"
        #plot_annual_data(output, title)
        results[title] = output
        
    for i in range(6):
        file = openstudio_folder + f"\\ROOM_3_69A20C51..FACE{i}__Surface Outside Face Conduction Heat Transfer Rate.pkl"
        with open(file, 'rb') as pkl_file:
            output = -np.array(pickle.load(pkl_file))
        title = f"Face {i}, Outside Face Conduction Heat Transfer Rate [W]"
        #plot_annual_data(output, title)
        results[title] = output
        
        
    for i in range(6):
        file = openstudio_folder + f"\\ROOM_3_69A20C51..FACE{i}__Surface Inside Face Conduction Heat Transfer Rate.pkl"
        with open(file, 'rb') as pkl_file:
            output = np.array(pickle.load(pkl_file))
        title = f"Face {i}, Inside Face Conduction Heat Transfer Rate [W]"
        #plot_annual_data(output, title)
        results[title] = output
        
    
    
    return results

#%%


#%%


def calc_sum_internal_transfer_EP(results):
    
    EP_sum_inside_transfer = np.zeros((8760))
    
    for i in range(6):

        title = f"Face {i}, Inside Face Conduction Heat Transfer Rate [W]"

        EP_sum_inside_transfer += results[title] 

    title = "EnergyPlus, total inside conduction heat transfer rate [W]"
    plot_annual_data(EP_sum_inside_transfer, title)
    
    return EP_sum_inside_transfer


#%%

results = load_and_plot()
EP_sum_inside_transfer = calc_sum_internal_transfer_EP(results)



#%%

#comparing H_tr_ms
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__walls_HC_ms.pkl"
with open(file, 'rb') as pkl_file:
    iso_sum_inside_transfer = 1000*np.array(pickle.load(pkl_file))
title = "ISO13790, total inside conduction heat transfer rate [W]"
plot_annual_data(iso_sum_inside_transfer, title)

title = "Difference, total inside conduction heat transfer rate [W]"
plot_annual_data(EP_sum_inside_transfer - iso_sum_inside_transfer, title)


r2_plot(data_EP = EP_sum_inside_transfer, 
        data_ISO = iso_sum_inside_transfer, 
        title = "Total inside conduction heat transfer rate [W]")

#%%

#comparing heating
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\heating.pkl"
with open(file, 'rb') as pkl_file:
    EP_heating = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__h_load_hourly.pkl"
with open(file, 'rb') as pkl_file:
    iso_heating = 1000*np.array(pickle.load(pkl_file))

title = "EP, heating load [W]"
plot_annual_data(EP_heating, title)

title = "ISO13790, heating load [W]"
plot_annual_data(iso_heating, title)

title = "Difference, heating load [W]"
plot_annual_data(EP_heating - iso_heating, title)


r2_plot(data_EP = EP_heating, 
        data_ISO = iso_heating, 
        title = "Heating load [W]")




#%%

#comparing heating
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\infiltration_load.pkl"
with open(file, 'rb') as pkl_file:
    EP_infil = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__infil_HC.pkl"
with open(file, 'rb') as pkl_file:
    iso_infil = 1000*np.array(pickle.load(pkl_file))

title = "EP, infiltration load [W]"
plot_annual_data(EP_infil, title)

title = "ISO13790, infiltration load [W]"
plot_annual_data(iso_infil, title)

title = "Difference, infiltration load [W]"
plot_annual_data(EP_infil - iso_infil, title)


r2_plot(data_EP = EP_infil, 
        data_ISO = iso_infil, 
        title = "Infiltration load [W]")


#%%

diff_eq_iso = iso_sum_inside_transfer + iso_infil + iso_heating
title = "ISO, control"
plot_annual_data(diff_eq_iso , title)

diff_eq_ep = EP_sum_inside_transfer + EP_infil + EP_heating
title = "EP, control"
plot_annual_data(diff_eq_ep , title)

#%%
#comparing air temp


#%%
#comparing op temp


