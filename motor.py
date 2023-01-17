import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName) -> None:
        self.jointName = jointName
        self.Prepare_To_Act()


    def Prepare_To_Act(self):
        self.frequency = c.frequency
        self.amplitude = c.amplitude
        self.phaseOffset = c.phaseOffset
        if self.jointName == "Torso_Frontleg":
            self.frequency *= 2
            print("\nstatement hit\n")
        x = np.linspace(0, 2*c.pi, c.iter)
        self.motorValues = self.amplitude * np.sin(self.frequency * x + self.phaseOffset)

    
    def Set_Value(self, i, robot):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robot.robotID, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = self.motorValues[i], maxForce = c.maxForce)


    