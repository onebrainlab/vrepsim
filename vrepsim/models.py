# -*- coding: utf-8 -*-
"""Interface to models simulated in V-REP.

Interface to models simulated in V-REP provides individual interfaces to the
following models:

- generic model;
- Pioneer P3-DX robot.
"""

import vrep

from vrepsim.exceptions import SimulationError
from vrepsim.objects import MotorArray, ProximitySensorArray, SceneObject


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
        self.us_sensors = ProximitySensorArray(vrep_sim, us_sensor_names)
        self.wheels = MotorArray(vrep_sim, motor_names)
