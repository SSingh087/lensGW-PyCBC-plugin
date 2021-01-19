def lensed_gw_fd(**kwds):
    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(loc_lensed, diff=None, 
                                    scaled= False, scale_factor=None, cosmo=None)
    return hp_tilde_lensed.to_frequencyseries(), hc_tilde_lensed.to_frequencyseries()

def lensed_gw_td(y0 = 0.1,y1 = 0.7937005,l0 = 0.5,l1 = 0,zS = 2.0,zL = 0.5,mL1  = 1e6,
                mL2  = 1e6,lens_model_list = ['POINT_MASS', 'POINT_MASS'],
                approximant='IMRPhenomD',mass1=100,mass2=100,spin1x=0.0,spin1y=0.0,
                spin1z=0.9,spin2x=0.0,spin2y=0.0,spin2z=0.4,inclination=1.23,
                distance=500,coa_phase=2.45,delta_t=1.0/16384,delta_f=16384,f_lower=30,
                polarization=2.34, eccentricity=0,end_time=1192529720):
    
    from lensGW.waveform.waveform_utils import lens_waveform_model
    from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
    from lensGW.utils.utils import get_lensed_gws
    from pycbc.types.timeseries import TimeSeries
    from pycbc import waveform

    Img_ra, Img_dec, source_pos_x, source_pos_y,\
    zL, zS, lens_model_list, kwargs_lens_list, mtot = lens_waveform_model(None).eval_param(
                                                        y0,y1,l0,l1,zS,zL,mL1,mL2,lens_model_list
                                                        )

    hp, hc = waveform.get_td_waveform(approximant= approximant, mass1= mass1, mass2= mass2, distance=distance,
                                         spin1z= spin1z,spin1x=spin1x,spin1y=spin1y,
                                         spin2z= spin2z,spin2x=spin2x,spin2y=spin2y,
                                         inclination= inclination, coa_phase= coa_phase,
                                         delta_t= delta_t, f_lower= f_lower,
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
                                           diff         = None,
                                           scaled       = False,
                                           scale_factor = None,
                                           cosmo        = None)
    #------------return numpy values---------------#
    hp_tilde_lensed, hc_tilde_lensed = get_lensed_gws(Fmag, hp.data, hc.data, None)

    #------------convert to pycbc.TimeSeries---------------#
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time = hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time = hc.start_time

    #waveform.add_custom_waveform('test',waveform_gen,'time', force=True)
    return hp_tilde_lensed, hc_tilde_lensed