import os
import solution
import constants as c
import copy
import multiprocessing


class PARALLEL_HILL_CLIMBER:
    def __init__(self) -> None:
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.parents = dict()
        self.nextAvailableID = 0
        self.evolveCalled = False
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        self.evolveCalled = True
        self.Evaluate(self.parents)
        # for p in processes:
        #     p.join()
        # self.parent.Evaluate()
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()


    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()


    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation(show="DIRECT")
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()


    def Print(self):
        print("\n")
        for key in self.parents.keys():
            print("P: ", self.parents[key].fitness, " C: ", self.children[key].fitness)
        print("\n")


    def Spawn(self):
        self.children = dict()
        for key, parent in self.parents.items():
            self.children[key] = copy.deepcopy(parent)
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1


    def Show_Best(self):
        best = self.parents[0]
        if self.evolveCalled:
            for parent in self.parents.values():
                if parent.fitness < best.fitness:
                    best = parent
        best.Start_Simulation(show="GUI")


    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        # this statement is what it is bc fitness is the x-coord which we want more negative
        for key in self.parents.keys():
            parent = self.parents[key]
            child = self.children[key]
            if parent.fitness < child.fitness:
                self.parents[key] = child