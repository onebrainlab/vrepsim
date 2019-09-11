# -*- coding: utf-8 -*-
"""Exceptions raised by V-REPSim.

Exceptions include:

- ConnectionError - raised during connecting to V-REP remote API server;
- ServerError - raised during communication with V-REP remote API server;
- SimulationError - raised during simulation.
"""


class VREPSimError(Exception):
    """Base V-REPSim exception."""
    pass


class ConnectionError(VREPSimError, RuntimeError):
    """Error during connecting to V-REP remote API server."""
    pass


class ServerError(VREPSimError, RuntimeError):
    """Error during communication with V-REP remote API server."""
    pass


class SimulationError(VREPSimError, RuntimeError):
    """Error during simulation."""
    pass
