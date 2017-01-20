# -*- coding: utf-8 -*-
"""Interface to scene objects simulated in V-REP.

Interface to scene objects simulated in V-REP provides individual interfaces to
the following scene objects:

- generic scene object;
- dummy object;
- motor (motorized joint);
- proximity sensor.

It also provides interfaces to the following arrays of scene objects:

- array of generic sensors;
- array of proximity sensors.
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
        return self._handle if self._handle != -1 else None

    @property
    def name(self):
        """Object name."""
        return self._name if self._name != "_Unnamed_" else None

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


class Motor(SceneObject):
    """Interface to motor (motorized joint) simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(Motor, self).__init__(vrep_sim, name)

    def set_velocity(self, velocity):
        """Set motor velocity."""
        res = vrep.simxSetJointTargetVelocity(
            self._client_id, self._handle, velocity, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError("Could not update {} "
                                  "velocity.".format(self._name))


class ProximitySensor(SceneObject):
    """Interface to proximity sensor simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(ProximitySensor, self).__init__(vrep_sim, name)

    def get_inv_distance(self):
        """Retrieve distance to the detected point inverted such that smaller
        values correspond to further distances.
        """
        res, detect, point, _, _ = vrep.simxReadProximitySensor(
            self._client_id, self._handle, vrep.simx_opmode_blocking)
        if res == vrep.simx_return_ok:
            if detect:
                return 1.0 - point[2]  # distance inverted
            else:
                return 0.0
        elif res == vrep.simx_return_novalue_flag:
            return 0.0
        else:
            raise SimulationError("Could not retrieve data from "
                                  "{}.".format(self._name))


class SensorArray(object):
    """Interface to an array of generic sensors simulated in V-REP."""

    def __init__(self):
        self._sensors = []

    def __contains__(self, item):
        """Check if specific sensor belongs to the array."""
        return item in self._sensors

    def __getitem__(self, key):
        """Retrieve specific sensor."""
        return self._sensors[key]

    def __iter__(self):
        """Retrieve iterator over sensors."""
        return iter(self._sensors)

    def __len__(self):
        """Retrieve number of sensors."""
        return len(self._sensors)


class ProximitySensorArray(SensorArray):
    """Interface to an array of proximity sensors simulated in V-REP."""

    def __init__(self, vrep_sim, sensor_names):
        super(ProximitySensorArray, self).__init__()
        if sensor_names:
            self._sensors = [ProximitySensor(vrep_sim, name)
                             for name in sensor_names]

    def get_inv_distances(self):
        """Retrieve distances to the detected points by all sensors inverted
        such that smaller values correspond to further distances.
        """
        return [sensor.get_inv_distance() for sensor in self._sensors]
