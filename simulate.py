import pybullet as p
import pybullet_data
import generate
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random as r
import constants as c
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()
pass

# generate

# pi = np.pi


# 
# backLegSensorValues = np.zeros(c.iter)
# frontLegSensorValues = np.zeros(c.iter)
# x = np.linspace(0, 2*pi, c.iter)
# targetAnglesBL = c.amplitudeBL * np.sin(c.frequencyBL * x + c.phaseOffsetBL)
# targetAnglesFL= c.amplitudeFL * np.sin(c.frequencyFL * x + c.phaseOffsetFL)
# # np.save("data/sinusoid1", targetAnglesBL)
# # np.save("data/sinusoid2", targetAnglesFL)
# # # np.save("data/sinusoid", targetAngles)
# # p.disconnect()
# # exit()
  
#     
# np.save("data/backLegTouch.npy", backLegSensorValues)
# np.save("data/frontLegTouch.npy", frontLegSensorValues)
# p.disconnect()