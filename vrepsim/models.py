# -*- coding: utf-8 -*-
"""Interface to models simulated in V-REP.

Interface to models simulated in V-REP provides individual interfaces to the
following models:

- generic model;
- Pioneer P3-DX robot.
"""

import vrep

from vrepsim.constants import MISSING_HANDLE, REMOVED_OBJ_HANDLE
from vrepsim.exceptions import ConnectionError, ServerError
from vrepsim.objects import MotorArray, ProximitySensorArray, SceneObject


class Model(SceneObject):
    """Interface to a generic model simulated in V-REP."""

    def __init__(self, name, parent=None, vrep_sim=None):
        super(Model, self).__init__(name, parent, vrep_sim)

    def get_bbox_limits(self, prec=None):
        """Retrieve limits of model bounding box."""
        BBOX_LIMITS = (
            ('x_min', vrep.sim_objfloatparam_modelbbox_min_x),
            ('x_max', vrep.sim_objfloatparam_modelbbox_max_x),
            ('y_min', vrep.sim_objfloatparam_modelbbox_min_y),
            ('y_max', vrep.sim_objfloatparam_modelbbox_max_y),
            ('z_min', vrep.sim_objfloatparam_modelbbox_min_z),
            ('z_max', vrep.sim_objfloatparam_modelbbox_max_z)
            )

        if self._handle < 0:
            if self._handle == MISSING_HANDLE:
                raise RuntimeError(
                    "Could not retrieve limits of {} bounding box: missing "
                    "name or handle.".format(self._name))
            if self._handle == REMOVED_OBJ_HANDLE:
                raise RuntimeError("Could not retrieve limits of {} bounding "
                                   "box: object removed.".format(self._name))
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve limits of {} bounding box: not connected "
                "to V-REP remote API server.".format(self._name))
        bbox_limits = []
        for limit in BBOX_LIMITS:
            res, lim = vrep.simxGetObjectFloatParameter(
                client_id, self._handle, limit[1], vrep.simx_opmode_blocking)
            if res != vrep.simx_return_ok:
                raise ServerError("Could not retrieve {0} limit of {1} "
                                  "bounding box.".format(limit[0], self._name))
            if prec is not None:
                lim = round(lim, prec)  # limit may be slightly imprecise due
                                        # to the use of single-precision
                                        # floating-point format by V-REP
            bbox_limits.append(lim)
        bbox_limits = [[min_lim, max_lim]
                       for min_lim, max_lim
                       in zip(bbox_limits[::2], bbox_limits[1::2])]
        return bbox_limits

    def set_removed(self, recursive=False):
        """Set model removed status."""
        self._handle = REMOVED_OBJ_HANDLE
        if self._parent is not None:
            if not recursive:
                try:
                    self._parent.unregister_child(self)
                except ValueError:
                    pass
            self._parent = None
        for child in self._children:
            child.set_removed(recursive=True)
        self._children.clear()

    def remove(self):
        """Remove model from scene."""
        if self._handle < 0:
            if self._handle == MISSING_HANDLE:
                raise RuntimeError("Could not remove {}: missing name or "
                                   "handle.".format(self._name))
            if self._handle == REMOVED_OBJ_HANDLE:
                raise RuntimeError("Could not remove {}: object already "
                                   "removed.".format(self._name))
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not remove {}: not connected to V-REP remote API "
                "server.".format(self._name))
        res = vrep.simxRemoveModel(client_id, self._handle,
                                   vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not remove {}.".format(self._name))
        self.set_removed()


class PioneerBot(Model):
    """Interface to Pioneer P3-DX robot simulated in V-REP."""

    def __init__(self, name, us_sensor_names, motor_names, parent=None,
                 vrep_sim=None):
        super(PioneerBot, self).__init__(name, parent, vrep_sim)
        self.us_sensors = ProximitySensorArray(us_sensor_names, self, vrep_sim)
        self.wheels = MotorArray(motor_names, self, vrep_sim)
