"""
Description:

"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score



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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case2"
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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case2"
    plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()
    

#%%
#comparing venilation load
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case2\ventilation_load.pkl"
with open(file, 'rb') as pkl_file:
    EP_ventilation = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case2\output\ISO13790\Room_1_d90d03ed__venti_HC.pkl"
with open(file, 'rb') as pkl_file:
    iso_ventilation = 1000*np.array(pickle.load(pkl_file))

title = "EP, ventilation load [W]"
filename = "EP, ventilation load"
plot_annual_data(EP_ventilation, title, filename)

title = "ISO13790, ventilation load [W]"
filename = "ISO13790, ventilation load"
plot_annual_data(iso_ventilation, title, filename)

title = "Difference, ventilation load [W]"
filename = "Difference, ventilation load"
plot_annual_data(EP_ventilation - iso_ventilation, title, filename)


r2_plot(data_EP = EP_ventilation, 
        data_ISO = iso_ventilation, 
        title = "Ventilation load [W]", 
        filename = "Ventilation load")


#%%
#comparing cooling
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case2\cooling.pkl"
with open(file, 'rb') as pkl_file:
    EP_cooling = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case2\output\ISO13790\Room_1_d90d03ed__c_load_hourly.pkl"
with open(file, 'rb') as pkl_file:
    iso_cooling = 1000*np.array(pickle.load(pkl_file))

title = "EP, cooling load [W]"
filename = "EP, cooling load"
plot_annual_data(EP_cooling, title, filename)

title = "ISO13790, cooling load [W]"
filename = "ISO13790, cooling load"
plot_annual_data(iso_cooling, title, filename)

title = "Difference, cooling load [W]"
filename = "Difference, cooling load"
plot_annual_data(EP_cooling - iso_cooling, title, filename)


r2_plot(data_EP = EP_cooling, 
        data_ISO = iso_cooling, 
        title = "Cooling load [W]", 
        filename = "Cooling load")


#%%

#comparing heating
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case2\heating.pkl"
with open(file, 'rb') as pkl_file:
    EP_heating = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case2\output\ISO13790\Room_1_d90d03ed__h_load_hourly.pkl"
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
#comparing air temp
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case2\air_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_air = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case2\output\ISO13790\Room_1_d90d03ed__theta__air.pkl"
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
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case2\oper_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_op = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case2\output\ISO13790\Room_1_d90d03ed__theta__op.pkl"
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


