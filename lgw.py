# Copyright (C) 2021  Shashwat Singh
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

def lensed_gw_fd(**kwargs):

    y0 = kwargs['y0']
    y1 = kwargs['y1']
    l0 = kwargs['l0']
    l1 = kwargs['l1']
    zS = kwargs['zS']
    zL = kwargs['zL']
    mL = kwargs['mL']
    lens_model_list = kwargs['lens_model_list']
    if 'approx' in kwargs:
        approx = kwargs.pop('approx')
    else:
        approx = 'IMRPhenomD'
    mass1 = kwargs['mass1']
    mass2 = kwargs['mass2']
    delta_t = kwargs['delta_t']
    delta_f = kwargs['delta_f']
    f_lower = kwargs['f_lower']
    if 'spin1x' in kwargs:
        spin1x = kwargs.pop('spin1x')
    else:
        spin1x = 0.
    if 'spin1y' in kwargs:
        spin1y = kwargs.pop('spin1y')
    else:
        spin1y = 0.
    if 'spin1z' in kwargs:
        spin1z = kwargs.pop('spin1z')
    else:
        spin1z = 0.
    if 'spin2x' in kwargs:
        spin2x = kwargs.pop('spin2x')
    else:
        spin2x = 0.
    if 'spin2y' in kwargs:
        spin2y = kwargs.pop('spin2y')
    else:
        spin2y = 0.
    if 'spin2z' in kwargs:
        spin2z = kwargs.pop('spin2z')
    else:
        spin2z = 0.
    if 'inclination' in kwargs:
        kwargs.pop('inclination')
    if 'distance' in kwargs:
        kwargs.pop('distance')
    if 'coa_phase' in kwargs:
        kwargs.pop('coa_phase')
    if 'eccentricity' in kwargs:
        kwargs.pop('eccentricity')

    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(
                                y0 = y0, y1 = y1, l0 = l0, l1 = l1, zS = zS, zL = zL,
                                mL = mL, lens_model_list = lens_model_list,
                                approx = approx, mass1 = mass1, mass2 = mass2,
                                delta_t = delta_t, delta_f = delta_f, f_lower = f_lower,
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
    
    y0 = kwargs['y0']
    y1 = kwargs['y1']
    l0 = kwargs['l0']
    l1 = kwargs['l1']
    zS = kwargs['zS']
    zL = kwargs['zL']
    mL = kwargs['mL']
    lens_model_list = kwargs['lens_model_list']
    if 'approx' in kwargs:
        approx = kwargs.pop('approx')
    else:
        approx = 'IMRPhenomD'
    mass1 = kwargs['mass1']
    mass2 = kwargs['mass2']
    delta_t = kwargs['delta_t']
    delta_f = kwargs['delta_f']
    f_lower = kwargs['f_lower']
    if 'spin1x' in kwargs:
        spin1x = kwargs.pop('spin1x')
    else:
        spin1x = 0.
    if 'spin1y' in kwargs:
        spin1y = kwargs.pop('spin1y')
    else:
        spin1y = 0.
    if 'spin1z' in kwargs:
        spin1z = kwargs.pop('spin1z')
    else:
        spin1z = 0.
    if 'spin2x' in kwargs:
        spin2x = kwargs.pop('spin2x')
    else:
        spin2x = 0.
    if 'spin2y' in kwargs:
        spin2y = kwargs.pop('spin2y')
    else:
        spin2y = 0.
    if 'spin2z' in kwargs:
        spin2z = kwargs.pop('spin2z')
    else:
        spin2z = 0.
    if 'inclination' in kwargs:
        kwargs.pop('inclination')
    if 'distance' in kwargs:
        kwargs.pop('distance')
    if 'coa_phase' in kwargs:
        kwargs.pop('coa_phase')
    if 'eccentricity' in kwargs:
        kwargs.pop('eccentricity')

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
    hc_tilde_lensed = TimeSeries(hc_tilde_lensed, delta_t=hc.delta_t)
    return hp_tilde_lensed, hc_tilde_lensed
