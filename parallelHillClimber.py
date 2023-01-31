import solution
import constants as c
import copy


class PARALLEL_HILL_CLIMBER:
    def __init__(self) -> None:
        self.parents = dict()
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION()


    def Evolve(self):
        for parent in self.parents.values():
            parent.Evaluate(show="GUI")
        # self.parent.Evaluate()
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Spawn()
        #     self.Mutate()
        #     self.child.Evaluate()
        #     self.Print()
        #     self.Select()


    def Print(self):
        print("\nP: ", self.parent.fitness, " C: ", self.child.fitness, "\n")


    def Spawn(self):
        self.child = copy.deepcopy(self.parent)


    def Show_Best(self):
        pass
        # self.parent.Evaluate(show="GUI")


    def Mutate(self):
        self.child.Mutate()
        # print(self.parent.weights)
        # print(self.child.weights)

    def Select(self):
        # this statement is what it is bc fitness is the x-coord which we want more negative
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child