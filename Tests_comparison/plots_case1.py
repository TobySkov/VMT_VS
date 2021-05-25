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

def r2_plot(data_EP, data_ISO, title, filename):

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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case1"
    plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()


#%%
def plot_annual_data(data, title, filename):
    
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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case1"
    plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
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
        filename = f"Face {i}, Heat Storage Rate"
        plot_annual_data(output, title, filename)
        results[title] = output
        
    for i in range(6):
        file = openstudio_folder + f"\\ROOM_3_69A20C51..FACE{i}__Surface Outside Face Conduction Heat Transfer Rate.pkl"
        with open(file, 'rb') as pkl_file:
            output = -np.array(pickle.load(pkl_file))
        title = f"Face {i}, Outside Face Conduction Heat Transfer Rate [W]"
        filename = f"Face {i}, Outside Face Conduction Heat Transfer Rate"
        plot_annual_data(output, title, filename)
        results[title] = output
        
        
    for i in range(6):
        file = openstudio_folder + f"\\ROOM_3_69A20C51..FACE{i}__Surface Inside Face Conduction Heat Transfer Rate.pkl"
        with open(file, 'rb') as pkl_file:
            output = np.array(pickle.load(pkl_file))
        title = f"Face {i}, Inside Face Conduction Heat Transfer Rate [W]"
        filename = f"Face {i}, Inside Face Conduction Heat Transfer Rate"
        plot_annual_data(output, title, filename)
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
    filename = "EnergyPlus, total inside conduction heat transfer rate"
    plot_annual_data(EP_sum_inside_transfer, title, filename)
    
    return EP_sum_inside_transfer


#%%

results = load_and_plot()
EP_sum_inside_transfer = calc_sum_internal_transfer_EP(results)

#plot_annual_data(EP_sum_inside_transfer, title = "EP, check", filename = "delete")

#%%

#comparing H_tr_ms
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__walls_HC_ms.pkl"
with open(file, 'rb') as pkl_file:
    iso_sum_inside_transfer = 1000*np.array(pickle.load(pkl_file))
title = "ISO13790, total inside conduction heat transfer rate [W]"
filename = "ISO13790, total inside conduction heat transfer rate"
plot_annual_data(iso_sum_inside_transfer, title, filename)

title = "Difference, total inside conduction heat transfer rate [W]"
filename = "Difference, total inside conduction heat transfer rate"
plot_annual_data(EP_sum_inside_transfer - iso_sum_inside_transfer, title, filename)


r2_plot(data_EP = EP_sum_inside_transfer, 
        data_ISO = iso_sum_inside_transfer, 
        title = "Total inside conduction heat transfer rate [W]",
        filename = "Total inside conduction heat transfer rate")

#%%

#comparing heating
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\heating.pkl"
with open(file, 'rb') as pkl_file:
    EP_heating = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__h_load_hourly.pkl"
with open(file, 'rb') as pkl_file:
    iso_heating = 1000*np.array(pickle.load(pkl_file))

title = "EP, heating load [W]"
filename = "EP, heating load"
plot_annual_data(EP_heating, title, filename)

title = "ISO13790, heating load [W]"
filename = "ISO13790, heating load"
plot_annual_data(iso_heating, title, filename)

title = "Difference, heating load [W]"
filename = "Difference, heating load"
plot_annual_data(EP_heating - iso_heating, title, filename)


r2_plot(data_EP = EP_heating, 
        data_ISO = iso_heating, 
        title = "Heating load [W]", 
        filename = "Heating load")




#%%

#comparing infiltration
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\infiltration_load.pkl"
with open(file, 'rb') as pkl_file:
    EP_infil = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__infil_HC.pkl"
with open(file, 'rb') as pkl_file:
    iso_infil = 1000*np.array(pickle.load(pkl_file))

title = "EP, infiltration load [W]"
filename = "EP, infiltration load"
plot_annual_data(EP_infil, title, filename)

title = "ISO13790, infiltration load [W]"
filename = "ISO13790, infiltration load"
plot_annual_data(iso_infil, title, filename)

title = "Difference, infiltration load [W]"
filename = "Difference, infiltration load"
plot_annual_data(EP_infil - iso_infil, title, filename)


r2_plot(data_EP = EP_infil, 
        data_ISO = iso_infil, 
        title = "Infiltration load [W]",
        filename = "Infiltration load")


#%%

diff_eq_iso = iso_sum_inside_transfer + iso_infil + iso_heating
title = "ISO, balance [W]"
filename = "ISO, balance"
plot_annual_data(diff_eq_iso , title, filename)

np.min(diff_eq_iso)
np.max(diff_eq_iso)
np.mean(diff_eq_iso)
np.std(diff_eq_iso)

diff_eq_ep = EP_sum_inside_transfer + EP_infil + EP_heating
title = "EP, balance [W]"
filename = "EP, balance"
plot_annual_data(diff_eq_ep , title, filename)

np.min(diff_eq_ep)
np.max(diff_eq_ep)
np.mean(diff_eq_ep)
np.std(diff_eq_ep)

#%%
#comparing air temp
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\air_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_air = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__theta__air.pkl"
with open(file, 'rb') as pkl_file:
    iso_air = np.array(pickle.load(pkl_file))

title = "EP, air temperature [C]"
filename = "EP, air temperature"
plot_annual_data(EP_air, title, filename)

title = "ISO13790, air temperature [C]"
filename = "ISO13790, air temperature"
plot_annual_data(iso_air, title, filename)

title = "Difference, air temperature [C]"
filename = "Difference, air temperature"
plot_annual_data(EP_air - iso_air, title, filename)


r2_plot(data_EP = EP_air, 
        data_ISO = iso_air, 
        title = "Air temperature [C]", 
        filename = "Air temperature")



#%%
#comparing op temp
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case1\oper_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_op = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case1\output\ISO13790\Room_3_69a20c51__theta__op.pkl"
with open(file, 'rb') as pkl_file:
    iso_op = np.array(pickle.load(pkl_file))

title = "EP, operative temperature [C]"
filename = "EP, operative temperature"
plot_annual_data(EP_op, title, filename)

title = "ISO13790, operative temperature [C]"
filename = "ISO13790, operative temperature"
plot_annual_data(iso_op, title, filename)

title = "Difference, operative temperature [C]"
filename = "Difference, operative temperature"
plot_annual_data(EP_op - iso_op, title, filename)


r2_plot(data_EP = EP_op, 
        data_ISO = iso_op, 
        title = "Operative temperature [C]", 
        filename = "Operative temperature")


