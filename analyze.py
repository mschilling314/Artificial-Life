import numpy as np
import matplotlib.pyplot as plot


backLegSensorValues = np.load("data/backLegTouch.npy")
frontLegSensorValues = np.load("data/frontLegTouch.npy")

print(backLegSensorValues)
plot.plot(backLegSensorValues, label="Back", linewidth=5)


print(frontLegSensorValues)
plot.plot(frontLegSensorValues, label="Front")
plot.legend()
plot.show()