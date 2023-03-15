from robot import ROBOT
from world import WORLD
import pybullet as p
import constants as c
import pybullet_data
import time


class SIMULATION:
    """
    A class designed to create and run a simulation involving a singular robot.
    """
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
        self.id = solnID
        self.world = WORLD()
        self.robot = ROBOT(solnID, lynx)
        

    def Run(self):
        """
        The process of actually running a simulation, done by performing the robot's methods in a particular order.
        """
        for i in range(c.iter):
            p.stepSimulation()
            # basePos, baseOrn = p.getBasePositionAndOrientation(self.id)
            # p.resetDebugVisualizerCamera( cameraDistance = 5, cameraYaw=75, cameraPitch=-20, cameraTargetPosition = basePos)
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()
            if self.directOrGui == "GUI":
                time.sleep(c.sleepFreq)

    
    def __del__(self):
        """
        Simple deconstructor that disconnects the simulation.
        """
        p.disconnect()


    def Get_Fitness(self) -> None:
        """
        Orders the robot to write its fitness to a file.
        """
        self.robot.Get_Fitness()
