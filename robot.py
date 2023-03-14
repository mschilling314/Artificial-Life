import os
import pybullet as p
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c


class ROBOT:
    def __init__(self, sID, links) -> None:
        self.sensors = dict()
        self.links = links
        self.nn = NEURAL_NETWORK("brain" + str(sID) + ".nndf")
        self.motors = dict()
        self.myID = sID
        self.robotID = p.loadURDF("body" + str(self.myID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        cmd = "del brain" + str(self.myID) + ".nndf"
        os.system(cmd)
        cmd = "del body" + str(self.myID) + ".urdf"
        os.system(cmd)


    def Prepare_To_Sense(self):
        for linkName in self.links:
            self.sensors[linkName] = SENSOR(linkName)


    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)


    def Sense(self, i):
        # print("\nThe self.sensors is: ", self.sensors.keys())
        for sensor in self.sensors.values():
            sensor.Get_Value(i)


    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self)
                # print(neuronName, " ", jointName, " ", desiredAngle, "\n\n")
        # for motor in self.motors.values():
        #     motor.Set_Value(i, self)


    def Think(self):
        self.nn.Update()
        # self.nn.Print()


    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotID)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        f = open("tmp" + str(self.myID) + ".txt", "w")
        f.write(str(xPosition))
        f.close()
        cmd = "rename tmp" + str(self.myID) + ".txt fitness" + str(self.myID) + ".txt"
        # print("\n\n\n\nRobot ", self.myID, "\n\n\n\n\n")
        os.system(cmd)