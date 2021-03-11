from pycbc import waveform
from lgw import *
waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)
hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(
                approximant="lensed",
                y0 = 0.1,y1 = 0.7937005,l0 = 0.5,l1 = 0,zS = 2.0,zL = 0.5,mL=[1e3,1e3], lens_model_list = ['POINT_MASS', 'POINT_MASS'],
                mass1=300,mass2=300,delta_t=1.0/16384,f_lower=20)