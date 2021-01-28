# lensGW-PyCBC-plugin
plugin for waveform generation using PyCBC

## Method to use:

### Method 1 :
- install PyCBC http://pycbc.org/pycbc/latest/html/install.html 
- install lenstronomy https://github.com/sibirrer/lenstronomy
- install lensGW https://github.com/SSingh087/lensGW/tree/main
- then follow these steps
```
%%shell
git clone https://github.com/SSingh087/lensGW-PyCBC-plugin.git
cd lensGW-PyCBC-plugin/
python setup.py install
```
***follow these steps in the same `virtualenv`**

### Method 2 :
```
%%shell

#Install PyCBC
virtualenv -p python3 env
source env/bin/activate
pip install --upgrade pip setuptools

git clone https://github.com/gwastro/pycbc.git

cd pycbc
pip install -r requirements.txt
pip install -r companion.txt
python setup.py install

cd ..

#Install lenstronomy
git clone https://github.com/gipagano/lenstronomy.git
cd lenstronomy
python setup.py install

#Install lensGW
git clone https://github.com/SSingh087/lensGW.git
cd lensGW
python setup.py install

cd..

#Install lensGW-PyCBC-plugin
git clone https://github.com/SSingh087/lensGW-PyCBC-plugin.git
cd lensGW-PyCBC-plugin/
python setup.py install
```
Then either run `test.py` script or in Python Shell
```
>>> from pycbc import waveform
>>> from lgw import *
>>> waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)
>>> hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(approximant="lensed", y0 = 0.1, y1 = 0.7937005, l0 = 0.5, 
                            l1 = 0,zS = 2.0,zL = 0.5,mL=[1e3,1e3], lens_model_list = ['POINT_MASS', 'POINT_MASS'],
                            approx='IMRPhenomD',mass1=500,mass2=500,spin1x=0.0,spin1y=0.0,
                            spin1z=0.3,spin2x=0.0,spin2y=0.0,spin2z=0.4,inclination=1.23,
                            distance=1000,coa_phase=2.45,delta_t=1.0/16384,delta_f=16384,f_lower=20, eccentricity=.3)
>>> print(hp_tilde_lensed)                          
```

