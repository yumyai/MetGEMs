#!/usr/bin/env python

from setuptools import setup
from glob import glob

__copyright__ = "Copyright 2018, The CMNet Project"
__license__ = "Apache 2.0"
__version__ = "0.0.0"
__maintainer__ = "Preecha Patumcharoenpol"

long_description = ("No, not ready yet."
                    "I said no.")

setup(name='fpdq',
      version=__version__,
      description=('CMNet - Community Metabolic Network analysis from meta-omics data'
                   'beta'),
      maintainer=__maintainer__,
      url='https://github.com/yumyai/CMNet',
      packages=['cmnet'],
      scripts=glob('scripts/*py'),
      install_requires=['numpy',
                        'h5py',
                        'joblib',
                        'networkx',
                        'biom-format'],
long_description=long_description)
