from lensGW.waveform.waveform_utils import lens_waveform_model
from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
from lensGW.utils.utils import get_lensed_gws
from pycbc.types.timeseries import TimeSeries
from pycbc.types.frequencyseries import FrequencySeries
from pycbc import waveform
from numpy import array, float64

def get_lens_param(is_td=True, **kwargs):
    
    y0 = kwargs['y0']
    y1 = kwargs['y1']
    l0 = kwargs['l0']
    l1 = kwargs['l1']
    zS = kwargs['zS']
    zL = kwargs['zL']
    mL = kwargs['mL']
    lens_model_list = kwargs['lens_model_list']
    mL = array(mL,dtype=float64)
    Img_ra, Img_dec, source_pos_x, source_pos_y,\
                _, _, _, kwargs_lens_list = lens_waveform_model(None).eval_param(
                                                            y0,y1,l0,l1,zS,zL,mL,lens_model_list)
                
    if "approximant" in kwargs:
        kwargs.pop("approximant")
    if is_td:
        hp, hc = waveform.get_td_waveform(approximant='IMRPhenomD', **kwargs)
    else:
        hp_fd, hc_fd = waveform.get_fd_waveform(approximant='IMRPhenomD', **kwargs)
        hp, hc = hp_fd.to_timeseries(delta_t=hp_fd.delta_t), hc_fd.to_timeseries(delta_t=hc_fd.delta_t)
    freq = waveform.utils.frequency_from_polarizations(hp, hc)
    Fmag = geometricalOpticsMagnification(freq.data,
                                           Img_ra,Img_dec,
                                           source_pos_x,source_pos_y,
                                           zL,zS,
                                           lens_model_list, kwargs_lens_list)
    #------------return numpy values---------------#
    hp_tilde_lensed, hc_tilde_lensed = get_lensed_gws(Fmag, hp.data, hc.data)
    #------------convert to pycbc.TimeSeries/FrequencySeries---------------#
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time += hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time += hc.start_time
    if is_td:
        return hp_tilde_lensed, hc_tilde_lensed  
    else:
        return hp_tilde_lensed, hc_tilde_lensed, hp.delta_f

def lensed_gw_fd(**kwargs):
    hp_tilde_lensed, hc_tilde_lensed, delta_f = get_lens_param(is_td=False,**kwargs)
    return hp_tilde_lensed.to_frequencyseries(delta_f=delta_f), hc_tilde_lensed.to_frequencyseries(delta_f=delta_f)

def lensed_gw_td(**kwargs):
    return get_lens_param(is_td=True,**kwargs)
