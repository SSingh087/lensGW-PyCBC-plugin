from lgw import *
from pycbc import waveform

if __name__ == "__main__":
    waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)
    print('Done')
    hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(
                    approximant="lensed",
                    y0 = 0.1,y1 = 0.7937005,l0 = 0.5,l1 = 0,zS = 2.0,zL = 0.5,mL1=[1e6,1e6],lens_model_list = ['POINT_MASS', 'POINT_MASS'],
                    approx='IMRPhenomD',mass1=100,mass2=100,spin1x=0.0,spin1y=0.0,
                    spin1z=0.9,spin2x=0.0,spin2y=0.0,spin2z=0.4,inclination=1.23,
                    distance=500,coa_phase=2.45,delta_t=1.0/16384,delta_f=16384,f_lower=30,
                    eccentricity=0)
    print(hp_tilde_lensed)
                              