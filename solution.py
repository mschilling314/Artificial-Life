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
        self.myID = nextAvailableID
        self.joints = []
        self.links = []
        self.currentLink = 0


    def Start_Simulation(self, show="DIRECT"):
        if self.myID == 0:
            self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        p = multiprocessing.Process(target=simulate.Simulate, args=[self.links, show, self.myID])
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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        rL = random.randint(-1, 1)
        self.Node(recursiveLimit= 3+rL, posi=[0, 0, 1], sizzle=[2, 3, 1], firstIter=True)
        pyrosim.End()
        self.weightsToHidden = np.random.rand(len(self.links), c.numHiddenNeurons)
        self.weightsToHidden = 2 * self.weightsToHidden - 1
        self.weightsToMotor = np.random.rand(c.numHiddenNeurons, len(self.joints))
        self.weightsToMotor = 2 * self.weightsToMotor - 1


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        # Create sensor neurons for the selected links
        for i in range(len(self.links)):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=self.links[i])
        newBase = len(self.links)
        # create hidden neurons
        for i in range(c.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i+newBase)
        newBase += c.numHiddenNeurons
        # create motor neurons for all joints
        for i in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name=i+newBase, jointName=self.joints[i])
        # create synapses for a fully-connected layer of sensors and hidden neurons
        for currentRow in range(len(self.links)):
            for currentColumn in range(c.numHiddenNeurons):
                sensor = currentRow
                hidden = currentColumn + len(self.links)
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=hidden, weight=self.weightsToHidden[currentRow, currentColumn])
        # Create synapes for a fully-connected layer of hidden neurons and motors
        for currentRow in range(c.numHiddenNeurons):
            for currentColumn in range(len(self.joints)):
                hidden = currentRow + len(self.links)
                motor = currentColumn + c.numHiddenNeurons + len(self.links)
                pyrosim.Send_Synapse(sourceNeuronName=hidden, targetNeuronName=motor, weight=self.weightsToMotor[currentRow, currentColumn])
        pyrosim.End()


    def Mutate(self):
        rowMutated = random.randint(0, len(self.links)-1)
        columnMutated = random.randint(0, c.numHiddenNeurons-1)
        self.weightsToHidden[rowMutated, columnMutated] = random.random() * 2 - 1
        rowMutated = random.randint(0, c.numHiddenNeurons-1)
        columnMutated = random.randint(0, len(self.joints)-1)
        self.weightsToMotor[rowMutated, columnMutated] = random.random() * 2 - 1


    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID


    def Node(self, recursiveLimit, posi, sizzle, firstIter=False):
        pyrosim.Send_Cube(name=str(self.currentLink), pos=posi, size=sizzle)
        existsNeuron = random.random() < 0.5
        if existsNeuron:
            self.links.append(str(self.currentLink))
        if recursiveLimit > 0:
            self.Edge(sizzle, recursiveLimit-1, posi, firstIter=firstIter)
        return


    def Edge(self, sizzle, rL, posi, firstIter=False):
        jName = str(self.currentLink) + "_" + str(self.currentLink + 1)
        jAxisSel = random.random()
        jointPos = [sizzle[0], 0, 0]
        if firstIter:
            jointPos[0] /= 2
            jointPos[2] = posi[2]
            posi[2] = 0
        if jAxisSel < 0.5:
            jAxis = "1 0 0"
        elif jAxisSel < 0.95:
            jAxis = "0 1 0"
        else:
            jAxis = "0 0 1"
        pyrosim.Send_Joint(name=jName, 
                           parent=str(self.currentLink), 
                           child=str(self.currentLink+1), 
                           type="revolute", 
                           position=jointPos, 
                           jointAxis=jAxis)
        self.joints.append(jName)
        self.currentLink += 1
        for i in range(len(sizzle)-1):
            sizzle[i] *= random.gauss(1, 0.3)
        posi[0] = sizzle[0]/2
        self.Node(rL, posi, sizzle)
        return

        