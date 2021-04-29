import pickle
import numpy as np
from CPP_ISO13790 import run_CPP_ISO13790
from postprocessing import gen_occ_sch


def ISO13790(info):

    run_ISO13790(info)

    window_output(info)




def window_output(info):

    output_folder = info["sim_folder"].joinpath("output\\ISO13790")

    if info["hemisphere"] == "northern":
        sum_idx = get_summer_idx_northern(info)
        win1_idx = get_winter1_idx_northern(info)
        win2_idx = get_winter2_idx_northern(info)

    elif info["hemisphere"] == "southern":
        sum1_idx = get_summer1_idx_southern(info)
        sum2_idx = get_summer2_idx_southern(info)
        win_idx = get_winter_idx_southern(info)

    theta__e = np.array(info["theta__e"])

    start_idx = 0
    end_idx = 0
    for i, room in enumerate(info["room_info"]):
        theta__s = room["theta__s"]
        U__window = room["U__window"]

        for j, aperture_name in enumerate(room["aperture_identifiers_list"]):
            aperture_mesh_areas = np.array(room["aperture_areas_list"][j])

            #This will be positive, when heat going from outside to inside
            #   just like solar gain and HC load.
            window_HC = np.matmul(np.reshape((U__window*aperture_mesh_areas),(len(aperture_mesh_areas),1)), np.reshape((theta__e-theta__s),(1,8760)))
            
            end_idx += len(aperture_mesh_areas)
            Phi_aperture = info["Phi_sol_2d_W"][start_idx:end_idx,:]
            start_idx += len(aperture_mesh_areas)

            if info["hemisphere"] == "northern":
                summer_window_HC = window_HC[:,sum_idx[0]:sum_idx[1]].sum(axis=1)/1000 #Translated to kWh
                winter_window_HC = (window_HC[:,win1_idx[0]:win1_idx[1]].sum(axis=1) + window_HC[:,win2_idx[0]:win2_idx[1]].sum(axis=1))/1000 #Translated to kWh

                summer_window_Phi = Phi_aperture[:,sum_idx[0]:sum_idx[1]].sum(axis=1)/1000 #Translated to kWh
                winter_window_Phi = (Phi_aperture[:,win1_idx[0]:win1_idx[1]].sum(axis=1) + Phi_aperture[:,win2_idx[0]:win2_idx[1]].sum(axis=1))/1000 #Translated to kWh

            elif info["hemisphere"] == "southern":
                summer_window_HC = (window_HC[:,sum1_idx[0]:sum1_idx[1]].sum(axis=1) + window_HC[:,sum2_idx[0]:sum2_idx[1]].sum(axis=1))/1000 #Translated to kWh
                winter_window_HC = window_HC[:,win_idx[0]:win_idx[1]].sum(axis=1) /1000 #Translated to kWh
            
                summer_window_Phi = (Phi_aperture[:,sum1_idx[0]:sum1_idx[1]].sum(axis=1) + Phi_aperture[:,sum2_idx[0]:sum2_idx[1]].sum(axis=1))/1000 #Translated to kWh
                winter_window_Phi = Phi_aperture[:,win_idx[0]:win_idx[1]].sum(axis=1) /1000 #Translated to kWh

            #Saving heating load
            with open(output_folder.joinpath(f"{aperture_name}__summer_HC.pkl"), 'wb') as outfile:
                pickle.dump(summer_window_HC.tolist(), outfile, protocol = 2)

            #Saving cooling load
            with open(output_folder.joinpath(f"{aperture_name}__winter_HC.pkl"), 'wb') as outfile:
                pickle.dump(winter_window_HC.tolist(), outfile, protocol = 2)

            #Saving theta__air
            with open(output_folder.joinpath(f"{aperture_name}__summer_Phi.pkl"), 'wb') as outfile:
                pickle.dump(summer_window_Phi.tolist(), outfile, protocol = 2)

            #Saving theta__op
            with open(output_folder.joinpath(f"{aperture_name}__winter_Phi.pkl"), 'wb') as outfile:
                pickle.dump(winter_window_Phi.tolist(), outfile, protocol = 2)



