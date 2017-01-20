# -*- coding: utf-8 -*-
"""Interface to models simulated in V-REP.

Interface to models simulated in V-REP provides individual interfaces to the
following models:

- generic model;
- Pioneer P3-DX robot.
"""

import vrep

from vrepsim.exceptions import SimulationError
from vrepsim.objects import SceneObject


class Model(SceneObject):
    """Interface to a generic model simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(Model, self).__init__(vrep_sim, name)

    def _get_obj_handle(self, obj_name):
        """Retrieve handle to the specified component object."""
        if not obj_name:
            raise SimulationError("Could not retrieve handle to _Unnamed_.")
        res, handle = vrep.simxGetObjectHandle(self._client_id, obj_name,
                                               vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve handle to {}.".format(obj_name))
        return handle

    def _get_obj_handles(self, obj_names):
        """Retrieve handles to the specified component objects."""
        return [self._get_obj_handle(obj_name) for obj_name in obj_names]


class PioneerBot(Model):
    """Interface to Pioneer P3-DX robot simulated in V-REP."""

    def __init__(self, vrep_sim, name, us_sensor_names, motor_names):
        super(PioneerBot, self).__init__(vrep_sim, name)
        if us_sensor_names:
            self._us_sensor_names = us_sensor_names
            self._us_sensor_handles = self._get_obj_handles(
                self._us_sensor_names)
            self._n_us_sensors = len(self._us_sensor_names)
        else:
            self._us_sensor_names = []
            self._us_sensor_handles = []
            self._n_us_sensors = 0
        if motor_names:
            self._motor_names = motor_names
            self._motor_handles = self._get_obj_handles(self._motor_names)
            self._n_motors = len(self._motor_names)
        else:
            self._motor_names = []
            self._motor_handles = []
            self._n_motors = 0

    @property
    def n_motors(self):
        """Number of used motors."""
        return self._n_motors

    @property
    def n_us_sensors(self):
        """Number of used ultrasonic sensors."""
        return self._n_us_sensors

    def get_inv_us_sensor_data(self):
        """Retrieve ultrasonic sensor data transformed such that smaller
        values correspond to further distances.
        """
        sensor_data = []
        for s, sensor_handle in enumerate(self._us_sensor_handles):
            res, detect, point, _, _ = vrep.simxReadProximitySensor(
                self._client_id, sensor_handle, vrep.simx_opmode_blocking)
            if res == vrep.simx_return_ok:
                if detect:
                    sensor_data.append(1.0-point[2])  # data transformed
                else:
                    sensor_data.append(0.0)
            elif res == vrep.simx_return_novalue_flag:
                sensor_data.append(0.0)
            else:
                raise SimulationError("Could not retrieve data from "
                                      "{}.".format(self._us_sensor_names[s]))
        return sensor_data

    def set_motor_speeds(self, motor_speeds):
        """Set motor speeds."""
        for m, motor_handle in enumerate(self._motor_handles):
            res = vrep.simxSetJointTargetVelocity(
                self._client_id, motor_handle, motor_speeds[m],
                vrep.simx_opmode_blocking)
            if res != vrep.simx_return_ok:
                raise SimulationError("Could not update {} motor "
                                      "speed.".format(self._motor_names[m]))
