//https://jtt94.github.io/posts/2020/08/pythoncpp/

#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <vector>
#include <chrono>
#include <stdlib.h>

using namespace std;
namespace py = pybind11;





inline void compute(const double& A__m, const double& A__t, const double& H__tr_w, const double& H__tr_is, const double& H__tr_ms,
    const double& H__tr_em, const double& C__m,
    const double& Phi__sol, const double& Phi__int, const double& H__ve,
    const double& theta__e, const double& theta__sup, const double& theta__m_tm1,
    const double& Phi__HC_nd, double& theta__m_t, double& theta__s, double& theta__air)
{
    //ISO 13790
    //Equations: (C.1), (C.2), (C.3)
    double Phi__ia = 0.5 * Phi__int;
    double Phi__m = (A__m / A__t) * (0.5 * Phi__int + Phi__sol);
    double Phi__st = (1 - (A__m / A__t) - H__tr_w / (9.1 * A__t)) * (0.5 * Phi__int + Phi__sol);

    //ISO 13790
    //Equations: (C.6), (C.7), (C.8)
    double H__tr_1 = 1 / ((1 / H__ve) + (1 / H__tr_is));
    double H__tr_2 = H__tr_1 + H__tr_w;
    double H__tr_3 = 1 / ((1 / H__tr_2) + (1 / H__tr_ms));

    //ISO 13790
    //Equations: (C.4), (C.5)
    double Phi__mtot = Phi__m + H__tr_em * theta__e + \
        H__tr_3 * ((Phi__st + H__tr_w * theta__e + H__tr_1 * (theta__sup + \
            (Phi__ia + Phi__HC_nd) / (H__ve))) / (H__tr_2));

    theta__m_t = (theta__m_tm1 * (C__m / 3600.0 - (0.5 * (H__tr_3 + H__tr_em))) \
        + Phi__mtot) / (C__m / 3600.0 + (0.5 * (H__tr_3 + H__tr_em)));

    //ISO 13790
    //Equations: (C.9), (C.10), (C.11)
    double theta__m = 0.5 * (theta__m_t + theta__m_tm1);

    theta__s = (H__tr_ms * theta__m + Phi__st + H__tr_w * theta__e + \
        H__tr_1 * (theta__sup + \
            (Phi__ia + Phi__HC_nd) / H__ve)) / (H__tr_ms + H__tr_w + \
                + H__tr_1);

    theta__air = (H__tr_is * theta__s + H__ve * theta__sup + Phi__ia + \
        Phi__HC_nd) / (H__tr_is + H__ve);
}






