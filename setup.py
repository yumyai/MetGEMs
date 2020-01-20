#!/usr/bin/env python

from setuptools import setup
from glob import glob

__copyright__ = "Copyright 2019, The GEMMET Project"
__license__ = "Apache License2"
__version__ = "0.0.1a"
__maintainer__ = "Preecha Patumcharoenpol"

long_description = ("Community Metabolic Network builder is the"
                    "...")

setup(name='gemmet',
      version=__version__,
      description=('GEMMET - Community metabolic network reconstruction from meta-omics data'
                   'beta'),
      maintainer=__maintainer__,
      url='https://github.com/yumyai/GEMMET',
      packages=['gemmet', 'gemmet/tasks'],
      scripts=glob('scripts/*'),
      include_package_data=True,
      package_data={'gemmet': ['default_files/models/*.tar.gz']},
      install_requires=['numpy',
                        'pandas',
                        'joblib'],
long_description=long_description)
