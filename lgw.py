import h5py
import numpy as np
from pycbc.types.timeseries import TimeSeries
from lensGW.waveform.waveform import gw_signal
from lensGW.waveform.lensed_utils import lensed_param
from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
from lensGW.utils.utils import get_lensed_gws

def lensed_gw_fd(loc_lensed,
              diff         = None,
              scaled       = False,
              scale_factor = None,
              cosmo        = None):
    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(loc_lensed, diff=None, scaled= False, scale_factor=None, cosmo=None)
    return hp_tilde_lensed.to_frequencyseries(), hc_tilde_lensed.to_frequencyseries()
    
def lensed_gw_td(loc_lensed,
              diff         = None,
              scaled       = False,
              scale_factor = None,
              cosmo        = None):
    Img_ra, Img_dec, source_pos_x, source_pos_y,\
    zL, zS, lens_model_list, kwargs_lens_list, mtot = lensed_param(loc_lensed).param_initialize()
    strain, hp, hc, freq = unlensed_gw()
    Fmag = geometricalOpticsMagnification(freq.data,
                                       Img_ra,Img_dec,
                                       source_pos_x,source_pos_y,
                                       zL,zS,
                                       lens_model_list,
                                       kwargs_lens_list,
                                       diff         = diff,
                                       scaled       = scaled,
                                       scale_factor = scale_factor,
                                       cosmo        = cosmo)
    #------------return numpy values---------------#
    hp_tilde_lensed, hc_tilde_lensed, lensed_strain = get_lensed_gws(Fmag, hp.data, hc.data, strain.data)
    #------------convert to pycbc.TimeSeries---------------#
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time = hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time = hc.start_time
    lensed_strain = TimeSeries(lensed_strain, delta_t=strain.delta_t)
    lensed_strain.start_time = strain.start_time
    freq = TimeSeries(Fmag, delta_t=freq.delta_t)
    freq.start_time = freq.start_time
    #waveform.add_custom_waveform('test',waveform_gen,'time', force=True)
    return hp_tilde_lensed, hc_tilde_lensed