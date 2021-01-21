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

