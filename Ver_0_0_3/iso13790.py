
import numpy as np
from CPP_ISO13790 import run_CPP_ISO13790
from postprocessing import gen_occ_sch




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
    for i, room in enumerate(info["room_info"]):
        #For each room
        H__tr_op = room["H__tr_op"]
        H__tr_w = room["H__tr_w"]
        A__f = room["A__f"]

        A__t = A__f*4.5 #Page 25 pdf
        A__m = A__f*2.5 #page 68 pdf (medium)
        C__m = A__f*165000 #page 68 pdf (medium)

        H__tr_is = 3.45*A__t #Page 25 pdf
        H__tr_ms = 9.1*A__m  #Page 66 pdf
        H__tr_em = 1/(1/H__tr_op - 1/H__tr_ms) #Page 66 pdf

        params = np.array([H__tr_em, H__tr_is, H__tr_w, H__tr_ms,
                       A__f, A__t, A__m, C__m,
                       setpoint_cooling, setpoint_heating])

        end_idx += room["aperture_count"]
        Phi__sol = Phi_sol_2d_W[start_idx:end_idx,:].sum(axis=0)
        start_idx += room["aperture_count"]

        Phi__int = Phi__int_Wm2*A__f

        H__ve = H__ve_infil_1_m2*room["exposed_area"] + H__ve_venti_1_m2*room["A__f"]

        result = run_CPP_ISO13790(theta__e, Phi__sol, Phi__int, H__ve, params)
    



    
    