import boidsapi.boids

ENUM_VALUES = [
  boidsapi.boids.SimulationState.PAUSED,
  boidsapi.boids.SimulationState.RESET,
  boidsapi.boids.SimulationState.RUNNING,
  boidsapi.boids.SimulationState.STEP
  ]

def simulationStateFromString(value: str) -> boidsapi.boids.SimulationState:
  for enum_value in ENUM_VALUES:
    if str(enum_value) == value:
      return enum_value
  raise RuntimeError(f"Unrecognized SimulationState value: {value}")
