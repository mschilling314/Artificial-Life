import pybullet as p
import pybullet_data
import generate
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

generate

iter = 300

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
planeID = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = np.zeros(iter)
frontLegSensorValues = np.zeros(iter)
for i in range(iter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
    time.sleep(1/60)
np.save("data/backLegTouch.npy", backLegSensorValues)
np.save("data/frontLegTouch.npy", frontLegSensorValues)
p.disconnect()