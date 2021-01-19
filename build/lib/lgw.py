def lensed_gw_fd():
    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(loc_lensed, diff=None, 
                                    scaled= False, scale_factor=None, cosmo=None)
    return hp_tilde_lensed.to_frequencyseries(), hc_tilde_lensed.to_frequencyseries()

def lensed_gw_td():
    
    from lensGW.waveform.waveform_utils import lens_waveform_model
    from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
    from lensGW.utils.utils import get_lensed_gws
    from pycbc.types.timeseries import TimeSeries
    from pycbc import waveform
    
    approximant=args['approximant']
    mass1=args['mass1']
    mass2=args['mass2']
    spin1x=args['spin1x']
    spin1y=args['spin1y']
    spin1z=args['spin1z']
    spin2x=args['spin2x']
    spin2y=args['spin2y']
    spin2z=args['spin2z']
    inclination=args['inclination']
    distance=args['distance']
    coa_phase=args['coa_phase']
    delta_t=args['delta_t']
    delta_f=args['delta_f']
    f_lower=args['f_lower']
    det=args['det']
    end_time=args['end_time']
    ra=args['ra']
    dec=args['dec']
    polarization=args['polarization']
    eccentricity=args['eccentricity']
    
    y0 = args['y0']
    y1 = args['y1']
    l0 = args['l0']
    l1 = args['l1']
    zS = args['zS']
    zL = args['zL']
    mL1  = args['mL1']
    mL2  = args['mL2']
    lens_model_list = args['lens_model_list']

    Img_ra, Img_dec, source_pos_x, source_pos_y,\
    zL, zS, lens_model_list, kwargs_lens_list, mtot = lens_waveform_model(None).eval_param(
                                                        y0,y1,l0,l1,zS,zL,mL1,mL2,lens_model_list
                                                        )

    hp, hc = get_td_waveform(approximant= approximant, mass1= mass1, mass2= mass2, distance=distance,
                                         spin1z= spin1z,spin1x=spin1x,spin1y=spin1y,
                                         spin2z= spin2z,spin2x=spin2x,spin2y=spin2y,
                                         inclination= inclination, coa_phase= coa_phase,
                                         delta_f= delta_f, f_lower= f_lower,
                                         eccentricity = eccentricity,
                                        )
    hp.start_time += end_time
    # hc.start_time += end_time ----------- this not required 
    
    freq = waveform.utils.frequency_from_polarizations(hp, hc)
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
    hp_tilde_lensed, hc_tilde_lensed, _ = get_lensed_gws(Fmag, hp.data, hc.data, strain.data)

    #------------convert to pycbc.TimeSeries---------------#
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time = hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time = hc.start_time

    #waveform.add_custom_waveform('test',waveform_gen,'time', force=True)
    return hp_tilde_lensed, hc_tilde_lensed