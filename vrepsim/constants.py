# -*- coding: utf-8 -*-
"""Assorted constants.

Assorted constants provide the following constants:

- constant related to substitute names for instances of interfaces;
- constant related to rounding float values returned by the V-REP remote API.
"""

EMPTY_NAME = "*Unnamed*"  # substitute name for an instance of an interface to
                          # a collection or a scene object whose name has not
                          # been specified during initialization
VREP_FLOAT_PREC = 4  # default precision for rounding float values returned by
                     # several functions from the V-REP remote API
