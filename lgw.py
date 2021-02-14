def lensed_gw_fd(**kwargs):
    delta_t=1./kwargs['delta_f']
    del kwargs['delta_f']
    kwargs['delta_t'] = delta_t
    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(**kwargs)    
    return hp_tilde_lensed.to_frequencyseries(), hc_tilde_lensed.to_frequencyseries()

def lensed_gw_td(**kwargs):
    
    from lensGW.waveform.waveform_utils import lens_waveform_model
    from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
    from lensGW.utils.utils import get_lensed_gws
    from pycbc.types.timeseries import TimeSeries
    from pycbc import waveform
    from numpy import array, float64
    
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

    hp, hc = waveform.get_td_waveform(approximant='IMRPhenomD', **kwargs)

    freq = waveform.utils.frequency_from_polarizations(hp, hc)
    Fmag = geometricalOpticsMagnification(freq.data,
                                           Img_ra,Img_dec,
                                           source_pos_x,source_pos_y,
                                           zL,zS,
                                           lens_model_list, kwargs_lens_list)
    #------------return numpy values---------------#
    hp_tilde_lensed, hc_tilde_lensed = get_lensed_gws(Fmag, hp.data, hc.data)

    #------------convert to pycbc.TimeSeries---------------#
    
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time += hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time += hc.start_time
    return hp_tilde_lensed, hc_tilde_lensed
