import random
import pyrosim.pyrosim as pyrosim

def makeTower(x, y, z, length, width, height):
    for i in range(10):
        pyrosim.Send_Cube(name="Box"+str(i), pos=[x, y, z], size=[length, width, height])
        z += height / 2
        length *= 0.9
        height *= 0.9
        width *= 0.9
        z += height / 2


def makeTowerRow(xo, yo, lo, num):
    for i in range(num):
        makeTower(xo + i*lo, yo, lo/2, lo, lo, lo)



def makeSquareOfTowers(xo, yo, side, num):
    for i in range(num):
        makeTowerRow(xo, yo + i*side, side, num)


def sendCube(nomen, x=0, y=0, side=1, zoff = 0):
    z = side / 2 + zoff# so that it starts on the floor
    pyrosim.Send_Cube(name=nomen, pos=[x, y, z], size=[side, side, side])


def Create_World():
    pyrosim.Start_SDF("world.sdf")
    sendCube("Box", -2, -2)
    pyrosim.End()


def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    sendCube("Torso", zoff=1)
    #pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , type = "revolute", position = [1, 0, 1])
    pyrosim.Send_Joint( name = "Torso_Backleg" , parent= "Torso" , child = "Backleg" , type = "revolute", position = [0.5, 0, 1])
    sendCube("Backleg", x=0.5, zoff=-1)
    pyrosim.Send_Joint( name = "Torso_Frontleg" , parent= "Torso" , child = "Frontleg" , type = "revolute", position = [-0.5, 0, 1])
    sendCube("Frontleg", x=-0.5, zoff=-1)
    pyrosim.End()


def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0, linkName= "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1, linkName= "Backleg")
    pyrosim.Send_Sensor_Neuron(name = 2, linkName= "Frontleg")
    pyrosim.Send_Motor_Neuron(name = 3, jointName= "Torso_Backleg")
    pyrosim.Send_Motor_Neuron(name = 4, jointName= "Torso_Frontleg")
    for sensor in range(3):
        for motor in range(3,5):
            w = 2*random.random() - 1
            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=w)
    pyrosim.End()


def Generate():
    Create_World()
    Generate_Body()
    Generate_Brain()

