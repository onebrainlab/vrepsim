# -*- coding: utf-8 -*-
"""Nengo communicator for data exchange with V-REP simulator.

Nengo communicator for data exchange with V-REP simulator provides the
following functionality:

- adding slots for input data to V-REP;
- adding slots for output data from V-REP;
- updating states of scene objects simulated in V-REP.
"""

from vrepsim.base import Communicator


class NengoComm(Communicator):
    """Nengo communicator for data exchange with V-REP simulator."""

    def __init__(self, vrep_sim, n_nengo_sim_steps):
        super(NengoComm, self).__init__(vrep_sim)
        self._input_handlers = []
        self._output_handlers = []
        self._size_in = 0
        self._size_out = 0
        self._output = []
        self._n_nengo_sim_steps = int(n_nengo_sim_steps)
        self._nengo_sim_steps_count = 1

    def __call__(self, t, x):
        """Update states of scene objects simulated in V-REP."""
        # Determine if state update is necessary and if so, update the states
        self._nengo_sim_steps_count -= 1
        if not self._nengo_sim_steps_count:
            # Reset counter of Nengo simulation time steps per V-REP simulation
            # time step
            self._nengo_sim_steps_count = self._n_nengo_sim_steps

            # Send input data to simulated scene objects
            start_dim = 0
            for func, dim in self._input_handlers:
                func(x[start_dim:start_dim+dim])
                start_dim += dim

            # Retrieve output data from simulated scene objects
            output = []
            for func in self._output_handlers:
                res = func()
                try:
                    output.extend(res)
                except TypeError:
                    output.append(res)
            self._output = output

            # Trigger next V-REP simulation step
            self.vrep_sim.trig_sim_step()

        return self._output

    @property
    def size_in(self):
        """Number of dimensions of input data to V-REP."""
        return self._size_in

    @property
    def size_out(self):
        """Number of dimensions of output data from V-REP."""
        return self._size_out

    def add_input(self, function, dimensions):
        """Add slots for input data to V-REP."""
        self._input_handlers.append((function, dimensions))
        self._size_in += dimensions

    def add_output(self, function, dimensions):
        """Add slots for output data from V-REP."""
        self._output_handlers.append(function)
        self._size_out += dimensions
        self._output.extend([0.0]*dimensions)