py::array_t<double> run_CPP_ISO13790(py::array_t<double> np_theta__e, py::array_t<double> np_Phi__sol,
    py::array_t<double> np_Phi__int, py::array_t<double> np_H__ve,
    py::array_t<double> params) {

    //Check input
    py::buffer_info buf_theta__e = np_theta__e.request();
    py::buffer_info buf_Phi__sol = np_Phi__sol.request();
    py::buffer_info buf_Phi__int = np_Phi__int.request();
    py::buffer_info buf_H__ve = np_H__ve.request();
    py::buffer_info buf_params = params.request();

    if (buf_theta__e.size != 8760 || buf_Phi__sol.size != 8760 || buf_Phi__int.size != 8760 || buf_H__ve.size != 8760 || buf_params.size != 10)
        throw std::runtime_error("Number of dimensions must be 8760 (input) or 10 (params)");

    //Convert input to arrays
    double* ptr_theta__e = (double*)buf_theta__e.ptr,
        * ptr_Phi__sol = (double*)buf_Phi__sol.ptr,
        * ptr_Phi__int = (double*)buf_Phi__int.ptr,
        * ptr_H__ve = (double*)buf_H__ve.ptr,
        * ptr_params = (double*)buf_params.ptr;

    //Allocate output
    vector<double> vec_theta__m(8760);
    vector<double> vec_theta__s(8760);
    vector<double> vec_theta__air(8760);
    vector<double> vec_Phi__HC_nd(8760);

    vector<double> vec_theta__m_t_old = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    vector<double> vec_theta__m_t_new = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

    //Unpack params
    double H__tr_em = ptr_params[0];
    double H__tr_is = ptr_params[1];
    double H__tr_w = ptr_params[2];
    double H__tr_ms = ptr_params[3];
    double A__f = ptr_params[4];
    double A__t = ptr_params[5];
    double A__m = ptr_params[6];
    double C__m = ptr_params[7];

    double setpoint_cooling = ptr_params[8];
    double setpoint_heating = ptr_params[9];


    double theta__m_tm1 = 10;

    //Allocate variables used in loop
    double Phi__sol, Phi__int, theta__e, theta__sup, H__ve;

    double Phi__HC_nd_0 = 0;
    double Phi__HC_nd_10 = 10 * A__f;
    double Phi__HC_nd;

    double theta__m_t_0, theta__s_0, theta__air_0;
    double theta__m_t_10, theta__s_10, theta__air_10;
    double theta__m_t, theta__s, theta__air;

    double theta__air_set;
    
    bool warmup = true;
    double cum_diff;
    int warmup_day = 0;


    //Warmup
    while (warmup) {
        for (int i = 0; i < 24; i++) {//Run first 24 hours of year again and again

            Phi__sol = ptr_Phi__sol[i];
            Phi__int = ptr_Phi__int[i];
            theta__e = ptr_theta__e[i];
            theta__sup = ptr_theta__e[i];
            H__ve = ptr_H__ve[i];

            compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
                Phi__HC_nd_0, theta__m_t_0, theta__s_0, theta__air_0);

            if (setpoint_heating <= theta__air_0 && theta__air_0 <= setpoint_cooling) { //Free floating conditions

                theta__m_tm1 = theta__m_t_0;
                vec_theta__m_t_new[i] = theta__m_t_0;

            }
            else {

                compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
                    Phi__HC_nd_10, theta__m_t_10, theta__s_10, theta__air_10);

                //Establishing what target to reach for/interpolate to
                if (theta__air_0 < setpoint_heating) {
                    theta__air_set = setpoint_heating;
                }
                else if (setpoint_cooling < theta__air_0) {
                    theta__air_set = setpoint_cooling;
                }

                Phi__HC_nd = Phi__HC_nd_10 * ((theta__air_set - theta__air_0) / (theta__air_10 - theta__air_0));

                compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
                    Phi__HC_nd, theta__m_t, theta__s, theta__air);

                theta__m_tm1 = theta__m_t;
                vec_theta__m_t_new[i] = theta__m_t;

            }
        }
        //Evaluate warmup day
        cum_diff = 0;
        for (int i = 0; i < 24; i++) {
            cum_diff += abs(vec_theta__m_t_new[i] - vec_theta__m_t_old[i]);
        }
        if (cum_diff < 0.5) {
            warmup = false;
        }
        warmup_day += 1;
        //cout << "Warmup day: " << warmup_day << "  Cummulative difference: " << cum_diff << "\n";
        vec_theta__m_t_old = vec_theta__m_t_new;
    }



    //Annual simulation
    for (int i = 0; i < 8760; i++) {

        Phi__sol = ptr_Phi__sol[i];
        Phi__int = ptr_Phi__int[i];
        theta__e = ptr_theta__e[i];
        theta__sup = ptr_theta__e[i];
        H__ve = ptr_H__ve[i];

        compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
            Phi__HC_nd_0, theta__m_t_0, theta__s_0, theta__air_0);

        if (setpoint_heating <= theta__air_0 && theta__air_0 <= setpoint_cooling) { //Free floating conditions

            theta__m_tm1 = theta__m_t_0;

            vec_theta__m[i] = theta__m_t_0;
            vec_theta__s[i] = theta__s_0;
            vec_theta__air[i] = theta__air_0;
            vec_Phi__HC_nd[i] = Phi__HC_nd_0;

        }
        else {

            compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
                Phi__HC_nd_10, theta__m_t_10, theta__s_10, theta__air_10);

            //Establishing what target to reach for/interpolate to
            if (theta__air_0 < setpoint_heating) {
                theta__air_set = setpoint_heating;
            }
            else if (setpoint_cooling < theta__air_0) {
                theta__air_set = setpoint_cooling;
            }

            Phi__HC_nd = Phi__HC_nd_10 * ((theta__air_set - theta__air_0) / (theta__air_10 - theta__air_0));

            compute(A__m, A__t, H__tr_w, H__tr_is, H__tr_ms, H__tr_em, C__m, Phi__sol, Phi__int, H__ve, theta__e, theta__sup, theta__m_tm1,
                Phi__HC_nd, theta__m_t, theta__s, theta__air);

            theta__m_tm1 = theta__m_t;

            vec_theta__m[i] = theta__m_t;
            vec_theta__s[i] = theta__s;
            vec_theta__air[i] = theta__air;
            vec_Phi__HC_nd[i] = Phi__HC_nd;

        }
    }



    //Converting 4 output vectors into 1
    auto np_result = py::array_t<double>(8760 * 4);
    py::buffer_info buf_result = np_result.request();
    double* ptr_result = (double*)buf_result.ptr;
    size_t idx = 0;
    int i;
    for (i = 0; i < 8760; i++)
    {
        ptr_result[idx] = vec_theta__m[i];
        idx += 1;
    }

    for (i = 0; i < 8760; i++)
    {
        ptr_result[idx] = vec_theta__s[i];
        idx += 1;
    }

    for (i = 0; i < 8760; i++)
    {
        ptr_result[idx] = vec_theta__air[i];
        idx += 1;
    }

    for (i = 0; i < 8760; i++)
    {
        ptr_result[idx] = vec_Phi__HC_nd[i];
        idx += 1;
    }


    return np_result;
}



PYBIND11_MODULE(CPP_ISO13790, m) {

    m.def("run_CPP_ISO13790", &run_CPP_ISO13790, "Running ISO13790 annual simulation");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}



