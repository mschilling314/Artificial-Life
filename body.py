import pyrosim.pyrosim as pyrosim
import links
import joints
import constants as c
import numpy as np


class BODY:
    def __init__(self, id) -> None:
        self.id = id
        self.links = []
        self.joints = []
        self.numSensors = 0


    def addLink(self, name, position, size, sensor=False):
        l = links.LINKS(name, position, size, sensor)
        if sensor:
            self.numSensors += 1
        self.links.append(l)


    def addJoint(self, name, parent, child, type, position, axis):
        j = joints.JOINTS(name, parent, child, type, position, axis)
        self.joints.append(j)


    def writeBodyToFile(self):
        pyrosim.Start_URDF("body" + str(self.id) + ".urdf")
        for link in self.links:
            link.writeToFile()
        for joint in self.joints:
            joint.writeToFile()
        pyrosim.End()


    # Not being used yet
    def makeBrain(self, numLayers, layerWidth):
        # First, create the weights going from the input layer to the first hidden layer
        self.weightsToHidden = np.random.rand(self.numSensors, layerWidth)
        self.weightsToHidden = 2 * self.weightsToHidden - 1
        # Next, create a tensor that has numLayers-1 fully connected layers
        self.hiddenWeights = np.random.rand(layerWidth, layerWidth, numLayers-1)
        self.hiddenWeights = 2 * self.hiddenWeights - 1
        # Lastly, create the weights to the output layer
        self.weightsToMotor = np.random.rand(layerWidth, len(self.joints))
        self.weightsToMotor = 2 * self.weightsToMotor - 1