def run_ISO13790(info):

    

    occ_sch = gen_occ_sch()

    theta__e = np.array(info["theta__e"])

    # 1200 J/(m3.K)
    H__ve_infil_1_m2 = np.ones((8760))*(1200*0.0001)    #Per exposed area, (0.0001 m3/(s.m2))
    H__ve_venti_1_m2 = occ_sch*(1200*0.0012)            #Per floor area, (q__tot = 1.2 l/(s.m2) = 0.0012 m3/(s.m2))
    
    setpoint_cooling = 20.0
    setpoint_heating = 26.0

    Phi__int_people_Wm2 = 108*(1/15) #108 W/person, 15 m2/person
    Phi__int_equip_Wm2 = 5 #5 W/m2 equipment
    Phi__int_light_Wm2 = 5 #5 W/m2 Lighting - Should prob be turned of when DA reaches certain level.
    Phi__int_Wm2 = occ_sch*(Phi__int_people_Wm2 + Phi__int_equip_Wm2 + Phi__int_light_Wm2)

    Phi_sol_2d_W = info["Phi_sol_2d_W"]

    start_idx = 0
    end_idx = 0

    theta__s = np.zeros((8760))
    theta__air = np.zeros((8760))
    Phi__HC_nd = np.zeros((8760))

    for i, room in enumerate(info["room_info"]):

        #For each room
        name = room["name"]
        H__tr_op = room["H__tr_op"]
        H__tr_w = room["H__tr_w"]
        A__f = room["A__f"]

        A__t = A__f*4.5         #Page 25 pdf
        A__m = A__f*2.5         #page 68 pdf (medium)
        C__m = A__f*165000      #page 68 pdf (medium)

        H__tr_is = 3.45*A__t    #Page 25 pdf
        H__tr_ms = 9.1*A__m     #Page 66 pdf
        H__tr_em = 1/(1/H__tr_op - 1/H__tr_ms) #Page 66 pdf

        params = np.array([H__tr_em, H__tr_is, H__tr_w, H__tr_ms,
                       A__f, A__t, A__m, C__m,
                       setpoint_cooling, setpoint_heating])

        end_idx += room["room_aperture_mesh_face_count"]
        Phi__sol = Phi_sol_2d_W[start_idx:end_idx,:].sum(axis=0)
        start_idx += room["room_aperture_mesh_face_count"]

        Phi__int = Phi__int_Wm2*A__f

        H__ve = H__ve_infil_1_m2*room["exposed_area"] + H__ve_venti_1_m2*room["A__f"]

        result = run_CPP_ISO13790(theta__e, Phi__sol, Phi__int, H__ve, params)

        #Unpacking results
        theta__s = result[0:8760]
        theta__air = result[8760:(2*8760)]
        Phi__HC_nd = result[(2*8760):(3*8760)]

        ###Saving results
        Phi__H_nd = Phi__HC_nd[Phi__HC_nd > 0].sum()/(1000*A__f) #Conversion from Wh to kWh/(m2)
        Phi__C_nd = Phi__HC_nd[Phi__HC_nd < 0].sum()/(1000*A__f) #Conversion from Wh to kWh/(m2)
        theta__op = 0.3*theta__air + 0.7*theta__s

        room["theta__s"] = theta__s

        output_folder = info["sim_folder"].joinpath("output\\ISO13790")

        #Saving heating load
        with open(output_folder.joinpath(f"{name}__h_load.pkl"), 'wb') as outfile:
            pickle.dump(Phi__H_nd.tolist(), outfile, protocol = 2)

        #Saving cooling load
        with open(output_folder.joinpath(f"{name}__c_load.pkl"), 'wb') as outfile:
            pickle.dump(Phi__C_nd.tolist(), outfile, protocol = 2)

        #Saving theta__air
        with open(output_folder.joinpath(f"{name}__theta__air.pkl"), 'wb') as outfile:
            pickle.dump(theta__air.tolist(), outfile, protocol = 2)

        #Saving theta__op
        with open(output_folder.joinpath(f"{name}__theta__op.pkl"), 'wb') as outfile:
            pickle.dump(theta__op.tolist(), outfile, protocol = 2)





    

def get_summer_idx_northern(info): #June, July, August
    start_idx = (31+28+31+30+31)*24
    end_idx = start_idx+(30+31+31)*24
    return (start_idx, end_idx)
   
def get_winter1_idx_northern(info): #December
    start_idx = 8760 - (31)*24
    end_idx = 8760
    return (start_idx, end_idx)

def get_winter2_idx_northern(info): #January, February
    start_idx = 0
    end_idx = (31+28)*24
    return (start_idx, end_idx)




def get_summer1_idx_southern(info): #December
    start_idx = 8760 - (31)*24
    end_idx = 8760
    return (start_idx, end_idx)
   
def get_summer2_idx_southern(info): #January, February
    start_idx = 0
    end_idx = (31+28)*24
    return (start_idx, end_idx)

def get_winter_idx_southern(info): #June, July, August
    start_idx = (31+28+31+30+31)*24
    end_idx = start_idx+(30+31+31)*24
    return (start_idx, end_idx)