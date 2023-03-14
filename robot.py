import os
import pybullet as p
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c


class ROBOT:
    """
    A class that holds the robot that is simulated.

    Attributes:
    sensors (dict[str, SENSOR]):  Stores access to the sensors.
    links (list[str]):  Stores the links that actually have sensors
    nn (NEURAL_NETWORK):  A neural net connected to the brainID.nndf file.
    motors (dict[str, MOTOR]):  A dictionary that holds the motor corresponding to joint names.
    myID (int):  An identification number, matching the solution of the robot.
    """
    def __init__(self, sID: int, links: list[str]) -> None:
        self.sensors = dict()
        self.nn = NEURAL_NETWORK("brain" + str(sID) + ".nndf")
        self.motors = dict()
        self.myID = sID
        self.robotID = p.loadURDF("body" + str(self.myID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.Prepare_To_Sense(links)
        self.Prepare_To_Act()
        cmd = "del brain" + str(self.myID) + ".nndf"
        os.system(cmd)
        cmd = "del body" + str(self.myID) + ".urdf"
        os.system(cmd)


    def Prepare_To_Sense(self, links: list[str]) -> None:
        """
        Initializes the dictionary of sensors with sensor objects.

        Parameters:
        links:  A list of the links that need to have a sensor neuron.
        """
        for linkName in links:
            self.sensors[linkName] = SENSOR(linkName)


    def Prepare_To_Act(self) -> None:
        """
        Initializes the dictionary of motors with motor objects.
        """
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)


    def Sense(self, i: int) -> None:
        """
        Does the actual sensing by calling a method from sensor.py.

        Parameters:
        i:  The time step.
        """
        # print("\nThe self.sensors is: ", self.sensors.keys())
        for sensor in self.sensors.values():
            sensor.Get_Value(i)


    def Act(self) -> None:
        """
        Sets the value of the motor's desired angle.
        """
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self.myID)
                # print(neuronName, " ", jointName, " ", desiredAngle, "\n\n")


    def Think(self) -> None:
        """
        Updates the neural network's values.
        """
        self.nn.Update()
        # self.nn.Print()


    def Get_Fitness(self) -> None:
        """
        Gets the fitness of the robot, prints it in a file named tmpID.txt at first, then fitnessID.txt.
        """
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotID)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        f = open("tmp" + str(self.myID) + ".txt", "w")
        f.write(str(xPosition))
        f.close()
        cmd = "rename tmp" + str(self.myID) + ".txt fitness" + str(self.myID) + ".txt"
        # print("\n\n\n\nRobot ", self.myID, "\n\n\n\n\n")
        os.system(cmd)