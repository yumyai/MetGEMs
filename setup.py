#!/usr/bin/env python

from setuptools import setup
from glob import glob

__copyright__ = "Copyright 2019, The CMNet Project"
__license__ = "Apache License2"
__version__ = "0.0.0a"
__maintainer__ = "Preecha Patumcharoenpol"

long_description = ("Community Metabolic Network builder is the"
                    "...")

setup(name='cmnet',
      version=__version__,
      description=('CMNet - Community metabolic network reconstruction from meta-omics data'
                   'beta'),
      maintainer=__maintainer__,
      url='https://github.com/yumyai/CMNet',
      packages=['cmnet'],
      scripts=glob('scripts/*'),
      package_data={'cmnet':
                    ['ext-tools/*R']},
      install_requires=['numpy',
                        'pandas',
                        'joblib'],
long_description=long_description)
