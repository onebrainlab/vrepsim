# -*- coding: utf-8 -*-
"""Assorted base data structures.

Assorted base data structures provide a generic communicator with V-REP
simulator.
"""

from vrepsim.simulator import get_default_simulator


class Communicator(object):
    """Generic communicator with V-REP simulator."""

    def __init__(self, vrep_sim):
        if vrep_sim is not None:
            self._vrep_sim = vrep_sim
        else:
            self._vrep_sim = get_default_simulator(raise_on_none=True)

    @property
    def client_id(self):
        """Client ID."""
        return self._vrep_sim.client_id

    @property
    def vrep_sim(self):
        """Interface to V-REP remote API server."""
        return self._vrep_sim
