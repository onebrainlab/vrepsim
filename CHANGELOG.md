Changelog
=========

0.4.0 - 2020-07-10
------------------

### Added

- Added support for Python 3.
- Added retrieving default interface to V-REP remote API server via interface
  to V-REP remote API server.
- Added communicating with V-REP remote API server using context manager via
  interface to V-REP remote API server.
- Added indicator of whether connection to V-REP remote API server is
  established to interface to V-REP remote API server.
- Added loading scene from file via interface to V-REP remote API server.
- Added indicator of whether scene object has been removed to interface to a
  generic scene object simulated in V-REP.
- Added retrieving distance to detected point from proximity sensor via
  interface to proximity sensor simulated in V-REP.
- Added retrieving distances to detected points by all sensors via interface to
  an array of proximity sensors simulated in V-REP.
- Added retrieving vision sensor depth buffer via interface to vision sensor
  simulated in V-REP.
- Added retrieving vision sensor resolution via interface to vision sensor
  simulated in V-REP.
- Added setting vision sensor resolution via interface to vision sensor
  simulated in V-REP.
- Added retrieving vision sensor near clipping plane via interface to vision
  sensor simulated in V-REP.
- Added setting vision sensor near clipping plane via interface to vision
  sensor simulated in V-REP.
- Added retrieving vision sensor far clipping plane via interface to vision
  sensor simulated in V-REP.
- Added setting vision sensor far clipping plane via interface to vision sensor
  simulated in V-REP.
- Added optional argument for retrieving scene object position, which allows
  specifying a precision to which the returned float values should be rounded.
- Added optional argument for retrieving scene object orientation, which allows
  specifying a precision to which the returned float values should be rounded.
- Added optional argument for retrieving positions of scene objects in a
  collection, which allows specifying a precision to which the returned float
  values should be rounded.
- Added optional argument for retrieving orientations of scene objects in a
  collection, which allows specifying a precision to which the returned float
  values should be rounded.

### Changed

- Changed hierarchy of classes that communicate with V-REP simulator.
- Changed arguments for interface to V-REP remote API server.
- Changed arguments for interfaces to scene objects and models simulated in
  V-REP.
- Changed connecting to and disconnecting from V-REP remote API server via
  interface to V-REP remote API server such that establishing multiple
  connections is explicitly forbidden.
- Changed handling errors when calling V-REP remote API functions.
- Changed handling errors when retrieving data from array of sensors.
- Changed handling errors when setting velocities for array of motors.
- Changed retrieving handle to scene object from various types via interface to
  scene objects simulated in V-REP.
- Changed retrieving handle to scene object parent via interface to a generic
  scene object simulated in V-REP.
- Changed argument for setting scene object parent via interface to a generic
  scene object simulated in V-REP.
- Changed retrieving whether V-REP simulation is started via interface to V-REP
  remote API server.
- Changed rounding float values returned by V-REP remote API functions.

### Fixed

- Fixed removing object from scene via interface to a generic scene object
  simulated in V-REP.
- Fixed removing model from scene via interface to a generic model simulated in
  V-REP.

### Deprecated

- Deprecated support for Python 2.

### Removed

- Removed retrieving distance to detected point inverted such that smaller
  values correspond to further distances from interface to proximity sensor
  simulated in V-REP.
- Removed retrieving distances to detected points by all sensors inverted such
  that smaller values correspond to further distances from interface to an
  array of proximity sensors simulated in V-REP.

0.3.0 - 2019-06-26
------------------

### Added

- Added interface to vision sensor simulated in V-REP.
- Added retrieving whether V-REP simulation is started via interface to V-REP
  remote API server.
- Added setting object position via interface to a generic scene object
  simulated in V-REP.
- Added setting object orientation via interface to a generic scene object
  simulated in V-REP.
- Added retrieving limits of object bounding box via interface to a generic
  scene object simulated in V-REP.
- Added retrieving limits of model bounding box via interface to a generic
  model simulated in V-REP.
- Added retrieving handle to object parent via interface to a generic scene
  object simulated in V-REP.
- Added setting object parent via interface to a generic scene object simulated
  in V-REP.
- Added copying and pasting object via interface to a generic scene object
  simulated in V-REP.
- Added removing object from scene via interface to a generic scene object
  simulated in V-REP.
- Added removing model from scene via interface to a generic model simulated in
  V-REP.
- Added calling function from associated script via interface to a generic
  scene object simulated in V-REP.

### Changed

- Changed semantics of V-REPSim exceptions.

0.2.0 - 2018-06-11
------------------

### Added

- Added retrieving dynamics engine name via interface to V-REP remote API
  server.
- Added retrieving dynamics engine time step via interface to V-REP remote API
  server.

0.1.0 - 2017-05-05
------------------

### Added

- Added interface to V-REP remote API server.
- Added interface to a generic scene object simulated in V-REP.
- Added interface to dummy object simulated in V-REP.
- Added interface to proximity sensor simulated in V-REP.
- Added interface to motor (motorized joint) simulated in V-REP.
- Added interface to an array of generic sensors simulated in V-REP.
- Added interface to an array of proximity sensors simulated in V-REP.
- Added interface to an array of motors simulated in V-REP.
- Added interface to a collection of scene objects simulated in V-REP.
- Added interface to a generic model simulated in V-REP.
- Added interface to Pioneer P3-DX robot simulated in V-REP.
- Added Nengo communicator for data exchange with V-REP simulator.
- Added hierarchy of V-REPSim exceptions.
- Added package installer.
- Added package description.
- Added package license terms.
