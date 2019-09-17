# -*- coding: utf-8 -*-
"""Interface to V-REP remote API server.

Interface to V-REP remote API server provides the following functionality:

- connecting to a V-REP remote API server;
- disconnecting from a V-REP remote API server;
- retrieving default interface to V-REP remote API server;
- retrieving V-REP version;
- retrieving dynamics engine name;
- retrieving scene path;
- starting a V-REP simulation in synchronous operation mode;
- stopping a V-REP simulation;
- retrieving whether V-REP simulation is started;
- triggering a V-REP simulation step;
- retrieving V-REP simulation time step;
- retrieving dynamics engine time step.
"""

import time

import vrep

from vrepsim.constants import VREP_FLOAT_PREC
from vrepsim.exceptions import ConnectionError, ServerError

_vrep_sim = None


def get_default_simulator(raise_on_none=False):
    """Retrieve default interface to V-REP remote API server."""
    if _vrep_sim is None and raise_on_none:
        raise RuntimeError("No interface is currently connected to V-REP "
                           "remote API server.")
    return _vrep_sim


class Simulator(object):
    """Interface to V-REP remote API server."""

    def __init__(self, addr, port, wait=True, reconnect=False, timeout=5000,
                 cycle=5, verbose=False):
        self._addr = addr
        self._port = port
        self._wait = wait
        self._reconnect = reconnect
        self._timeout = timeout
        self._cycle = cycle
        self.verbose = verbose
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
    def cycle(self):
        """Interval between data exchanges with V-REP."""
        return self._cycle

    @property
    def port(self):
        """V-REP remote API server port."""
        return self._port

    @property
    def reconnect(self):
        """Automatic attempts to reconnect to V-REP remote API server after
        losing connection.
        """
        return self._reconnect

    @property
    def timeout(self):
        """Timeout for establishing connection with V-REP remote API server or
        for blocking function calls.
        """
        return self._timeout

    @property
    def wait(self):
        """Blocking wait until establishing connection with V-REP remote API
        server or exceeding timeout.
        """
        return self._wait

    def connect(self, verbose=None):
        """Connect to V-REP remote API server."""
        global _vrep_sim

        # If necessary, determine whether messages should be displayed
        if verbose is None:
            verbose = self.verbose

        # Check if connection to V-REP is already established
        if _vrep_sim is None:
            conn_msg = "connected"
        else:
            if self._client_id is not None:
                conn_msg = "reconnected"
            else:
                raise ConnectionError(
                    "Could not connect to V-REP remote API server at {0}:{1}: "
                    "another connection to V-REP remote API server already "
                    "established.".format(self._addr, self._port))

        # Just in case, close all opened connections to V-REP
        vrep.simxFinish(-1)
        self._client_id = None
        _vrep_sim = None

        # Connect to V-REP
        client_id = vrep.simxStart(
            self._addr, self._port, self._wait, not self._reconnect,
            self._timeout, self._cycle)
        if client_id == -1:
            raise ConnectionError(
                "Failed to connect to V-REP remote API server at "
                "{0}:{1}.".format(self._addr, self._port))
        self._client_id = client_id
        _vrep_sim = self

        # If necessary, display confirmation message
        if verbose:
            print("Successully {0} to V-REP remote API server at "
                  "{1}:{2}.".format(conn_msg, self._addr, self._port))

    def disconnect(self, verbose=None):
        """Disconnect from V-REP remote API server."""
        global _vrep_sim

        # If necessary, determine whether messages should be displayed
        if verbose is None:
            verbose = self.verbose

        # If connected to V-REP, disconnect
        if self._client_id is not None:
            # Disconnect from V-REP
            vrep.simxFinish(self._client_id)
            self._client_id = None
            _vrep_sim = None

            # If necessary, display confirmation message
            if verbose:
                print("Disconnected from V-REP remote API server at "
                      "{0}:{1}.".format(self._addr, self._port))
        else:
            # If necessary, display warning message
            if verbose:
                print("Could not disconnect from V-REP remote API server: "
                      "not connected.")

    def get_dyn_eng_dt(self, prec=VREP_FLOAT_PREC):
        """Retrieve dynamics engine time step."""
        vrep.sim_floatparam_dynamic_step_size = 3  # constant missing in Python
                                                   # binding to V-REP remote
                                                   # API
        if self._client_id is None:
            raise ConnectionError(
                "Could not retrieve dynamics engine time step: not connected "
                "to V-REP remote API server.")
        res, dyn_eng_dt = vrep.simxGetFloatingParameter(
            self._client_id, vrep.sim_floatparam_dynamic_step_size,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve dynamics engine time step.")
        if prec is not None:
            dyn_eng_dt = round(dyn_eng_dt, prec)  # dynamics engine time step
                                                  # may be slightly imprecise
                                                  # (about the 10th digit after
                                                  # the decimal point)
        return dyn_eng_dt

    def get_dyn_eng_name(self):
        """Retrieve dynamics engine name."""
        dyn_engs_names = {0: "Bullet", 1: "ODE", 2: "Vortex", 3: "Newton"}
        if self._client_id is None:
            raise ConnectionError("Could not retrieve dynamics engine name: "
                                  "not connected to V-REP remote API server.")
        res, dyn_eng_id = vrep.simxGetIntegerParameter(
            self._client_id, vrep.sim_intparam_dynamic_engine,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve dynamics engine name.")
        return dyn_engs_names[dyn_eng_id]

    def get_scene_path(self):
        """Retrieve scene path."""
        if self._client_id is None:
            raise ConnectionError("Could not retrieve scene path: not "
                                  "connected to V-REP remote API server.")
        res, scene_path = vrep.simxGetStringParameter(
            self._client_id, vrep.sim_stringparam_scene_path_and_name,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve scene path.")
        return scene_path

    def get_sim_dt(self, prec=VREP_FLOAT_PREC):
        """Retrieve V-REP simulation time step."""
        if self._client_id is None:
            raise ConnectionError(
                "Could not retrieve V-REP simulation time step: not connected "
                "to V-REP remote API server.")
        res, sim_dt = vrep.simxGetFloatingParameter(
            self._client_id, vrep.sim_floatparam_simulation_time_step,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve V-REP simulation time step.")
        if prec is not None:
            sim_dt = round(sim_dt, prec)  # V-REP simulation time step may be
                                          # slightly imprecise (about the 10th
                                          # digit after the decimal point)
        return sim_dt

    def get_version(self):
        """Retrieve V-REP version."""
        if self._client_id is None:
            raise ConnectionError("Could not retrieve V-REP version: not "
                                  "connected to V-REP remote API server.")
        res, version = vrep.simxGetIntegerParameter(
            self._client_id, vrep.sim_intparam_program_version,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve V-REP version.")
        return "{x}.{y}.{z}".format(x=version // 10000,
                                    y=(version // 100) % 100,
                                    z=version % 100)

    def is_sim_started(self):
        """Retrieve whether V-REP simulation is started.

        The return value may be inaccurate if the function is called
        immediately after starting or stopping a simulation; in such a case,
        introducing a short delay before calling it should help.
        """
        SIM_NOT_STOPPED = 0x01

        # Retrieve whether V-REP is currently waiting for a trigger signal;
        # the result by itself, however, is not conclusive as to whether a
        # simulation is started or not (not waiting for a trigger signal does
        # not necessarily mean that a simulation is not started because there
        # may be unprocessed trigger signals during a simulation, in
        # which case V-REP will be advancing the simulation without reporting
        # that it needs to wait for a trigger signal); this operation is
        # performed only to receive a new message from the V-REP remote API
        # server so that the next operation could operate on up-to-date data
        if self._client_id is None:
            raise ConnectionError(
                "Could not retrieve whether V-REP simulation is started: not "
                "connected to V-REP remote API server.")
        res, _ = vrep.simxGetBooleanParameter(
            self._client_id, vrep.sim_boolparam_waiting_for_trigger,
            vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not retrieve whether V-REP simulation is "
                              "started.")

        # Retrieve the server state from the last message received from the
        # V-REP remote API server
        res, server_state = vrep.simxGetInMessageInfo(
            self._client_id, vrep.simx_headeroffset_server_state)
        if res == -1:
            raise ServerError("Could not retrieve whether V-REP simulation is "
                              "started.")

        # Determine whether V-REP simulation is started
        return server_state & SIM_NOT_STOPPED

    def start_sim(self, verbose=None):
        """Start V-REP simulation in synchronous operation mode."""
        # If necessary, determine whether messages should be displayed
        if verbose is None:
            verbose = self.verbose

        # Start V-REP simulation in synchronous operation mode
        if self._client_id is None:
            raise ConnectionError("Could not start V-REP simulation: not "
                                  "connected to V-REP remote API server.")
        res = vrep.simxSynchronous(self._client_id, True)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not enable V-REP synchronous operation mode.")
        res = vrep.simxStartSimulation(self._client_id,
                                       vrep.simx_opmode_blocking)
        if res not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
            raise ServerError("Could not start V-REP simulation.")

        # If necessary, display confirmation message
        if verbose:
            print("V-REP simulation started at "
                  "{}.".format(time.strftime("%H:%M:%S")))

    def stop_sim(self, verbose=None):
        """Stop V-REP simulation."""
        # If necessary, determine whether messages should be displayed
        if verbose is None:
            verbose = self.verbose

        # Stop V-REP simulation
        if self._client_id is None:
            raise ConnectionError("Could not stop V-REP simulation: not "
                                  "connected to V-REP remote API server.")
        res = vrep.simxStopSimulation(self._client_id,
                                      vrep.simx_opmode_blocking)
        if res not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
            raise ServerError("Could not stop V-REP simulation.")

        # If necessary, display confirmation message
        if verbose:
            print("V-REP simulation stopped at "
                  "{}.".format(time.strftime("%H:%M:%S")))

    def trig_sim_step(self):
        """Trigger V-REP simulation step."""
        if self._client_id is None:
            raise ConnectionError("Could not trigger V-REP simulation step: "
                                  "not connected to V-REP remote API server.")
        res = vrep.simxSynchronousTrigger(self._client_id)
        if res != vrep.simx_return_ok:
            raise ServerError("Could not trigger V-REP simulation step.")
