import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim


class SENSOR:
    """
    A simple class that allows the robot to interface with pyrosim's sensor capabilities.

    Attributes:
    linkName (str):  The name of the link this sensor is attached to.
    values (np.array):  The values that the sensor in this link takes on at each time step.
    """
    def __init__(self, linkName) -> None:
        self.linkName = linkName
        self.values = np.zeros(c.iter)


    def Get_Value(self, i):
        """
        Writes the value of the touch sensor at the timestep i into an array of sensor values.

        Parameters:
        i:  The timestep.
        """
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        # if i == len(self.values) - 1:
        #     print(self.values)