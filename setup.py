#!/usr/bin/env python

from glob import glob
from setuptools import setup

__copyright__ = "Copyright 2019, The METGEM Project"
__license__ = "Apache License2"
__version__ = "0.0.2"
__maintainer__ = "Preecha Patumcharoenpol"

long_description = ("Community Metabolic Network builder is the"
                    "...")

setup(name='metgem',
      version=__version__,
      description=('METGEM - Community metabolic network reconstruction from meta-omics data'
                   'beta'),
      maintainer=__maintainer__,
      url='https://github.com/yumyai/MetGEM',
      packages=['metgem/', 'metgem/tasks'],
      scripts=glob('scripts/*'),
      include_package_data=True,
      package_data={'metgem': ['default_files/models/*/*.tar.gz']},
      install_requires=['numpy',
                        'pandas',
                        'joblib'],
long_description=long_description)
