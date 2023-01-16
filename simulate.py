import pybullet as p
import pybullet_data
import generate
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random as r

generate

pi = np.pi

iter = 1000
amplitudeBL = pi/4
frequencyBL = 10
phaseOffsetBL = 0
amplitudeFL = pi/4
frequencyFL = 10
phaseOffsetFL = pi/4 + 0.5

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
planeID = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = np.zeros(iter)
frontLegSensorValues = np.zeros(iter)
x = np.linspace(0, 2*pi, iter)
targetAnglesBL = amplitudeBL * np.sin(frequencyBL * x + phaseOffsetBL)
targetAnglesFL= amplitudeFL * np.sin(frequencyFL * x + phaseOffsetFL)
# np.save("data/sinusoid1", targetAnglesBL)
# np.save("data/sinusoid2", targetAnglesFL)
# # np.save("data/sinusoid", targetAngles)
# p.disconnect()
# exit()
for i in range(iter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
    tP1 = r.random() * pi - pi/2
    tP2 = r.random() * pi - pi/2
    maxForce = 50
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotID, jointName = "Torso_Backleg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBL[i], maxForce = maxForce)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotID, jointName = "Torso_Frontleg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFL[i], maxForce = maxForce)
    
    time.sleep(1/240)
np.save("data/backLegTouch.npy", backLegSensorValues)
np.save("data/frontLegTouch.npy", frontLegSensorValues)
p.disconnect()