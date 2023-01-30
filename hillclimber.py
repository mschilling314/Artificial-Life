import solution
import constants as c


class HILL_CLIMBER:
    def __init__(self) -> None:
        self.parent = solution.SOLUTION()


    def Evolve(self):
        self.parent.Evaluate()
        for currentGeneration in c.numberOfGenerations:
            self.Spawn()
            self.Mutate()
            self.child.Evaluate()
            self.Select()


    def Spawn(self):
        pass


    def Mutate(self):
        pass

    def Select(self):
        pass