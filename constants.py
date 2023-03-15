import numpy as np
pi = np.pi

iter = 1000
coreHeight = 10
amplitude = pi/4
frequency = 10
phaseOffset = 0
maxForce = 5000
# amplitudeFL = pi/4
# frequencyFL = 10
# phaseOffsetFL = pi/4
sleepFreq = 1/600
g = -9.8
populationSize = 25
numberOfGenerations = 100


numHiddenNeurons = 5

motorJointRange = 0.3

height = 5.2


if __name__ == "__main__":
    import search


    search.run_sim()
