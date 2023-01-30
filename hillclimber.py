import solution
import constants as c
import copy


class HILL_CLIMBER:
    def __init__(self) -> None:
        self.parent = solution.SOLUTION()


    def Evolve(self):
        self.parent.Evaluate()
        for currentGeneration in range(c.numberOfGenerations):
            self.Spawn()
            self.Mutate()
            self.child.Evaluate()
            self.Select()


    def Spawn(self):
        self.child = copy.deepcopy(self.parent)


    def Mutate(self):
        self.child.Mutate()
        # print(self.parent.weights)
        # print(self.child.weights)

    def Select(self):
        # this statement is what it is bc fitness is the x-coord which we want more negative
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child