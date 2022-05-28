import sys
sys.path.append('../lensGW/')
sys.path.append('../lensGW-PyCBC-plugin/')
from lgw import *

if __name__ == '__main__':
    source_ra=0.0
    source_dec=0.0
    lens_ra=0.1
    lens_dec=0.2
    zs=2.0
    zl=0.5
    ml=1e8
    lens_model_list=['POINT_MASS']
    mass1=30
    mass2=30
    delta_t=1.0/4096
    f_lower=9
    distance=6791.8106

    hp_tilde_lensed, hc_tilde_lensed = lensed_gw_td(
                                        source_ra=source_ra, source_dec=source_dec, 
                                        lens_ra=lens_ra, lens_dec=lens_dec, distance=distance,
                                        zs=zs, zl=zL, ml=mL, lens_model_list=lens_model_list,
                                        mass1=mass1, mass2=mass2, delta_t=delta_t, f_lower=f_lower)
    hp, hc = waveform.get_td_waveform(approximant='TaylorF2', mass1=mass1, distance=distance,
                                  mass2=mass2, delta_t=delta_t, f_lower=f_lower)
    import pylab
    hp_tilde_lensed.start_time = hp.start_time
    pylab.plot(hp_tilde_lensed.sample_times, hp_tilde_lensed)
    pylab.plot(hp.sample_times, hp)
    pylab.legend(ncol=2, fontsize=12)
    pylab.grid()
    pylab.savefig('a.png') 