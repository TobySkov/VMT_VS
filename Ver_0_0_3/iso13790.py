import pickle
import numpy as np
from CPP_ISO13790 import run_CPP_ISO13790
from postprocessing import gen_occ_sch
import time

def ISO13790(info):

    start = time.time()
    run_ISO13790(info)
    end = time.time()
    print(f"+++++ run_ISO13790, wall time: {end-start} [s] +++++")

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
        #theta__s = room["theta__s"]
        U__window = room["U__window"]

        for j, aperture_name in enumerate(room["aperture_identifiers_list"]):
            aperture_mesh_areas = np.array(room["aperture_areas_list"][j])

            #This will be positive, when heat going from outside to inside
            #   just like solar gain and HC load.
            #window_HC = np.matmul(np.reshape((U__window*aperture_mesh_areas),(len(aperture_mesh_areas),1)), np.reshape((theta__e-theta__s),(1,8760)))
            
            end_idx += len(aperture_mesh_areas)
            Phi_aperture = info["Phi_sol_2d_Wm2"][start_idx:end_idx,:]
            Phi_aperture_outside = info["Phi_sol_2d_Wm2_outside"][start_idx:end_idx,:]
            start_idx += len(aperture_mesh_areas)


            with open(output_folder.joinpath(f"{aperture_name}__Phi_aperture.pkl"), 'wb') as outfile:
                pickle.dump((np.mean(Phi_aperture,axis=0)).tolist(), outfile, protocol = 2) 

            with open(output_folder.joinpath(f"{aperture_name}__Phi_aperture_outside.pkl"), 'wb') as outfile:
                pickle.dump((np.mean(Phi_aperture_outside,axis=0)).tolist(), outfile, protocol = 2) 
                 



def run_ISO13790(info):

    occ_sch = gen_occ_sch()

    theta__e = np.array(info["theta__e"])

    # 1200 J/(m3.K)
    H__ve_infil_1_m2 = np.ones((8760))*(1200*0.0001)    #Per exposed area, (0.0001 m3/(s.m2))
    H__ve_venti_1_m2 = occ_sch*(1200*0.0012)            #Per floor area, (q__tot = 1.2 l/(s.m2) = 0.0012 m3/(s.m2))
    
    setpoint_heating = 20.0
    setpoint_cooling = 26.0
    
    Phi__int_people_Wm2 = 108*(1/15) #108 W/person, 15 m2/person
    Phi__int_equip_Wm2 = 5 #5 W/m2 equipment
    Phi__int_light_Wm2 = 5 #5 W/m2 Lighting 
    Phi__int_Wm2 = occ_sch*(Phi__int_people_Wm2 + Phi__int_equip_Wm2 + Phi__int_light_Wm2)

    Phi_sol_2d_W = info["Phi_sol_2d_W"]

    start_idx = 0
    end_idx = 0

    theta__m = np.zeros((8760))
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
        theta__m = result[0:8760]
        theta__s = result[8760:2*8760]
        theta__air = result[2*8760:(3*8760)]
        Phi__HC_nd = result[(3*8760):(4*8760)]

        ###Saving results
        Phi__H_nd = np.zeros((8760))
        Phi__C_nd = np.zeros((8760))

        Phi__H_nd[Phi__HC_nd > 0] = Phi__HC_nd[Phi__HC_nd > 0]/(1000)   #Conversion from Wh to kWh
        Phi__C_nd[Phi__HC_nd < 0] = -Phi__HC_nd[Phi__HC_nd < 0]/(1000)  #Conversion from Wh to kWh
        Phi__HC_nd = Phi__HC_nd/(1000)                                  #Conversion from Wh to kWh
        Phi__sol = Phi__sol/1000                                        #Conversion from Wh to kWh
        theta__op = 0.3*theta__air + 0.7*theta__s

        room["theta__s"] = theta__s

        #Additional outputs
        infil_HC = (np.multiply((H__ve_infil_1_m2*room["exposed_area"]),
                                (theta__e - theta__air)))/1000

        venti_HC = (np.multiply((H__ve_venti_1_m2*room["A__f"]),
                               (theta__e - theta__air)))/1000

        windows_HC = (H__tr_w*(theta__e - theta__s))/1000

        walls_HC_em = (H__tr_em*(theta__e - theta__m))/1000

        walls_HC_ms = (H__tr_ms*(theta__m - theta__s))/1000

        Phi__int_people = (occ_sch*Phi__int_people_Wm2*A__f)/1000
        Phi__int_equip = (occ_sch*Phi__int_equip_Wm2*A__f)/1000
        Phi__int_light = (occ_sch*Phi__int_light_Wm2*A__f)/1000

        output_folder = info["sim_folder"].joinpath("output\\ISO13790")

        #Saving hourly heating and cooling load
        with open(output_folder.joinpath(f"{name}__hc_load_hourly.pkl"), 'wb') as outfile:
            pickle.dump(Phi__HC_nd.tolist(), outfile, protocol = 2)

        #Saving heating load
        with open(output_folder.joinpath(f"{name}__h_load_hourly.pkl"), 'wb') as outfile:
            pickle.dump(Phi__H_nd.tolist(), outfile, protocol = 2)

        #Saving cooling load
        with open(output_folder.joinpath(f"{name}__c_load_hourly.pkl"), 'wb') as outfile:
            pickle.dump(Phi__C_nd.tolist(), outfile, protocol = 2)

        #Saving theta__air
        with open(output_folder.joinpath(f"{name}__theta__air.pkl"), 'wb') as outfile:
            pickle.dump(theta__air.tolist(), outfile, protocol = 2)

        #Saving theta__op
        with open(output_folder.joinpath(f"{name}__theta__op.pkl"), 'wb') as outfile:
            pickle.dump(theta__op.tolist(), outfile, protocol = 2)

        #Saving Phi_sol
        with open(output_folder.joinpath(f"{name}__Phi__sol.pkl"), 'wb') as outfile:
            pickle.dump(Phi__sol.tolist(), outfile, protocol = 2)

        #Additional output
        with open(output_folder.joinpath(f"{name}__infil_HC.pkl"), 'wb') as outfile:
            pickle.dump(infil_HC.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__venti_HC.pkl"), 'wb') as outfile:
            pickle.dump(venti_HC.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__windows_HC.pkl"), 'wb') as outfile:
            pickle.dump(windows_HC.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__walls_HC_em.pkl"), 'wb') as outfile:
            pickle.dump(walls_HC_em.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__walls_HC_ms.pkl"), 'wb') as outfile:
            pickle.dump(walls_HC_ms.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__Phi__int_people.pkl"), 'wb') as outfile:
            pickle.dump(Phi__int_people.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__Phi__int_equip.pkl"), 'wb') as outfile:
            pickle.dump(Phi__int_equip.tolist(), outfile, protocol = 2)

        with open(output_folder.joinpath(f"{name}__Phi__int_light.pkl"), 'wb') as outfile:
            pickle.dump(Phi__int_light.tolist(), outfile, protocol = 2)





    

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