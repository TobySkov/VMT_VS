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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case3"
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
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_case3"
    plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()


#%% Ouside window radiation
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE0_GLZ0__Surface Outside Face Incident Solar Radiation Rate per Area.pkl"
with open(file, 'rb') as pkl_file:
    ep_face0 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE1_GLZ0__Surface Outside Face Incident Solar Radiation Rate per Area.pkl"
with open(file, 'rb') as pkl_file:
    ep_face1 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE2_GLZ0__Surface Outside Face Incident Solar Radiation Rate per Area.pkl"
with open(file, 'rb') as pkl_file:
    ep_face2 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE3_GLZ0__Surface Outside Face Incident Solar Radiation Rate per Area.pkl"
with open(file, 'rb') as pkl_file:
    ep_face3 = np.array(pickle.load(pkl_file))

title = "EP, window face 0, incident solar radiation  [W/m2]"
filename = "EP, window face 0, incident solar radiation"
plot_annual_data(ep_face0, title, filename)

title = "EP, window face 1, incident solar radiation  [W/m2]"
filename = "EP, window face 1, incident solar radiation"
plot_annual_data(ep_face1, title, filename)

title = "EP, window face 2, incident solar radiation  [W/m2]"
filename = "EP, window face 2, incident solar radiation"
plot_annual_data(ep_face2, title, filename)

title = "EP, window face 3, incident solar radiation  [W/m2]"
filename = "EP, window face 3, incident solar radiation"
plot_annual_data(ep_face3, title, filename)


#%%
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face0_Glz0__Phi_aperture_outside.pkl"
with open(file, 'rb') as pkl_file:
    iso_face0 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face1_Glz0__Phi_aperture_outside.pkl"
with open(file, 'rb') as pkl_file:
    iso_face1 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face2_Glz0__Phi_aperture_outside.pkl"
with open(file, 'rb') as pkl_file:
    iso_face2 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face3_Glz0__Phi_aperture_outside.pkl"
with open(file, 'rb') as pkl_file:
    iso_face3 = np.array(pickle.load(pkl_file))

title = "ISO13790, window face 0, incident solar radiation  [W/m2]"
filename = "ISO13790, window face 0, incident solar radiation"
plot_annual_data(iso_face0, title, filename)

title = "ISO13790, window face 1, incident solar radiation  [W/m2]"
filename = "ISO13790, window face 1, incident solar radiation"
plot_annual_data(iso_face1, title, filename)

title = "ISO13790, window face 2, incident solar radiation  [W/m2]"
filename = "ISO13790, window face 2, incident solar radiation"
plot_annual_data(iso_face2, title, filename)

title = "ISO13790, window face 3, incident solar radiation  [W/m2]"
filename = "ISO13790, window face 3, incident solar radiation"
plot_annual_data(iso_face3, title, filename)

#%%


r2_plot(data_EP = np.concatenate((ep_face0,ep_face1,ep_face2,ep_face3)), 
        data_ISO = np.concatenate((iso_face0,iso_face1,iso_face2,iso_face3)), 
        title = "Windows incident solar radiation [W/m2]", 
        filename = "Windows incident solar radiation")


#%% Transmitted solar radiation

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE0_GLZ0__Surface Window Transmitted Solar Radiation Energy.pkl"
with open(file, 'rb') as pkl_file:
    ep_face0 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE1_GLZ0__Surface Window Transmitted Solar Radiation Energy.pkl"
with open(file, 'rb') as pkl_file:
    ep_face1 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE2_GLZ0__Surface Window Transmitted Solar Radiation Energy.pkl"
with open(file, 'rb') as pkl_file:
    ep_face2 = np.array(pickle.load(pkl_file))
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\ROOM_1_E56F2DAA..FACE3_GLZ0__Surface Window Transmitted Solar Radiation Energy.pkl"
with open(file, 'rb') as pkl_file:
    ep_face3 = np.array(pickle.load(pkl_file))

title = "EP, window face 0, transmitted solar radiation  [W/m2]"
filename = "EP, window face 0, transmitted solar radiation"
plot_annual_data(ep_face0, title, filename)

title = "EP, window face 1, transmitted solar radiation  [W/m2]"
filename = "EP, window face 1, transmitted solar radiation"
plot_annual_data(ep_face1, title, filename)

title = "EP, window face 2, transmitted solar radiation  [W/m2]"
filename = "EP, window face 2, transmitted solar radiation"
plot_annual_data(ep_face2, title, filename)

