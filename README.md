# V-REPSim: V-REP Simulator Python Interface

V-REPSim provides a high-level interface based on the V-REP remote API for
controlling V-REP simulations from an external Python program.

## Dependencies

For V-REPSim to operate successfully, the following V-REP files (or,
alternatively, links to them) have to exist in the current directory so that
the V-REP remote API could be used (here, `V-REP_DIR` denotes the directory in
which V-REP is installed):

- `vrep.py` (original file in:
  `V-REP_DIR/programming/remoteApiBindings/python/python/`);
- `vrepConst.py` (original file in:
  `V-REP_DIR/programming/remoteApiBindings/python/python/`);
- `[remoteApi.so | remoteApi.dylib | remoteApi.dll]` (original file in:
  `V-REP_DIR/programming/remoteApiBindings/lib/lib/[32Bit | 64Bit]/`).

## Example

The example script below demonstrates how V-REPSim can be used to:

- connect to a V-REP remote API server;
- retrieve V-REP simulation time step;
- start a V-REP simulation in synchronous operation mode;
- create a representation of a model simulated in V-REP;
- trigger a V-REP simulation step;
- stop the V-REP simulation;
- disconnect from the V-REP remote API server.

For this script to run successfully, V-REP simulator must first be launched
with a continuous remote API server service started and a scene file must be
opened in the simulator.

```python
import vrep
import vrepsim as vrs

# Connect to V-REP
vrep_sim = vrs.Simulator('127.0.0.1', 19997)
vrep_sim.connect(verbose=True)

# Retrieve V-REP simulation time step
sim_dt = vrep_sim.get_sim_dt()

# Start V-REP simulation in synchronous operation mode
vrep_sim.start_sim(verbose=True)

# Create representation of the floor and print its position
floor = vrs.Model(vrep_sim, "ResizableFloor_5_25")
print("Floor position: {}".format(floor.get_position()))

# Perform operations not provided by V-REPSim by using V-REP remote API
# directly, e.g.,
ret_code = vrep.simxAddStatusbarMessage(
    vrep_sim.client_id, "Control from external Python program enabled.",
    vrep.simx_opmode_oneshot)
if ret_code not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
    print("Could not add a message to the status bar.")

# Run a simulation for the specified time
sim_time = 0.0
while sim_time < 10.0:
    # Perform some operations using V-REPSim or V-REP remote API directly
    # ...

    # Trigger next V-REP simulation step
    vrep_sim.trig_sim_step()
    sim_time += sim_dt

# Stop V-REP simulation
vrep_sim.stop_sim(verbose=True)

# Disconnect from V-REP
vrep_sim.disconnect(verbose=True)
```
