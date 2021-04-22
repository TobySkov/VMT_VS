
import numpy as np
from CPP_ISO13790 import run_CPP_ISO13790


def run_ISO13790():


    H__tr_op
    H__tr_w
    A__f

    A__t = A__f*4.5 #Page 25 pdf
    A__m = A__f*2.5 #page 68 pdf (medium)
    C__m = A__f*165000 #page 68 pdf (medium)

    H__tr_is = 3.45*A__t #Page 25 pdf
    H__tr_ms = 9.1*A__m  #Page 66 pdf
    H__tr_em = 1/(1/H__tr_op - 1/H__tr_ms) #Page 66 pdf

    setpoint_cooling = 20.0
    setpoint_heating = 26.0

    params = np.array([H__tr_em, H__tr_is, H__tr_w, H__tr_ms,
                       A__f, A__t, A__m, C__m,
                       setpoint_cooling, setpoint_heating])

    theta__e = np.zeros((8760))
    Phi_sol = np.zeros((8760))
    Phi_int = np.zeros((8760))
    H__ve = np.zeros((8760))
    


    pass

    
    