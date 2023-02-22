import os
import random
import time
import numpy as np
from bodyPlan import BODYPLAN
import pyrosim.pyrosim as pyrosim
import simulate
import multiprocessing
import constants as c


class SOLUTION:
    def __init__(self, nextAvailableID) -> None:
        self.myID = nextAvailableID
        self.joints = []
        self.links = []


    def Start_Simulation(self, show="DIRECT"):
        if self.myID == 0:
            self.Create_World()
        self.links = []
        self.joints = []
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
        if len(self.links) == 0:
            return
        rowMutated = random.randint(0, len(self.links)-1)
        columnMutated = random.randint(0, c.numHiddenNeurons-1)
        self.weightsToHidden[rowMutated, columnMutated] = random.random() * 2 - 1
        rowMutated = random.randint(0, c.numHiddenNeurons-1)
        columnMutated = random.randint(0, len(self.joints)-1)
        self.weightsToMotor[rowMutated, columnMutated] = random.random() * 2 - 1


    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    
    def createNeuron(self, name):
        existsNeuron = random.random() < 0.7
        cS = '<color rgba="0 0 1 1"/>'
        col = 'Blue'
        if existsNeuron:
            self.links.append(name)
            cS = '<color rgba="0 1 0 1"/>'
            col = 'Green'
        return cS, col
    

    def createEdgeQueue(self, node, bodyPlan) -> list:
        edgeQueue = []
        for i in range(len(bodyPlan.bodyEdgeMatrix[node])):
            for _ in range(bodyPlan.bodyEdgeMatrix[node][i]):
                edgeQueue.append(i)
        return edgeQueue


    def Create_Body(self):
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        rL = int(random.gauss(2, 0.5))
        bp = BODYPLAN()
        self.coreHeight = 1.5*rL*bp.maxHeight()
        self.Node(bp, 0, "a", recursiveLimit=rL, posi=[0, 0, self.coreHeight])
        pyrosim.End()
        self.weightsToHidden = np.random.rand(len(self.links), c.numHiddenNeurons)
        self.weightsToHidden = 2 * self.weightsToHidden - 1
        self.weightsToMotor = np.random.rand(c.numHiddenNeurons, len(self.joints))
        self.weightsToMotor = 2 * self.weightsToMotor - 1


    def Node(self, bodyPlan, node, name, recursiveLimit, posi):
        cS, col = self.createNeuron(name)
        s = bodyPlan.sizzles[node]
        for i in range(len(s)-1):
                s[i] *= random.gauss(1, 0.3)
        pyrosim.Send_Cube(name=name, pos=posi, size=s, colorString= cS, color=col)
        if recursiveLimit > 0:
            edgeQueue = self.createEdgeQueue(node, bodyPlan)
            for i, edge in enumerate(edgeQueue):
                kid = name + chr(ord("a") + i)
                self.Edge(bodyPlan, name, kid, s, recursiveLimit-1, posi, edge)
        return


    def Edge(self, bodyPlan, name, kid, sizzle, rL, posi, edge):
        jName = name + "_" + kid
        jointPos = self.pickJointPosition(kid, sizzle)
        posi[2] = 0
        pyrosim.Send_Joint(name=jName, 
                           parent=name, 
                           child=kid, 
                           type="revolute", 
                           position=jointPos, 
                           jointAxis=self.pickJointAxis())
        self.joints.append(jName)
        self.Node(bodyPlan, edge, kid, rL, posi)
        return


    def pickJointPosition(self, kid, s):
        pos = [0, 0, 0]
        ind = 0
        sign = 1
        
        # if it's 1st iter, fix things
        if len(kid) == 2:
            # pick orientation for a quadruped bodyplan (need to gen.)
            if kid[1] == "c" or kid[1] == "a":
                sign = -1
            if kid[1] == "c" or kid[1] == "d":
                ind = 1
            pos[ind] = sign * s[ind]
            pos[ind] /= 2
            pos[2] = self.coreHeight - s[2]
            print(pos)
        else:
            pos[2] = -s[2]
        
        return pos
        

    def pickJointAxis(self) -> str:
        jAxisSel = random.random()
        if jAxisSel < 0.33:
            jAxis = "1 0 0"
        elif jAxisSel < 0.66:
            jAxis = "0 1 0"
        else:
            jAxis = "0 0 1"
        return jAxis
        
