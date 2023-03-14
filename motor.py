import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    """
    A simple class to interface between the robot and pyrosim's Motors/Joints.

    Attributes:
    jointName (str): The name of the joint this motor is attached to.
    """
    def __init__(self, jointName) -> None:
        self.jointName = jointName

    
    def Set_Value(self, desiredAngle: float, robotID: int) -> None:
        """
        Sends the desired angle and robotID to pyrosim to update motor values.

        Parameters:
        desiredAngle:  The angle that the joint wants to be at, determined by the neural net.
        robotID:  The unique integer ID of the robot that we are targeting.
        """
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotID, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = desiredAngle, maxForce = c.maxForce)


    