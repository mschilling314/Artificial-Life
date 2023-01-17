from robot import ROBOT
from world import WORLD
import pybullet as p
import constants as c
import pybullet_data
import pyrosim
import time


class SIMULATION:
    def __init__(self) -> None:
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.g)
        self.world = WORLD()
        self.robot = ROBOT()
        

    def Run(self):
        for i in range(c.iter):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)
            time.sleep(c.sleepFreq)

    
    def __del__(self):
        p.disconnect()
