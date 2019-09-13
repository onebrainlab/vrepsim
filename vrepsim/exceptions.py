# -*- coding: utf-8 -*-
"""Exceptions raised by V-REPSim.

Exceptions include:

- ConnectionError - related to connection to V-REP remote API server;
- ServerError - related to communication with V-REP remote API server;
- SimulationError - related to simulation.
"""


class VREPSimError(Exception):
    """Base V-REPSim exception."""
    pass


class ConnectionError(VREPSimError, RuntimeError):
    """Error related to connection to V-REP remote API server."""
    pass


class ServerError(VREPSimError, RuntimeError):
    """Error related to communication with V-REP remote API server."""
    pass


class SimulationError(VREPSimError, RuntimeError):
    """Error related to simulation."""
    pass
