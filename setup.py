#!/usr/bin/env python
"""
setup.py file for reverse chirp example pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

VERSION = '0.0.dev0'

setup (
    name = 'pycbc-lensGW',
    version = VERSION,
    description = 'lensGW plugin for PyCBC',
    long_description = open('descr.rst').read(),
    author = 'Shashwat Singh',
    author_email = 'shashwat98singh@gmail.com',
    url = 'www.bosex.org',
    download_url = 'https://github.com/SSingh087/lensGW-PyCBC-plugin%s' % VERSION,
    keywords = ['pycbc', 'signal processing', 'gravitational waves','strong gravitational lensing'],
    install_requires = ['pycbc','lensGW'],
    py_modules = ['lgw'],
    entry_points = {"pycbc.waveform.td":"revchirp = revchirp:reverse_chirp_td",
                    "pycbc.waveform.fd":"revchirp = revchirp:reverse_chirp_fd"},
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
