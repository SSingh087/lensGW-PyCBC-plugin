from lensGW.waveform.waveform_utils import lens_waveform_model
from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
from lensGW.utils.utils import get_lensed_gws
from pycbc.types.timeseries import TimeSeries
from pycbc.types.frequencyseries import FrequencySeries
from pycbc import waveform
from numpy import array, float64

def get_lens_param(ml, lens_ra, lens_dec, zs, zl, source_ra, source_dec, n_images=1,
                    is_td=True, **kwargs):
                    
    """
    Evaluates the lensed waveform with respect to the given parameters
    :param ml: lens mass
    :type ml: float
    :param source_ra: Right accession of the source of GW (in radians)
    :type source_ra: float
    :param source_dec: Declination of the source of GW (in radians)
    :type source_dec: float
    :param lens_ra: Right accession of the lens (in radians)
    :type lens_ra: array
    :param lens_dec: Declination of the lens (in radians)
    :type lens_dec: array
    :param zl: lens redshift
    :type zl: float
    :param zs: source redshift
    :type zs: float
    :param n_images: Number of images to output (should be less than total images found)
    :type n_images: integer
    :param is_td: Is time domain ?
    :type is_td: Bool (default True)
    :param: **kwargs: other lens parameters
    
    :return:
    :param: hp_tilde_lensed, hp_tilde_lensed, delta_f (only for Frequecy Domain)
    :rtype: TimeSeries, TimeSeries, float
    """
    
    optim = kwargs['optim']
    lens_model_list = kwargs['lens_model_list']
    ml, lens_ra, lens_dec = array(ml,dtype=float64), array(lens_ra,dtype=float64), array(lens_dec,dtype=float64)

    #if mL.shape[1]>1:
    #    mL, l0, l1 = mL.squeeze(axis=0), l0.squeeze(axis=0), l1.squeeze(axis=0)
    #    Img_ra, Img_dec, source_pos_x, source_pos_y, _, _, _, _,\
    #    _, kwargs_lens_list = lens_waveform_model(None).eval_param(
    #                                                y0,y1,l0,l1,zS,zL,mL,lens_model_list,optim)
    #elif len(mL)==1:

    Img_ra, Img_dec, kwargs_lens_list=lens_waveform_model(None).eval_param(
                                                    source_ra, source_dec, lens_ra, lens_dec, 
                                                    zs, zl, ml, lens_model_list, optim)

    if "approximant" in kwargs:
        kwargs.pop("approximant")
    if is_td:
        hp, hc = waveform.get_td_waveform(approximant='IMRPhenomD', **kwargs)
    else:
        hp_fd, hc_fd = waveform.get_fd_waveform(approximant='IMRPhenomD', **kwargs)
        hp, hc = hp_fd.to_timeseries(delta_t=hp_fd.delta_t), hc_fd.to_timeseries(delta_t=hc_fd.delta_t)
    freq = waveform.utils.frequency_from_polarizations(hp, hc)
    Fmag = geometricalOpticsMagnification(freq.data, Img_ra, Img_dec,
                                           source_ra, source_dec,
                                           zl, zs, lens_model_list, kwargs_lens_list)
                                           
    #------------return numpy values---------------#
    hp_tilde_lensed, hc_tilde_lensed = get_lensed_gws(Fmag, hp.data, hc.data)
    #------------convert to pycbc.TimeSeries/FrequencySeries---------------#
    #iterating wrt to number of images corresponding to each time delay
    
    hp_tilde_lensed = TimeSeries(hp_tilde_lensed, delta_t=hp.delta_t)
    hp_tilde_lensed.start_time += hp.start_time
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    hc_tilde_lensed.start_time += hc.start_time
    
    # only returns nth image
    if is_td:
        return hp_tilde_lensed[n_images-1], hc_tilde_lensed[n_images-1]  
    else:
        return hp_tilde_lensed[n_images-1], hc_tilde_lensed[n_images-1], hp.delta_f
        
        
    
    #if n_images <= len(Img_ra):
        #if is_td:
            #return hp_tilde_lensed[:n,:], hc_tilde_lensed[:n,:]  
        #else:
            #return hp_tilde_lensed[:n,:], hc_tilde_lensed[:n,:], hp.delta_f

def lensed_gw_fd(ml=1e8, lens_ra=0.5, lens_dec=0, zs=2.0, zl=0.5, source_ra=0.3, source_dec=0.3,
                n_images=1, **kwargs):
    """
    Returns the lensed waveform in Frequecy domain
    :param mL: lens mass (default: 1e8)
    :type mL: float
    :param source_ra: Right accession of the source of GW (in radians) (default: 0.3)
    :type source_ra: float
    :param source_dec: Declination of the source of GW (in radians) (default: 0.3)
    :type source_dec: float
    :param lens_ra: Right accession of the lens (in radians) (default: 0.5)
    :type lens_ra: array
    :param lens_dec: Declination of the lens (in radians) (default: 0)
    :type lens_dec: array
    :param zl: lens redshift (default: 0.5)
    :type zl: float
    :param zs: source redshift (default: 2)
    :type zs: float
    :param n_images: Number of images to output (should be less than total images found)
    :type n_images: integer
    :param: **kwargs: other lens parameters
    """
    
    ml, lens_ra, lens_dec = [ml], [lens_ra], [lens_dec]
    hp_tilde_lensed, hc_tilde_lensed, delta_f = get_lens_param(ml, lens_ra, lens_dec, zs, zl, source_ra, source_dec,
                                                               n_images=1, is_td=False,**kwargs)
    return hp_tilde_lensed.to_frequencyseries(delta_f=delta_f), hc_tilde_lensed.to_frequencyseries(delta_f=delta_f)

def lensed_gw_td(ml=1e8, lens_ra=0.5, lens_dec=0, zs=2.0, zl=0.5, source_ra=0.3, source_dec=0.3, 
                n_images=1, **kwargs):
    """
    Returns the lensed waveform in Time domain
    :param ml: lens mass (default: 1e8)
    :type ml: float
    :param source_ra: Right accession of the source of GW (in radians) (default: 0.3)
    :type source_ra: float
    :param source_dec: Declination of the source of GW (in radians) (default: 0.3)
    :type source_dec: float
    :param lens_ra: Right accession of the lens (in radians) (default: 0.5)
    :type lens_ra: array
    :param lens_dec: Declination of the lens (in radians) (default: 0)
    :type lens_dec: array
    :param zl: lens redshift (default: 0.5)
    :type zl: float
    :param zs: source redshift (default: 2)
    :type zs: float
    :param: **kwargs: other lens parameters
    """
 
    ml, lens_ra, lens_dec = [ml], [lens_ra], [lens_dec]
    return get_lens_param(ml, lens_ra, lens_dec, zs, zl, source_ra, source_dec, 
                            n_images=1, is_td=True,**kwargs)
