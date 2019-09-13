# -*- coding: utf-8 -*-
"""Interface to scene objects simulated in V-REP.

Interface to scene objects simulated in V-REP provides individual interfaces to
the following scene objects:

- generic scene object;
- dummy object;
- motor (motorized joint);
- proximity sensor;
- vision sensor.

It also provides interfaces to the following arrays of scene objects:

- array of motors;
- array of generic sensors;
- array of proximity sensors.
"""

import vrep

from vrepsim.base import Communicator
from vrepsim.constants import VREP_FLOAT_PREC
from vrepsim.exceptions import ConnectionError, ServerError, SimulationError


class SceneObject(Communicator):
    """Interface to a generic scene object simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(SceneObject, self).__init__(vrep_sim)
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

    @staticmethod
    def get_handle(scene_obj, name):
        """Retrieve object handle."""
        if scene_obj is None:
            return -1
        elif isinstance(scene_obj, int):
            return scene_obj
        elif isinstance(scene_obj, SceneObject):
            handle = scene_obj.handle
            if handle is None:
                raise ValueError("Handle of {} is invalid.".format(name))
            return handle
        else:
            raise TypeError("Type of {} is not supported.".format(name))

    def call_script_func(self, funcname, script_type='customization',
                         args_int=[], args_float=[], args_string=[],
                         args_buf=bytearray()):
        """Call function from associated script."""
        ASSOC_SCRIPT_TYPES = {
            'child': vrep.sim_scripttype_childscript,
            'customization': vrep.sim_scripttype_customizationscript
            }

        # Validate script type
        try:
            vrep_script_type = ASSOC_SCRIPT_TYPES[script_type]
        except KeyError:
            raise ValueError("Script type is not supported.")

        # Call function from the script
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not call function {0} from {1} script associated with "
                "{2}: not connected to V-REP remote API server."
                "".format(funcname, script_type, self._name))
        res, rets_int, rets_float, rets_string, rets_buf = \
            vrep.simxCallScriptFunction(
                client_id, self._name, vrep_script_type, funcname, args_int,
                args_float, args_string, args_buf, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not call function {0} from {1} script associated with "
                "{2}.".format(funcname, script_type, self._name))
        return rets_int, rets_float, rets_string, rets_buf

    def copy_paste(self):
        """Copy and paste object."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not copy and paste {}: not connected to V-REP remote "
                "API server.".format(self._name))
        res, handles = vrep.simxCopyPasteObjects(client_id, [self._handle],
                                                 vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not copy and paste {}.".format(self._name))
        return handles[0]

    def get_bbox_limits(self, prec=VREP_FLOAT_PREC):
        """Retrieve limits of object bounding box."""
        BBOX_LIMITS = (
            ('x_min', vrep.sim_objfloatparam_objbbox_min_x),
            ('x_max', vrep.sim_objfloatparam_objbbox_max_x),
            ('y_min', vrep.sim_objfloatparam_objbbox_min_y),
            ('y_max', vrep.sim_objfloatparam_objbbox_max_y),
            ('z_min', vrep.sim_objfloatparam_objbbox_min_z),
            ('z_max', vrep.sim_objfloatparam_objbbox_max_z)
            )

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
                lim = round(lim, prec)  # limit may be slightly imprecise
                                        # (about the 6th digit after the
                                        # decimal point)
            bbox_limits.append(lim)
        bbox_limits = [[min_lim, max_lim]
                       for min_lim, max_lim
                       in zip(bbox_limits[::2], bbox_limits[1::2])]
        return bbox_limits

    def get_orientation(self, relative=None):
        """Retrieve object orientation specified as Euler angles about x, y,
        and z axes of the reference frame, each angle between -pi and pi.
        """
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve orientation of {}: not connected to V-REP "
                "remote API server.".format(self._name))
        relative_handle = SceneObject.get_handle(relative, "relative")
        res, orientation = vrep.simxGetObjectOrientation(
            client_id, self._handle, relative_handle,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve orientation of {}.".format(self._name))
        return orientation

    def set_orientation(self, orientation, relative=None, allow_in_sim=False):
        """Set object orientation specified as Euler angles about x, y, and z
        axes of the reference frame, each angle between -pi and pi.
        """
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not set orientation of {}: not connected to V-REP "
                "remote API server.".format(self._name))
        if not allow_in_sim and self.vrep_sim.is_sim_started():
            raise SimulationError(
                "Could not set orientation of {}: setting orientation not "
                "allowed during simulation.".format(self._name))
        relative_handle = SceneObject.get_handle(relative, "relative")
        res = vrep.simxSetObjectOrientation(
            client_id, self._handle, relative_handle, orientation,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not set orientation of {}.".format(self._name))

    def get_parent_handle(self):
        """Retrieve handle to object parent."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve handle to the parent of {}: not connected "
                "to V-REP remote API server.".format(self._name))
        res, handle = vrep.simxGetObjectParent(client_id, self._handle,
                                               vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve handle to the parent of "
                              "{}.".format(self._name))
        return handle

    def set_parent(self, parent=None, keep_pos=True):
        """Set object parent."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not set parent of {}: not connected to V-REP remote "
                "API server.".format(self._name))
        parent_handle = SceneObject.get_handle(parent, "parent")
        res = vrep.simxSetObjectParent(client_id, self._handle, parent_handle,
                                       keep_pos, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not set parent of {}.".format(self._name))

    def get_position(self, relative=None):
        """Retrieve object position."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve position of {}: not connected to V-REP "
                "remote API server.".format(self._name))
        relative_handle = SceneObject.get_handle(relative, "relative")
        res, position = vrep.simxGetObjectPosition(
            client_id, self._handle, relative_handle,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve position of {}.".format(self._name))
        return position

    def set_position(self, position, relative=None, allow_in_sim=False):
        """Set object position."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not set position of {}: not connected to V-REP remote "
                "API server.".format(self._name))
        if not allow_in_sim and self.vrep_sim.is_sim_started():
            raise SimulationError(
                "Could not set position of {}: setting position not allowed "
                "during simulation.".format(self._name))
        relative_handle = SceneObject.get_handle(relative, "relative")
        res = vrep.simxSetObjectPosition(
            client_id, self._handle, relative_handle, position,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not set position of {}.".format(self._name))

    def remove(self):
        """Remove object from scene."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not remove {}: not connected to V-REP remote API "
                "server.".format(self._name))
        res = vrep.simxRemoveObject(client_id, self._handle,
                                    vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not remove {}.".format(self._name))
        self._name = "_Removed_"
        self._handle = -1

    def _get_handle(self):
        """Retrieve object handle."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve handle to {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, handle = vrep.simxGetObjectHandle(client_id, self._name,
                                               vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
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
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not set {} velocity: not connected to V-REP remote API "
                "server.".format(self._name))
        res = vrep.simxSetJointTargetVelocity(
            client_id, self._handle, velocity, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not set {} velocity.".format(self._name))


class ProximitySensor(SceneObject):
    """Interface to proximity sensor simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(ProximitySensor, self).__init__(vrep_sim, name)

    def get_inv_distance(self):
        """Retrieve distance to the detected point inverted such that smaller
        values correspond to further distances.
        """
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve data from {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, detect, point, _, _ = vrep.simxReadProximitySensor(
            client_id, self._handle, vrep.simx_opmode_blocking)
        if res == vrep.simx_return_ok:
            if detect:
                return 1.0 - point[2]  # distance inverted
            else:
                return 0.0
        elif res == vrep.simx_return_novalue_flag:
            return 0.0
        else:
            raise ServerError(
                "Could not retrieve data from {}.".format(self._name))


class VisionSensor(SceneObject):
    """Interface to vision sensor simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(VisionSensor, self).__init__(vrep_sim, name)

    def get_image(self, grayscale=False):
        """Retrieve image."""
        # Retrieve image from the vision sensor simulated in V-REP
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve image from {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, resolution, image = vrep.simxGetVisionSensorImage(
            client_id, self._handle, grayscale, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve image from {}.".format(self._name))

        # Convert misrepresented pixel values due to the underlying unsigned
        # type
        image = [val if val >= 0 else val + 256 for val in image]

        # If necessary, arrange RGB triplets
        width, height = resolution
        n_pixels = width * height
        if not grayscale:
            image = [image[p:p+3] for p in range(0, 3*n_pixels, 3)]

        # Arrange pixels in rows, reversing from bottom up to top down order
        image = [image[p:p+width] for p in reversed(range(0, n_pixels, width))]

        return image


class MotorArray(object):
    """Interface to an array of motors simulated in V-REP."""

    def __init__(self, vrep_sim, motor_names):
        if motor_names:
            self._motors = [Motor(vrep_sim, name) for name in motor_names]
        else:
            self._motors = []

    def __contains__(self, item):
        """Check if specific motor belongs to the array."""
        return item in self._motors

    def __getitem__(self, key):
        """Retrieve specific motor."""
        return self._motors[key]

    def __iter__(self):
        """Retrieve iterator over motors."""
        return iter(self._motors)

    def __len__(self):
        """Retrieve number of motors."""
        return len(self._motors)

    def set_velocities(self, motor_velocities):
        """Set velocities for all motors."""
        for m, motor in enumerate(self._motors):
            motor.set_velocity(motor_velocities[m])


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