title = "EP, window face 3, transmitted solar radiation  [W/m2]"
filename = "EP, window face 3, transmitted solar radiation"
plot_annual_data(ep_face3, title, filename)




#%%

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face0_Glz0__Phi_aperture.pkl"
with open(file, 'rb') as pkl_file:
    iso_face0 = np.array(pickle.load(pkl_file))

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face1_Glz0__Phi_aperture.pkl"
with open(file, 'rb') as pkl_file:
    iso_face1 = np.array(pickle.load(pkl_file))
    
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face2_Glz0__Phi_aperture.pkl"
with open(file, 'rb') as pkl_file:
    iso_face2 = np.array(pickle.load(pkl_file))
    
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa..Face3_Glz0__Phi_aperture.pkl"
with open(file, 'rb') as pkl_file:
    iso_face3 = np.array(pickle.load(pkl_file))


title = "ISO13790, window face 0, transmitted solar radiation  [W/m2]"
filename = "ISO13790, window face 0, transmitted solar radiation"
plot_annual_data(iso_face0, title, filename)

title = "ISO13790, window face 1, transmitted solar radiation  [W/m2]"
filename = "ISO13790, window face 1, transmitted solar radiation"
plot_annual_data(iso_face1, title, filename)

title = "ISO13790, window face 2, transmitted solar radiation  [W/m2]"
filename = "ISO13790, window face 2, transmitted solar radiation"
plot_annual_data(iso_face2, title, filename)

title = "ISO13790, window face 3, transmitted solar radiation  [W/m2]"
filename = "ISO13790, window face 3, transmitted solar radiation"
plot_annual_data(iso_face3, title, filename)


#%%

r2_plot(data_EP = np.concatenate((ep_face0,ep_face1,ep_face2,ep_face3)), 
        data_ISO = np.concatenate((iso_face0,iso_face1,iso_face2,iso_face3)), 
        title = "Windows transmitted solar radiation [W/m2]", 
        filename = "Windows transmitted solar radiation")

#%%

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\solar_gain.pkl"
with open(file, 'rb') as pkl_file:
    EP_solar = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa__Phi__sol.pkl"
with open(file, 'rb') as pkl_file:
    iso_solar = 1000*np.array(pickle.load(pkl_file))

title = "EP, total solar heat gain [W]"
filename = "EP, total solar heat gain"
plot_annual_data(EP_solar, title, filename)

title = "ISO13790, total solar heat gain [W]"
filename = "ISO13790, total solar heat gain"
plot_annual_data(iso_solar, title, filename)

title = "Difference, total solar heat gain [W]"
filename = "Difference, total solar heat gain"
plot_annual_data(EP_solar - iso_solar, title, filename)


r2_plot(data_EP = EP_solar, 
        data_ISO = iso_solar, 
        title = "total solar heat gain [W]", 
        filename = "total solar heat gain")

#%% Check that it adds up


ep_solar_check = 19.2*(ep_face0 + ep_face1 + ep_face2 + ep_face3)
iso_solar_check = 19.2*(iso_face0 + iso_face1 + iso_face2 + iso_face3)

title = "EP, solar check"
filename = "delete"
plot_annual_data(EP_solar - ep_solar_check, title, filename)


title = "ISO, solar check"
filename = "delete"
plot_annual_data(iso_solar - iso_solar_check, title, filename)


#%%
#comparing cooling
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\cooling.pkl"
with open(file, 'rb') as pkl_file:
    EP_cooling = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa__c_load_hourly.pkl"
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
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\heating.pkl"
with open(file, 'rb') as pkl_file:
    EP_heating = 1000*np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa__h_load_hourly.pkl"
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
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\air_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_air = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa__theta__air.pkl"
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
file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\openstudio_case3\oper_temp.pkl"
with open(file, 'rb') as pkl_file:
    EP_op = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\iso13790_case3\output\ISO13790\Room_1_e56f2daa__theta__op.pkl"
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


#%%

day1_start_idx = 24*(31+28+21)
day1_end_idx = day1_start_idx + 24

day2_start_idx = 24*(31+28+31+30+31+21)
day2_end_idx = day2_start_idx + 24

day3_start_idx = 24*(31+28+31+30+31+30+31+31+21)
day3_end_idx = day3_start_idx + 24

day4_start_idx = 24*(31+28+31+30+31+30+31+31+30+31+30+21)
day4_end_idx = day4_start_idx + 24

#%% EnergyPlus days


#EP_air[day4_start_idx:day4_end_idx]








