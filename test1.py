from lgw import *
from pycbc import waveform
import pylab

if __name__ == "__main__":
    waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)
    hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(
                    approximant="lensed",
                    y0 = 0.1,y1 = 0.7937005,l0 = 0.5,l1 = 0,zS = 2.0,zL = 0.5,mL=[1e3,1e3], lens_model_list = ['POINT_MASS', 'POINT_MASS'],
                    approx='IMRPhenomD',mass1=500,mass2=500,spin1x=0.0,spin1y=0.0,
                    spin1z=0.3,spin2x=0.0,spin2y=0.0,spin2z=0.4,inclination=1.23,
                    distance=1000,coa_phase=2.45,delta_t=1.0/16384,delta_f=16384,f_lower=20,
                    eccentricity=.3)
    pylab.plot(hp_tilde_lensed.sample_times, hp_tilde_lensed)
    pylab.plot(hp_tilde_lensed.sample_times, hc_tilde_lensed)
