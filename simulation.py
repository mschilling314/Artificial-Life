import time
from robot import ROBOT
from world import WORLD
import pybullet as p
import constants as c
import pybullet_data
import pyrosim


class SIMULATION:
    def __init__(self) -> None:
        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.g)
        self.world = WORLD()
        self.robot = ROBOT()
        pyrosim.Prepare_To_Simulate(self.robot.robotID)


    def Run():
        for i in range(c.iter):
            p.stepSimulation()
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
            # maxForce = 50
            # pyrosim.Set_Motor_For_Joint(bodyIndex = robotID, jointName = "Torso_Backleg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBL[i], maxForce = maxForce)
            # pyrosim.Set_Motor_For_Joint(bodyIndex = robotID, jointName = "Torso_Frontleg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFL[i], maxForce = maxForce)
            time.sleep(c.sleepFreq)
  