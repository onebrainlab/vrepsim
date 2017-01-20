# -*- coding: utf-8 -*-
"""Interface to models simulated in V-REP.

Interface to models simulated in V-REP provides individual interfaces to the
following models:

- generic model;
- Pioneer P3-DX robot.
"""

from vrepsim.objects import MotorArray, ProximitySensorArray, SceneObject


class Model(SceneObject):
    """Interface to a generic model simulated in V-REP."""

    def __init__(self, vrep_sim, name):
        super(Model, self).__init__(vrep_sim, name)


class PioneerBot(Model):
    """Interface to Pioneer P3-DX robot simulated in V-REP."""

    def __init__(self, vrep_sim, name, us_sensor_names, motor_names):
        super(PioneerBot, self).__init__(vrep_sim, name)
        self.us_sensors = ProximitySensorArray(vrep_sim, us_sensor_names)
        self.wheels = MotorArray(vrep_sim, motor_names)
