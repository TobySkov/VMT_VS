"""
Description:

"""


import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

#%%

def r2_plot(data_1, data_2, xlabel, ylabel, title, filename):

    both_data = np.concatenate((data_1, data_2))
    min_val = np.min(both_data)
    max_val = np.max(both_data)
    
    r2 = r2_score(data_1, data_2)
    
    plt.figure(figsize=(6,3),dpi=500)
    plt.plot(data_1, data_2,"o")
    plt.plot([min_val, max_val],[min_val, max_val],c="black")
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(f"{title}. R2 = {r2:.6f}", fontsize=14)
    path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\plots_daylight"
    plt.savefig(path + "\\" + filename + ".png", dpi=500, bbox_inches = 'tight', pad_inches = 0)
    plt.show()


#%%

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\daylight\VMT_Accelerad_da.pkl"
with open(file, 'rb') as pkl_file:
    output_vmt_accelerad = np.array(pickle.load(pkl_file))


file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\daylight\VMT_Radiance_da.pkl"
with open(file, 'rb') as pkl_file:
    output_vmt_radiance = np.array(pickle.load(pkl_file))

file = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\daylight\ladybugtools_da.pkl"
with open(file, 'rb') as pkl_file:
    output_ladybug_radiance = np.array(pickle.load(pkl_file))


#%%

r2_plot(data_1 = output_ladybug_radiance, 
        data_2 = output_vmt_accelerad, 
        xlabel = "Ladybug Tools", 
        ylabel = "VMT", 
        title = "Daylight autonomy comparison", 
        filename = "VMT_vs_Ladybug")


#%%

r2_plot(data_1 = output_vmt_radiance, 
        data_2 = output_vmt_accelerad, 
        xlabel = "VMT running Radiance", 
        ylabel = "VMT running Accelerad", 
        title = "Daylight autonomy comparison", 
        filename = "VMT_vs_VMT")


