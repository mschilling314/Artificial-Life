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


pyrosim.Start_SDF("boxes.sdf")
length = 1
width = 1
height = 1
x = 0
y = 0
z = height / 2 # so that it starts on the floor
#pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])

makeSquareOfTowers(x, y, length, 3)



pyrosim.End()