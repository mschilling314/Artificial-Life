import pybullet as p
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR


class ROBOT:
    def __init__(self) -> None:
        self.sensors = dict()
        self.motors = dict()
        self.robotID = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()


    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)


    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)


    def Sense(self, i):
        for sensor in self.sensors.values():
            sensor.Get_Value(i)


    def Act(self, i):
        for motor in self.motors.values():
            motor.Set_Value(i, self)