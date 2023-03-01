import pyrosim.pyrosim as pyrosim


class LINKS:
    def __init__(self, name, position, size, sensor=False) -> None:
        self.name = name
        self.position = position
        self.size = size
        self.sensor = sensor
        if sensor:
            self.colorString = '<color rgba="0 1 0 1"/>'
            self.color = "Green"
        else:
            self.colorString = '<color rgba="0 0 1 1"/>'
            self.color = "Blue"


    def writeToFile(self):
        pyrosim.Send_Cube(name=self.name, pos=self.position, size=self.size, colorString=self.colorString, color=self.color)