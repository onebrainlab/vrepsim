# -*- coding: utf-8 -*-
"""Interface to scene objects simulated in V-REP.

Interface to scene objects simulated in V-REP provides individual interfaces to
the following scene objects:

- generic scene object;
- dummy object.
"""

import vrep

from vrepsim.exceptions import SimulationError


class SceneObject(object):
    """Interface to a generic scene object simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        self._client_id = vrep_sim.client_id
        if name:
            self._name = name
            self._handle = self._get_handle()
        else:
            self._name = "_Unnamed_"
            self._handle = -1

    @property
    def handle(self):
        """Object handle."""
        return self._handle

    @property
    def name(self):
        """Object name."""
        return self._name

    def get_orientation(self):
        """Retrieve object orientation specified as Euler angles about x, y,
        and z axes of the absolute reference frame, each angle between -pi
        and pi.
        """
        res, orientation = vrep.simxGetObjectOrientation(
            self._client_id, self._handle, -1, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve orientation of {}.".format(self._name))
        return orientation

    def get_position(self):
        """Retrieve object position."""
        res, position = vrep.simxGetObjectPosition(
            self._client_id, self._handle, -1, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve position of {}.".format(self._name))
        return position

    def _get_handle(self):
        """Retrieve object handle."""
        res, handle = vrep.simxGetObjectHandle(self._client_id, self._name,
                                               vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve handle to {}.".format(self._name))
        return handle


class Dummy(SceneObject):
    """Interface to dummy object simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(Dummy, self).__init__(vrep_sim, name)
