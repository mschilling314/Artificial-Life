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
data = np.load("fitnessVals.npy")
plot.plot(data[:,:,0])
plot.title("Parent Fitness")
plot.show()
plot.figure()
plot.title("Child Fitness")
plot.plot(data[:,:,1])


plot.show()