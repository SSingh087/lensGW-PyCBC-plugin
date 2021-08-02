#!/usr/bin/env python

from setuptools import Extension, setup, Command, find_packages
from codecs import open

VERSION = '1.0.0'

def readme():
    with open('README.md') as f:
        return f.read()

setup ( 
    name = 'pycbc-lensGW',
    version = VERSION,
    description = 'lensGW plugin for PyCBC',
    long_description = readme(),
    author = 'Shashwat Singh',
    author_email = 'shashwat98singh@gmail.com',
    download_url = 'https://github.com/SSingh087/lensGW-PyCBC-plugin',
    keywords = ['pycbc', 'signal processing', 'gravitational waves','strong gravitational lensing'],
    install_requires = ['pycbc','lensGW'],
    py_modules = ['lgw'],
    entry_points = {"pycbc.waveform.td":"lgw = lgw:lensed_gw_td",
                    "pycbc.waveform.fd":"lgw = lgw:lensed_gw_fd"},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
