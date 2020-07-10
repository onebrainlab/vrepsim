#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os

setup_path = os.path.abspath(os.path.dirname(__file__))


def read_description(filename):
    with open(os.path.join(setup_path, filename), 'r') as description_file:
        return description_file.read()


setup(
    name="vrepsim",
    version='0.4.0',
    author="Przemyslaw (Mack) Nowak",
    author_email="pnowak.mack@gmail.com",
    description="High-level Python interface to V-REP simulator",
    long_description=read_description("README.md"),
    url="https://github.com/macknowak/vrepsim",
    license="GNU General Public License v3 or later (GPLv3+)",
    packages=['vrepsim'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
        ]
    )
