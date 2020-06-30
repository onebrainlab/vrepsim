#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name="vrepsim",
    version='0.4.0.dev1',
    author="Przemyslaw (Mack) Nowak",
    author_email="pnowak.mack@gmail.com",
    description="High-level Python interface to V-REP simulator",
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
