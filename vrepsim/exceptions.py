# -*- coding: utf-8 -*-
"""Exceptions raised by V-REPSim.

Exceptions include:

- ServerError - raised during communication with V-REP remote API server;
- SimulationError - raised during simulation.
"""


class VREPSimError(Exception):
    """Base V-REPSim exception."""
    pass


class ServerError(VREPSimError, RuntimeError):
    """Error during communication with V-REP remote API server."""
    pass


class SimulationError(VREPSimError, RuntimeError):
    """Error during simulation."""
    pass
