import random
import numpy as np
import pyrosim.pyrosim as pyrosim
import simulate


class SOLUTION:
    def __init__(self) -> None:
        self.weights = np.random.rand(3, 2)
        self.weights = 2 * self.weights - 1


    def Evaluate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        simulate.Simulate()
        fitnessFile = open("fitness.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()


    def sendCube(self, nomen, x=0, y=0, side=1, zoff = 0):
        z = side / 2 + zoff# so that it starts on the floor
        pyrosim.Send_Cube(name=nomen, pos=[x, y, z], size=[side, side, side])

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        self.sendCube("Box", -2, -2)
        pyrosim.End()


    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        self.sendCube("Torso", zoff=1)
        #pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [1, 0, 1])
        pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [0.5, 0, 1])
        self.sendCube("Backleg", x=0.5, zoff=-1)
        pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [-0.5, 0, 1])
        self.sendCube("Frontleg", x=-0.5, zoff=-1)
        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0, linkName= "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName= "Backleg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName= "Frontleg")
        pyrosim.Send_Motor_Neuron(name = 3, jointName= "Torso_Backleg")
        pyrosim.Send_Motor_Neuron(name = 4, jointName= "Torso_Frontleg")
        for currentRow in range(self.weights.shape[0]):
            for currentColumn in range(self.weights.shape[1]):
                sensor = currentRow
                motor = currentColumn + self.weights.shape[0]
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()


    def Mutate(self):
        rowMutated = random.randint(0, self.weights.shape[0]-1)
        columnMutated = random.randint(0, self.weights.shape[1]-1)
        self.weights[rowMutated, columnMutated] = random.random() * 2 - 1

