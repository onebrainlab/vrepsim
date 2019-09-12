# -*- coding: utf-8 -*-
"""Interface to models simulated in V-REP.

Interface to models simulated in V-REP provides individual interfaces to the
following models:

- generic model;
- Pioneer P3-DX robot.
"""

import vrep

from vrepsim.constants import VREP_FLOAT_PREC
from vrepsim.exceptions import ServerError
from vrepsim.objects import MotorArray, ProximitySensorArray, SceneObject


class Model(SceneObject):
    """Interface to a generic model simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(Model, self).__init__(vrep_sim, name)

    def get_bbox_limits(self, prec=VREP_FLOAT_PREC):
        """Retrieve limits of model bounding box."""
        BBOX_LIMITS = (
            ('x_min', vrep.sim_objfloatparam_modelbbox_min_x),
            ('x_max', vrep.sim_objfloatparam_modelbbox_max_x),
            ('y_min', vrep.sim_objfloatparam_modelbbox_min_y),
            ('y_max', vrep.sim_objfloatparam_modelbbox_max_y),
            ('z_min', vrep.sim_objfloatparam_modelbbox_min_z),
            ('z_max', vrep.sim_objfloatparam_modelbbox_max_z)
            )

        bbox_limits = []
        for limit in BBOX_LIMITS:
            res, lim = vrep.simxGetObjectFloatParameter(
                self.client_id, self._handle, limit[1],
                vrep.simx_opmode_blocking)
            if res != vrep.simx_return_ok:
                raise ServerError("Could not retrieve {0} limit of {1} "
                                  "bounding box.".format(limit[0], self._name))
            if prec is not None:
                lim = round(lim, prec)  # limit may be slightly imprecise
                                        # (about the 6th digit after the
                                        # decimal point)
            bbox_limits.append(lim)
        bbox_limits = [[min_lim, max_lim]
                       for min_lim, max_lim
                       in zip(bbox_limits[::2], bbox_limits[1::2])]
        return bbox_limits

    def remove(self):
        """Remove model from scene."""
        res = vrep.simxRemoveModel(self.client_id, self._handle,
                                   vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not remove {}.".format(self._name))
        self._name = "_Removed_"
        self._handle = -1


class PioneerBot(Model):
    """Interface to Pioneer P3-DX robot simulated in V-REP."""

    def __init__(self, vrep_sim, name, us_sensor_names, motor_names):
        super(PioneerBot, self).__init__(vrep_sim, name)
        self.us_sensors = ProximitySensorArray(vrep_sim, us_sensor_names)
        self.wheels = MotorArray(vrep_sim, motor_names)
