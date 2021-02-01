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

def lensed_gw_fd(y0 = 0,y1 = 0,l0 = 0,l1 = 0,zS = 0,zL = 0,mL = [100,100],lens_model_list = [],
                approx='IMRPhenomD',mass1=50,mass2=50,spin1x=0.0,spin1y=0.0,
                spin1z=0.0,spin2x=0.0,spin2y=0.0,spin2z=0.0,inclination=0.0,
                distance=500,coa_phase=0.0,delta_t=1.0/4096,delta_f=4096,f_lower=30,
                eccentricity=0,**kwds):

    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(
                y0 = 0,y1 = 0, l0 = 0,l1 = 0,zS = 0,zL = 0,mL = [100,100], lens_model_list = [],
                approx='IMRPhenomD', mass1=50, mass2=50, delta_t=1.0/4096, delta_f=4096, f_lower=30,
                spin1x=0.0,spin1y=0.0, spin1z=0.0, spin2x=0.0, spin2y=0.0, spin2z=0.0,
                inclination=0.0, distance=500, coa_phase=0.0, eccentricity=0
                )
    
    return hp_tilde_lensed.to_frequencyseries(), hc_tilde_lensed.to_frequencyseries()

def lensed_gw_td(y0 = 0,y1 = 0, l0 = 0,l1 = 0,zS = 0,zL = 0,mL = [100,100], lens_model_list = [],
                approx='IMRPhenomD', mass1=50, mass2=50, delta_t=1.0/4096, delta_f=4096, f_lower=30,
                spin1x=0.0,spin1y=0.0, spin1z=0.0, spin2x=0.0, spin2y=0.0, spin2z=0.0,
                inclination=0.0, distance=500, coa_phase=0.0, eccentricity=0, **kwds):
    
    from lensGW.waveform.waveform_utils import lens_waveform_model
    from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
    from lensGW.utils.utils import get_lensed_gws
    from pycbc.types.timeseries import TimeSeries
    from pycbc import waveform
    
    Img_ra, Img_dec, source_pos_x, source_pos_y,\
                _, _, _, kwargs_lens_list = lens_waveform_model(None).eval_param(
                                                            y0,y1,l0,l1,zS,zL,mL,lens_model_list)
    if 'approximant' in kwds:
        kwds.pop("approximant")
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