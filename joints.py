class JOINTS:
    def __init__(self, name, parent, child, type, position, axis) -> None:
        self.name = name
        self.parent = parent
        self.child = child
        self.type = type
        self.position = position
        self.axis = axis


    def writeToFile(self, file):
        