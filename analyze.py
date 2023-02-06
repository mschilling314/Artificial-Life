import numpy as np
import matplotlib.pyplot as plot
import time


# backLegSensorValues = np.load("data/backLegTouch.npy")
# frontLegSensorValues = np.load("data/frontLegTouch.npy")

# print(backLegSensorValues)
# plot.plot(backLegSensorValues, label="Back", linewidth=5)


# print(frontLegSensorValues)
# plot.plot(frontLegSensorValues, label="Front")
# plot.legend()
sinusoid = np.load("data/sinusoid1.npy")
s = np.load("data/sinusoid2.npy")
plot.plot(sinusoid)
plot.plot(s)

plot.show()