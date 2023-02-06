import os
import random
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import simulate
import multiprocessing
import constants as c


class SOLUTION:
    def __init__(self, nextAvailableID) -> None:
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = 2 * self.weights - 1
        self.myID = nextAvailableID


    def Evaluate(self, processes, show="DIRECT"):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        p = multiprocessing.Process(target=simulate.Simulate, args=[show, self.myID])
        p.start()
        processes.append(p)
        #simulate.Simulate(gui=show)
        fitnessFileName = "fitness"+ str(self.myID) +".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        print(self.fitness)
        fitnessFile.close()


    def Start_Simulation(self, show="DIRECT"):
        if self.myID == 0:
            self.Create_World()
            self.Create_Body()
        self.Create_Brain()
        p = multiprocessing.Process(target=simulate.Simulate, args=[show, self.myID])
        p.start()


    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness"+ str(self.myID) +".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        cmd = "del fitness" + str(self.myID) + ".txt"
        os.system(cmd)


    def sendCube(self, nomen, x=0, y=0, side=1, zoff = 0):
        z = side / 2 + zoff# so that it starts on the floor
        pyrosim.Send_Cube(name=nomen, pos=[x, y, z], size=[side, side, side])

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        self.sendCube("Box", -2, -2)
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        #pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [1, 0, 1])
        pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [0, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Backleg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [0, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Frontleg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint( name = "Torso_Leftleg" , parent= "Torso" , child = "Leftleg" , type = "revolute", position = [-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leftleg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint( name = "Torso_Rightleg" , parent= "Torso" , child = "Rightleg" , type = "revolute", position = [0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Rightleg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Frontleg_Frontfoot", parent="Frontleg", child = "Frontfoot", type="revolute", position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Frontfoot", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Backleg_Backfoot", parent="Backleg", child = "Backfoot", type="revolute", position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Backfoot", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Leftleg_Leftfoot", parent="Leftleg", child = "Leftfoot", type="revolute", position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="Leftfoot", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Rightleg_Rightfoot", parent="Rightleg", child = "Rightfoot", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="Rightfoot", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0, linkName= "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName= "Backleg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName= "Frontleg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName= "Leftleg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName= "Rightleg")
        pyrosim.Send_Sensor_Neuron(name = 5, linkName= "Backfoot")
        pyrosim.Send_Sensor_Neuron(name = 6, linkName= "Frontfoot")
        pyrosim.Send_Sensor_Neuron(name = 7, linkName= "Leftfoot")
        pyrosim.Send_Sensor_Neuron(name = 8, linkName= "Rightfoot")
        pyrosim.Send_Motor_Neuron(name = 9, jointName= "Torso_Backleg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName= "Torso_Frontleg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName= "Torso_Leftleg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName= "Torso_Rightleg")
        pyrosim.Send_Motor_Neuron(name = 13, jointName= "Backleg_Backfoot")
        pyrosim.Send_Motor_Neuron(name = 14, jointName= "Frontleg_Frontfoot")
        pyrosim.Send_Motor_Neuron(name = 15, jointName= "Leftleg_Leftfoot")
        pyrosim.Send_Motor_Neuron(name = 16, jointName= "Rightleg_Rightfoot")
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                sensor = currentRow
                motor = currentColumn + c.numSensorNeurons
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()


    def Mutate(self):
        rowMutated = random.randint(0, c.numSensorNeurons-1)
        columnMutated = random.randint(0, c.numMotorNeurons-1)
        self.weights[rowMutated, columnMutated] = random.random() * 2 - 1


    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID


