# -*- coding: utf-8 -*-
"""Interface to collections simulated in V-REP.

Interface to collections simulated in V-REP provides an interface to a
collection of scene objects simulated in V-REP.
"""

import vrep

from vrepsim.exceptions import SimulationError


class Collection(object):
    """Interface to a collection of scene objects simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        self._client_id = vrep_sim.client_id
        self._name = name
        self._handle = self._get_handle()

    @property
    def handle(self):
        """Collection handle."""
        return self._handle

    @property
    def name(self):
        """Collection name."""
        return self._name

    def get_names(self):
        """Retrieve names of component scene objects."""
        res, _, _, _, names = vrep.simxGetObjectGroupData(
            self._client_id, self._handle, 0, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve names of {}.".format(self._name))
        return names

    def get_orientations(self):
        """Retrieve orientations of component scene objects, specified as Euler
        angles about x, y, and z axes of the absolute reference frame, each
        angle between -pi and pi.
        """
        res, _, _, orientations, _ = vrep.simxGetObjectGroupData(
            self._client_id, self._handle, 5, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve orientations of {}.".format(self._name))
        return [orientations[o*3:(o+1)*3]
                for o in range(len(orientations) / 3)]

    def get_positions(self):
        """Retrieve positions of component scene objects."""
        res, _, _, positions, _ = vrep.simxGetObjectGroupData(
            self._client_id, self._handle, 3, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve positions of {}.".format(self._name))
        return [positions[p*3:(p+1)*3] for p in range(len(positions) / 3)]

    def _get_handle(self):
        """Retrieve collection handle."""
        res, handle = vrep.simxGetCollectionHandle(self._client_id, self._name,
                                                   vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve handle to {}.".format(self._name))
        return handle
