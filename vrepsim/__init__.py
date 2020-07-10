# -*- coding: utf-8 -*-
"""V-REPSim: V-REP simulator Python interface.

V-REPSim provides a high-level interface based on the V-REP remote API for
controlling V-REP simulations from an external Python program.

For V-REPSim to operate successfully, the following V-REP files (or,
alternatively, links to them) have to exist in the current directory so that
the V-REP remote API could be used (here, V-REP_DIR denotes the directory in
which V-REP is installed):

- vrep.py (original file in: V-REP_DIR/programming/remoteApiBindings/python/
  python/);
- vrepConst.py (original file in: V-REP_DIR/programming/remoteApiBindings/
  python/python/);
- [remoteApi.so | remoteApi.dylib | remoteApi.dll] (original file in:
  V-REP_DIR/programming/remoteApiBindings/lib/lib/[32Bit | 64Bit]/).
"""

__version__ = '0.4.0'
__author__ = "Przemyslaw (Mack) Nowak"

import sys
import warnings

if sys.version_info[0] == 2:
    warnings.warn("Support for Python 2 is deprecated.", DeprecationWarning)

from .collections import Collection
from .models import Model, PioneerBot
from .objects import (Dummy, Motor, MotorArray, ProximitySensor,
                      ProximitySensorArray, SceneObject, SensorArray,
                      VisionSensor)
from .simulator import Simulator, get_default_simulator
from . import collections, models, nengo, objects, simulator
