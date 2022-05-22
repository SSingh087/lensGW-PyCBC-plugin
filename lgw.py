
# Copyright (C) 2021  Shashwat Singh
#
#
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

import sys
sys.path.append('../lensGW/')


from lensGW.waveform.waveform_utils import lens_waveform_model
from lensGW.amplification_factor.amplification_factor import geometricalOpticsMagnification
from lensGW.utils.utils import get_lensed_gws
from pycbc.types.timeseries import TimeSeries
from pycbc.types.frequencyseries import FrequencySeries
from pycbc import waveform
from numpy import array, float64

def eval_lensed_waveform(mL, lens_ra, lens_dec, zs, zl, source_ra, source_dec, is_td, **kwargs):
    """
    Evaluates the lensed waveform with respect to the given parameters
    :param mL: lens mass
    :type mL: float
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
    :param: **kwargs: other lens parameters
    
    :return:
    :param: hp_tilde_lensed, hp_tilde_lensed, delta_f (only for Frequecy Domain)
    :rtype: TimeSeries, TimeSeries, float
    """
    
    optim = False #kwargs['optim']
    lens_model_list = kwargs['lens_model_list']
    
    Img_ra, Img_dec, kwargs_lens_list, solver_kwargs = lens_waveform_model.eval_param(
                                                            source_ra, source_dec, lens_ra, lens_dec, 
                                                            zs, zl, mL, lens_model_list, optim)

    if "approximant" in kwargs:
        kwargs.pop("approximant")
    if is_td == 'True':
        # currently works only for the dominant 2,2 mode 
        hp_td, hc_td = waveform.get_td_waveform(approximant='TaylorF2', **kwargs)
        hp_fd, hc_fd = hp_td.to_frequencyseries(), hc_td.to_frequencyseries()
    else: 
        hp_fd, hc_fd = waveform.get_fd_waveform(approximant='TaylorF2', **kwargs)

    freq = hp_fd.sample_frequencies.data #since hp.sample_frequencies.data == hc.sample_frequencies.data (always)
    Fmag = geometricalOpticsMagnification(freq, Img_ra, Img_dec,
                                           source_ra, source_dec,
                                           zl, zs, lens_model_list, 
                                           kwargs_lens_list,
                                           diff         = None,
                                           scaled       = solver_kwargs['Scaled'],
                                           scale_factor = solver_kwargs['ScaleFactor'],
                                           cosmo        = None)
                                           
    #------------return numpy values---------------#
    hp_fd_tilde_lensed, hc_fd_tilde_lensed = get_lensed_gws(Fmag, hp_fd.data, hc_fd.data)
    
    #------------convert to pycbc.FrequencySeries---------------#

    hp_fd_tilde_lensed = FrequencySeries(hp_fd_tilde_lensed, delta_f=hp_fd.delta_f)
    hc_fd_tilde_lensed = FrequencySeries(hc_fd_tilde_lensed, delta_f=hc_fd.delta_f)
    
    return hp_fd_tilde_lensed, hc_fd_tilde_lensed


def lensed_gw_fd(mL=1e8, lens_ra=0.0, lens_dec=0.0, zs=1.0, zl=0.5, source_ra=0.5, source_dec=0.5, **kwargs):
    """
    Returns the lensed waveform in Frequecy domain
    :param mL: lens mass (default: 1e8)
    :type mL: float
    :param source_ra: Right accession of the source of GW (in radians) (default: 0.0)
    :type source_ra: float
    :param source_dec: Declination of the source of GW (in radians) (default: 0.0)
    :type source_dec: float
    :param lens_ra: Right accession of the lens (in radians) (default: 0.5)
    :type lens_ra: array
    :param lens_dec: Declination of the lens (in radians) (default: 0.5)
    :type lens_dec: array
    :param zl: lens redshift (default: 0.5)
    :type zl: float
    :param zs: source redshift (default: 1)
    :type zs: float
    :param n_images: Number of images to output (should be less than total images found)
    :type n_images: integer
    :param: **kwargs: other lens parameters
    """

    return eval_lensed_waveform([mL], [lens_ra], [lens_dec], zs, zl, source_ra, source_dec,
                        is_td='False', **kwargs)

def lensed_gw_td(mL=1e8, lens_ra=0.5, lens_dec=0, zs=2.0, zl=0.5, source_ra=0.3, source_dec=0.3, **kwargs):
    """
    Returns the lensed waveform in Time domain
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
    :param: **kwargs: other lens parameters
    """

    hp_fd_tilde_lensed, hc_fd_tilde_lensed = eval_lensed_waveform([mL], [lens_ra], [lens_dec], zs, zl, source_ra, source_dec,
                                                    is_td='True', **kwargs)
    hp_td_tilde_lensed = hp_fd_tilde_lensed.to_timeseries(delta_t=hp_fd_tilde_lensed.delta_t)
    hc_td_tilde_lensed = hc_fd_tilde_lensed.to_timeseries(delta_t=hp_fd_tilde_lensed.delta_t)
    return hp_td_tilde_lensed, hc_td_tilde_lensed

