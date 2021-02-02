def lensed_gw_fd(**kwargs):

    y0 = kwargs['y0']
    y1 = kwargs['y1']
    l0 = kwargs['l0']
    l1 = kwargs['l1']
    zS = kwargs['zS']
    zL = kwargs['zL']
    mL = kwargs['mL']
    lens_model_list = kwargs['lens_model_list']
    approx = kwargs['approx']
    mass1 = kwargs['mass1']
    mass2 = kwargs['mass2']
    delta_f = kwargs['delta_f']
    f_lower = kwargs['f_lower']
    distance = kwargs['distance']
    inclination = kwargs['inclination']
    coa_phase = kwargs['coa_phase']
    eccentricity = kwargs['eccentricity']
    spin1x = kwargs['spin1x']
    spin1y = kwargs['spin1y']
    spin1z = kwargs['spin1z']
    spin2x = kwargs['spin2x']
    spin2y = kwargs['spin2y']
    spin2z = kwargs['spin2z']

    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(
                                y0 = y0, y1 = y1, l0 = l0, l1 = l1, zS = zS, zL = zL,
                                mL = mL, lens_model_list = lens_model_list,
                                approx = approx, mass1 = mass1, mass2 = mass2,
                                delta_t = 1./delta_f, f_lower = f_lower,
                                spin1x = spin1x, spin1y = spin1y, spin1z = spin1z,
                                spin2x = spin2x, spin2y = spin2y, spin2z = spin2z, 
                                inclination = inclination, distance = distance,
                                coa_phase = coa_phase, eccentricity = eccentricity, 
                                        )
    
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
    approx = kwargs['approx']
    mass1 = kwargs['mass1']
    mass2 = kwargs['mass2']
    delta_t = kwargs['delta_t']
    f_lower = kwargs['f_lower']
    distance = kwargs['distance']
    inclination = kwargs['inclination']
    coa_phase = kwargs['coa_phase']
    eccentricity = kwargs['eccentricity']
    spin1x = kwargs['spin1x']
    spin1y = kwargs['spin1y']
    spin1z = kwargs['spin1z']
    spin2x = kwargs['spin2x']
    spin2y = kwargs['spin2y']
    spin2z = kwargs['spin2z']
    
    mL = array(mL,dtype=float64)
    Img_ra, Img_dec, source_pos_x, source_pos_y,\
                _, _, _, kwargs_lens_list = lens_waveform_model(None).eval_param(
                                                            y0,y1,l0,l1,zS,zL,mL,lens_model_list)
                                                            
    hp, hc = waveform.get_td_waveform(approximant=approx, mass1=mass1, mass2=mass2, distance=distance,
                                         spin1z=spin1z, spin1x=spin1x, spin1y=spin1y,
                                         spin2z=spin2z, spin2x=spin2x, spin2y=spin2y,
                                         inclination=inclination, coa_phase=coa_phase,
                                         delta_t=delta_t, f_lower=f_lower, eccentricity=eccentricity,
                                        )
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
