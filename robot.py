import pybullet as p


class ROBOT:
    def __init__(self) -> None:
        self.sensors = dict()
        self.motors = dict()
        self.robotID = p.loadURDF("body.urdf")