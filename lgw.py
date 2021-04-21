from lensGW.waveform.waveform_utils import lens_waveform_model
from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
from lensGW.utils.utils import get_lensed_gws
from pycbc.types.timeseries import TimeSeries
from pycbc.types.frequencyseries import FrequencySeries
from pycbc import waveform
from numpy import array, float64

def get_lens_param(mL, l0, l1, zS, zL, y0, y1, is_td=True, **kwargs):
    optim = kwargs['optim']
    lens_model_list = kwargs['lens_model_list']
    mL, l0, l1 = array(mL,dtype=float64), array(l0,dtype=float64), array(l1,dtype=float64)

    #if mL.shape[1]>1:
    #    mL, l0, l1 = mL.squeeze(axis=0), l0.squeeze(axis=0), l1.squeeze(axis=0)
    #    Img_ra, Img_dec, source_pos_x, source_pos_y, _, _, _, _,\
    #    _, kwargs_lens_list = lens_waveform_model(None).eval_param(
    #                                                y0,y1,l0,l1,zS,zL,mL,lens_model_list,optim)
    #elif len(mL)==1:
    Img_ra, Img_dec, source_pos_x, source_pos_y, _, _, _, _,\
    lens_model_list, kwargs_lens_list=lens_waveform_model(None).eval_param(
                                                y0,y1,l0,l1,zS,zL,mL,lens_model_list,optim)

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

def lensed_gw_fd(mL=1e8, l0=0.5, l1=0, zS=2.0, zL=0.5, y0=0.3, y1=0.3,**kwargs):
    mL, l0, l1 = [mL], [l0], [l1]
    hp_tilde_lensed, hc_tilde_lensed, delta_f = get_lens_param(mL, l0, l1, zS, zL, y0, y1, is_td=False,**kwargs)
    return hp_tilde_lensed.to_frequencyseries(delta_f=delta_f), hc_tilde_lensed.to_frequencyseries(delta_f=delta_f)

def lensed_gw_td(mL=1e8, l0=0.5, l1=0, zS=2.0, zL=0.5, y0=0.3, y1=0.3, **kwargs):
    mL, l0, l1 = [mL], [l0], [l1]
    return get_lens_param(mL, l0, l1, zS, zL, y0, y1, is_td=True,**kwargs)
