from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

description="Generate parameters for MC tuning"

setup(
    name="tuning_sampler",
    version="0.1.0",
    description=description,
    long_description=description,
    author="Xiangyang Ju",
    license="Apache License, Version 2.0",
    keywords=["generator", "MC tuning"],
    url="https://github.com/xju2/tuning_sampler.git",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'pyDOE',
    ],
    setup_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    scripts=[
        'scripts/create_diy_configs',
    ],
)
