"""
Description:

"""

import pickle
import numpy as np






#%% Case 1

openstudio_folder = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_comparison\pickles_Case1"


#%% Surface conduction
file = openstudio_folder + "\\ROOM_3_69A20C51..FACE0.pkl"
with open(file, 'rb') as pkl_file:
    ROOM_3_69A20C51_FACE0_HC = pickle.load(pkl_file)



#%%