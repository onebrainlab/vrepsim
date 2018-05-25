# -*- coding: utf-8 -*-
"""Interface to V-REP remote API server.

Interface to V-REP remote API server provides the following functionality:

- connecting to a V-REP remote API server;
- disconnecting from a V-REP remote API server;
- retrieving V-REP version;
- retrieving dynamics engine name;
- retrieving scene path;
- starting a V-REP simulation in synchronous operation mode;
- stopping a V-REP simulation;
- triggering a V-REP simulation step;
- retrieving V-REP simulation time step;
- retrieving dynamics engine time step.
"""

import time

import vrep

from vrepsim.exceptions import ServerError, SimulationError


class Simulator(object):
    """Interface to V-REP remote API server."""

    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._client_id = None

    @property
    def addr(self):
        """V-REP remote API server address."""
        return self._addr

    @property
    def client_id(self):
        """Client ID."""
        return self._client_id

    @property
    def port(self):
        """V-REP remote API server port."""
        return self._port

    def connect(self, wait=True, no_reconnect=True, timeout=5000, cycle=5,
                verbose=False):
        """Connect to V-REP remote API server."""
        # Just in case, close all opened connections to V-REP
        vrep.simxFinish(-1)
        self._client_id = None

        # Connect to V-REP
        client_id = vrep.simxStart(self._addr, self._port, wait, no_reconnect,
                                   timeout, cycle)
        if client_id == -1:
            raise ServerError("Failed to connect to V-REP remote API server "
                              "at {0}:{1}.".format(self._addr, self._port))
        self._client_id = client_id

        # If necessary, display confirmation message
        if verbose:
            print("Successully connected to V-REP remote API server at "
                  "{0}:{1}.".format(self._addr, self._port))

    def disconnect(self, verbose=False):
        """Disconnect from V-REP remote API server."""
        # If connected to V-REP, disconnect
        if self._client_id is not None:
            # Disconnect from V-REP
            vrep.simxFinish(self._client_id)
            self._client_id = None

            # If necessary, display confirmation message
            if verbose:
                print("Disconnected from V-REP remote API server at "
                      "{0}:{1}.".format(self._addr, self._port))
        else:
            # If necessary, display warning message
            if verbose:
                print("Could not disconnect from V-REP remote API server: "
                      "not connected.")

    def get_dyn_eng_dt(self):
        """Retrieve dynamics engine time step."""
        vrep.sim_floatparam_dynamic_step_size = 3  # constant missing in Python
                                                   # binding to V-REP remote
                                                   # API
        res, dyn_eng_dt = vrep.simxGetFloatingParameter(
            self._client_id, vrep.sim_floatparam_dynamic_step_size,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve dynamics engine time step.")
        return round(dyn_eng_dt, 4)  # dynamics engine time step may be
                                     # slightly imprecise (around the 10th
                                     # digit after the decimal point)

    def get_dyn_eng_name(self):
        """Retrieve dynamics engine name."""
        dyn_engs_names = {0: "Bullet", 1: "ODE", 2: "Vortex", 3: "Newton"}
        res, dyn_eng_id = vrep.simxGetIntegerParameter(
            self._client_id, vrep.sim_intparam_dynamic_engine,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve dynamics engine name.")
        return dyn_engs_names[dyn_eng_id]

    def get_scene_path(self):
        """Retrieve scene path."""
        res, scene_path = vrep.simxGetStringParameter(
            self._client_id, vrep.sim_stringparam_scene_path_and_name,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError("Could not retrieve scene path.")
        return scene_path

    def get_sim_dt(self):
        """Retrieve V-REP simulation time step."""
        res, sim_dt = vrep.simxGetFloatingParameter(
            self._client_id, vrep.sim_floatparam_simulation_time_step,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not retrieve V-REP simulation time step.")
        return round(sim_dt, 4)  # V-REP simulation time step may be slightly
                                 # imprecise (around the 10th digit after the
                                 # decimal point)

    def get_version(self):
        """Retrieve V-REP version."""
        res, version = vrep.simxGetIntegerParameter(
            self._client_id, vrep.sim_intparam_program_version,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve V-REP version.")
        return "{x}.{y}.{z}".format(x=version // 10000,
                                    y=(version // 100) % 100,
                                    z=version % 100)

    def start_sim(self, verbose=False):
        """Start V-REP simulation in synchronous operation mode."""
        # Start V-REP simulation in synchronous operation mode
        res = vrep.simxSynchronous(self._client_id, True)
        if res != vrep.simx_return_ok:
            raise SimulationError(
                "Could not enable V-REP synchronous operation mode.")
        res = vrep.simxStartSimulation(self._client_id,
                                       vrep.simx_opmode_blocking)
        if res not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
            raise SimulationError("Could not start V-REP simulation.")

        # If necessary, display confirmation message
        if verbose:
            print("V-REP simulation started at "
                  "{}.".format(time.strftime("%H:%M:%S")))

    def stop_sim(self, verbose=False):
        """Stop V-REP simulation."""
        # Stop V-REP simulation
        res = vrep.simxStopSimulation(self._client_id,
                                      vrep.simx_opmode_blocking)
        if res not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
            raise SimulationError("Could not stop V-REP simulation.")

        # If necessary, display confirmation message
        if verbose:
            print("V-REP simulation stopped at "
                  "{}.".format(time.strftime("%H:%M:%S")))

    def trig_sim_step(self):
        """Trigger V-REP simulation step."""
        res = vrep.simxSynchronousTrigger(self._client_id)
        if res != vrep.simx_return_ok:
            raise SimulationError("Could not trigger V-REP simulation step.")
