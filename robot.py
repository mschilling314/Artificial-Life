import pybullet as p
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self) -> None:
        self.sensors = dict()
        self.nn = NEURAL_NETWORK("brain.nndf")
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
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self)
                # print(neuronName, " ", jointName, " ", desiredAngle, "\n\n")
        # for motor in self.motors.values():
        #     motor.Set_Value(i, self)


    def Think(self):
        self.nn.Update()
        # self.nn.Print()


    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotID, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        f = open("fitness.txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()