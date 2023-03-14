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
    """
    A class holding a possible solution to try for the fitness function.

    Attributes:
    original (bool):  Indicates whether this is the original or has been copied.
    myID (int):  An identifier for this particular solution.
    joints (list[str]):  A list of the joints within the robot.
    links (list[str]):  A list of the links within the robot that have sensor neurons.
    bodyPlan (BODYPLAN):  The bodyplan encoded in a directed graph.
    fitness (float):  A measure of how well a given solution does.
    weightsToHidden (np.array): The weights between sensor and hidden neurons.
    weightsToMotor (np.array):  The weights between hidden and motor neurons.
    coreHeight (float):  The estimated core height of the robot, calculated using the recursive limit and bodyPlan.
    """
    def __init__(self, nextAvailableID: int) -> None:
        self.myID = nextAvailableID
        self.joints = []
        self.links = []
        self.bodyPlan = BODYPLAN()
        self.original = True


    def Start_Simulation(self, show: str="DIRECT") -> None:
        """
        Creates the world, body, and brain before starting a sim in parallel. 

        Parameters:
        self: Needs to be called using solution.Start_Simulation.
        show: String of value either "DIRECT" or "GUI" to determine if the simulation should be shown or not.

        Returns: 
        Nothing.
        """
        if self.myID == 0:
            self.Create_World()
        self.links = []
        self.joints = []
        self.Create_Body()
        self.Create_Brain()
        p = multiprocessing.Process(target=simulate.Simulate, args=[self.links, show, self.myID])
        p.start()


    def Wait_For_Simulation_To_End(self) -> None:
        """
        Waits until the simulation ends, then stores the fitness of a given solution.

        Parameters:
        self:  Requires a solution to store the fitness into self.fitness.

        Returns: 
        Nothing.
        """
        fitnessFileName = "fitness"+ str(self.myID) +".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        cmd = "del fitness" + str(self.myID) + ".txt"
        os.system(cmd)


    def Create_World(self) -> None:
        """
        Creates the world.sdf file.

        Parameters:
        self:  Not acutally needed though.

        Returns: 
        Nothing.
        """
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[0, 0, 0.5], size=[1,1,1])
        pyrosim.End()


    def Create_Brain(self) -> None:
        """
        Creates the brain.nndf file for a given solution, but assumes only a single hidden layer architecture, so may need to rewrite for generality.

        Parameters:
        self:  For access to the myID, links, and joints fields.

        Returns:
        Nothing, just writes to a file.
        """
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


    def Mutate(self) -> None:
        """
        Meant to mutate one of the parts of the robot.

        Parameters:
        self: For access to the weights of the synapses.

        Returns:
        Nothing, modifies internal fields.
        """
        if len(self.links) == 0:
            return
        rowMutated = random.randint(0, len(self.links)-1)
        columnMutated = random.randint(0, c.numHiddenNeurons-1)
        self.weightsToHidden[rowMutated, columnMutated] = random.random() * 2 - 1
        rowMutated = random.randint(0, c.numHiddenNeurons-1)
        columnMutated = random.randint(0, len(self.joints)-1)
        self.weightsToMotor[rowMutated, columnMutated] = random.random() * 2 - 1


    def Set_ID(self, nextAvailableID: int) -> None:
        """
        Sets the myID fields.

        Parameters:
        self:  The object of the field being set.
        nextAvailableID:  The next available ID.

        Returns:
        Nothing, modifies self.
        """
        self.myID = nextAvailableID

    
    def createNeuron(self, name: str) -> tuple[str]:
        """
        Decides whether to create a neuron with 70% probability, if it does exist modifies the links.

        Parameters:
        self:  To modify the links field if the neuron will be created.

        Returns:
        cS:  The color string needed by pyrosim for rendering the link.
        col:  The color itself, similar to cS.
        """
        existsNeuron = random.random() < 0.7
        cS = '<color rgba="0 0 1 1"/>'
        col = 'Blue'
        if existsNeuron:
            self.links.append(name)
            cS = '<color rgba="0 1 0 1"/>'
            col = 'Green'
        return cS, col
    

    def createEdgeQueue(self, node: int) -> list[int]:
        """
        Creates a queue based on the bodyplan's directed graph, with edges added for the integer weight of the edge between nodes.

        Parameters:
        self:  Used for the bodyPlan field.
        node:  The node in the bodyplan we're moving from (an integer).

        Returns:
        edgeQueue:  A list of the nodes at the other end of a directed edge of node within bodyPlan, one for each integer weight.
        """
        edgeQueue = []
        for i in range(len(self.bodyPlan.bodyEdgeMatrix[node])):
            for _ in range(self.bodyPlan.bodyEdgeMatrix[node][i]):
                edgeQueue.append(i)
        return edgeQueue


    def Create_Body(self) -> None:
        """
        Creates a procedurally generated body from the bodyplan, and writes it to the file.  Also randomly initializes synapse weights.

        Parameters:
        self:  Used for myID fields, coreHeight, and other fields related to synapse length.

        Returns:
        Nothing, writes to a file though.
        """
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        rL = int(random.gauss(2, 0.5))
        self.coreHeight = rL*self.bodyPlan.maxHeight()
        self.Node(node=0, name="a", recursiveLimit=rL, posi=[0, 0, self.coreHeight])
        pyrosim.End()
        self.weightsToHidden = np.random.rand(len(self.links), c.numHiddenNeurons)
        self.weightsToHidden = 2 * self.weightsToHidden - 1
        self.weightsToMotor = np.random.rand(c.numHiddenNeurons, len(self.joints))
        self.weightsToMotor = 2 * self.weightsToMotor - 1


    def Node(self, node: int, name: str, recursiveLimit: int, posi: list[float]) -> None:
        """
        Meant to create links, and if necessary recurse.

        Parameters:
        self: For methods, as well as the bodyPlan field.
        node:  The bodyPlan node (an integer) we're currently working at.
        recursiveLimit:  The number of times we can recurse.
        posi:  The current position [x, y, z] within the world, can be relative.

        Returns:
        Nothing, writes to the robot.urdf file.
        """
        cS, col = self.createNeuron(name)
        s = self.bodyPlan.sizzles[node]
        self.bodyPlan.mutateSizes(node=node)
        pyrosim.Send_Cube(name=name, pos=posi, size=s, colorString= cS, color=col)
        if recursiveLimit > 0:
            edgeQueue = self.createEdgeQueue(node)
            for i, edge in enumerate(edgeQueue):
                kid = name + chr(ord("a") + i)
                self.Edge(name=name, kid=kid, rL=recursiveLimit-1, posi=posi, edgeNode=edge)
        return


    def Edge(self, name: str, kid: str, rL: int, posi: list[float], edgeNode: int) -> None:
        """
        Deals with joint creation and then calls Node to continue the process.

        Parameters:
        self: To use methods and access fields.
        name:  The name of the joint's parent.
        kid:  The name of the joint's child.
        rL:  The recursive limit, only meant to be passed back to Node.
        posi:  The position in the world.
        edgeNode:  The node we're going to within the bodyPlan.

        Returns:
        Nothing, just writes to the URDF file.

        """
        jName = name + "_" + kid
        jointPos = self.pickJointPosition(edgeNode, kid)
        posi[2] = 0
        pyrosim.Send_Joint(name=jName, 
                           parent=name, 
                           child=kid, 
                           type="revolute", 
                           position=jointPos, 
                           jointAxis=self.pickJointAxis())
        self.joints.append(jName)
        self.Node(edgeNode, kid, rL, posi)
        return


    def pickJointPosition(self, node: int, kid: str) -> list[float]:
        """
        Picks the position of the joint based on a quadruped's body plan.  Need to generalize somehow.

        Parameters:
        self:  The object being modified.
        node:  The node calling this function from bodyPlan.
        kid:  The name of the child in the joint, used to determine position.
        s:  The size of the upstream link.

        Returns:
        pos:  The position of the joint, either relative or absoluted depending on kid.
        """
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
            pos[ind] = sign * self.bodyPlan.sizzles[node][ind]
            pos[ind] /= 2
            pos[2] = self.coreHeight - self.bodyPlan.sizzles[node][2]
            print(pos)
        else:
            pos[2] = -self.bodyPlan.sizzles[node][2]
        
        return pos
        

    def pickJointAxis(self) -> str:
        """
        Meant to choose an axis about which the joint can move.

        Parameters:
        self:  Not strictly necessary.

        Returns:
        jAxis: a string corresponding to a randomly selected axis.
        """
        jAxisSel = random.random()
        if jAxisSel < 0.33:
            jAxis = "1 0 0"
        elif jAxisSel < 0.66:
            jAxis = "0 1 0"
        else:
            jAxis = "0 0 1"
        return jAxis
        
