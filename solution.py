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
        self.weightsToHidden = np.random.rand(c.numSensorNeurons, c.numHiddenNeurons)
        self.weightsToHidden = 2 * self.weightsToHidden - 1
        self.weightsToMotor = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
        self.weightsToMotor = 2 * self.weightsToMotor - 1
        self.myID = nextAvailableID
        self.joints = []
        self.links = []


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
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, c.height], size=[0.5, 1, 2])
        self.links.append("Torso")
        #pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [1, 0, 1])
        pyrosim.Send_Joint( name = "Torso_Leftarm" , parent= "Torso" , child = "Leftarm" , type = "revolute", position = [0, -0.6, c.height+0.5], jointAxis = "0 1 0")
        self.joints.append("Torso_Leftarm")
        pyrosim.Send_Cube(name="Leftarm", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        self.links.append("Leftarm")
        pyrosim.Send_Joint( name = "Torso_Rightarm" , parent= "Torso" , child = "Rightarm" , type = "revolute", position = [0, 0.6, c.height+0.5], jointAxis = "0 1 0")
        self.joints.append("Torso_Rightarm")
        pyrosim.Send_Cube(name="Rightarm", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        self.links.append("Rightarm")
        pyrosim.Send_Joint( name = "Torso_Leftleg" , parent= "Torso" , child = "Leftleg" , type = "revolute", position = [0, -0.25, c.height-1], jointAxis = "0 1 0")
        self.joints.append("Torso_Leftleg")
        pyrosim.Send_Cube(name="Leftleg", pos=[0, 0, -1], size=[0.2, 0.2, 2])
        self.links.append("Leftleg")
        pyrosim.Send_Joint( name = "Torso_Rightleg" , parent= "Torso" , child = "Rightleg" , type = "revolute", position = [0, 0.25, c.height-1], jointAxis = "0 1 0")
        self.joints.append("Torso_Rightleg")
        pyrosim.Send_Cube(name="Rightleg", pos=[0, 0, -1], size=[0.2, 0.2, 2])
        self.links.append("Rightleg")
        pyrosim.Send_Joint(name="Rightarm_Righthand", parent="Rightarm", child = "Righthand", type="revolute", position=[0, 0, -1], jointAxis="0 1 0")
        self.joints.append("Rightarm_Righthand")
        pyrosim.Send_Cube(name="Righthand", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        self.links.append("Righthand")
        pyrosim.Send_Joint(name="Leftarm_Lefthand", parent="Leftarm", child = "Lefthand", type="revolute", position=[0, 0, -1], jointAxis="0 1 0")
        self.joints.append("Leftarm_Lefthand")
        pyrosim.Send_Cube(name="Lefthand", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        self.links.append("Lefthand")
        pyrosim.Send_Joint(name="Leftleg_Leftshin", parent="Leftleg", child = "Leftshin", type="revolute", position=[0, 0, -2], jointAxis="0 1 0")
        self.joints.append("Leftleg_Leftshin")
        pyrosim.Send_Cube(name="Leftshin", pos=[0, 0, -1], size=[0.2, 0.2, 2])
        self.links.append("Leftshin")
        pyrosim.Send_Joint(name="Rightleg_Rightshin", parent="Rightleg", child = "Rightshin", type="revolute", position=[0, 0, -2], jointAxis="0 1 0")
        self.joints.append("Rightleg_Rightshin")
        pyrosim.Send_Cube(name="Rightshin", pos=[0, 0, -1], size=[0.2, 0.2, 2])
        self.links.append("Rightshin")
        pyrosim.Send_Joint(name="Rightshin_Rightfoot", parent="Rightshin", child="Rightfoot", type="revolute", position=[0, 0, -2], jointAxis="0 1 0")
        self.joints.append("Rightshin_Rightfoot")
        pyrosim.Send_Cube(name="Rightfoot", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        self.links.append("Rightfoot")
        pyrosim.Send_Joint(name="Leftshin_Leftfoot", parent="Leftshin", child="Leftfoot", type="revolute", position=[0, 0, -2], jointAxis="0 1 0")
        self.joints.append("Leftshin_Leftfoot")
        pyrosim.Send_Cube(name="Leftfoot", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        self.links.append("Leftfoot")
        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        for i in range(len(self.links)):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=self.links[i])
        newBase = len(self.links)
        for i in range(c.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i+newBase)
        newBase += c.numHiddenNeurons
        for i in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name=i+newBase, jointName=self.joints[i])
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numHiddenNeurons):
                sensor = currentRow
                hidden = currentColumn + c.numSensorNeurons
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=hidden, weight=self.weightsToHidden[currentRow][currentColumn])
        for currentRow in range(c.numHiddenNeurons):
            for currentColumn in range(c.numMotorNeurons):
                hidden = currentRow + c.numSensorNeurons
                motor = currentColumn + c.numHiddenNeurons + c.numSensorNeurons
                pyrosim.Send_Synapse(sourceNeuronName=hidden, targetNeuronName=motor, weight=self.weightsToMotor[currentRow][currentColumn])
        pyrosim.End()


    def Mutate(self):
        rowMutated = random.randint(0, c.numSensorNeurons-1)
        columnMutated = random.randint(0, c.numHiddenNeurons-1)
        self.weightsToHidden[rowMutated, columnMutated] = random.random() * 2 - 1
        rowMutated = random.randint(0, c.numHiddenNeurons-1)
        columnMutated = random.randint(0, c.numMotorNeurons-1)
        self.weightsToMotor[rowMutated, columnMutated] = random.random() * 2 - 1


    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID


