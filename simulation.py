from robot import ROBOT
from world import WORLD
import pybullet as p
import constants as c
import pybullet_data
import pyrosim
import time


class SIMULATION:
    def __init__(self, lynx, pretty="DIRECT", solnID=0) -> None:
        self.directOrGui = pretty
        if pretty == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        elif pretty == "GUI":
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        else:
            print("You gave an invalid input to the SIMULATION constructor.")
            exit()
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.g)
        self.world = WORLD()
        self.robot = ROBOT(solnID, lynx)
        

    def Run(self):
        for i in range(c.iter):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGui == "GUI":
                time.sleep(c.sleepFreq)

    
    def __del__(self):
        p.disconnect()


    def Get_Fitness(self):
        self.robot.Get_Fitness()
