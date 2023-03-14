import os
import solution
import constants as c
import copy


class PARALLEL_HILL_CLIMBER:
    """
    A class that implements parallel hill climbing.

    Attributes:
    parents (dict[int, solution.SOLUTION]): Contains the parent solutions in each "silo".
    children (dict[int, solution.SOLUTION]):  Contains the child solutions in each "silo" evolved from the parents.
    nextAvailableID (int):  Provides IDs to the solutions.
    evolveCalled (bool):  Used by ShowBest to prevent errors by indicating whether evolution has been run.
    """
    def __init__(self) -> None:
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        os.system("del body*.urdf")
        self.parents = dict()
        self.nextAvailableID = 0
        self.evolveCalled = False
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self) -> None:
        """
        Runs evolution for as many generations as specified.

        Consider modifying to pass the currentGeneration to Evolve_For_One_Generation to pass it to the body constructor.
        """
        self.evolveCalled = True
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()


    def Evolve_For_One_Generation(self) -> None:
        """
        Runs evolution for a generation by Spawning new children, mutating them, evaluating them, and then selecting the children or parents in each "silo".
        """
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # self.Print()
        self.Select(fitter=lambda p, c: p.fitness > c.fitness)


    def Evaluate(self, solutions: dict[int, solution.SOLUTION]) -> None:
        """
        Runs the simulation for a given set of solutions.

        Parameters:
        solutions:  A dictionary where the values are the solutions to be simulated.
        """
        for solution in solutions.values():
            solution.Start_Simulation(show="GUI")
        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()


    def Print(self) -> None:
        """
        Prints out the parents, their children, and the relative fitnesses of each.
        """
        print("\n")
        for key in self.parents.keys():
            print("P: ", self.parents[key].fitness, " C: ", self.children[key].fitness)
        print("\n")


    def Spawn(self) -> None:
        """
        Creates children for each parent.
        """
        self.children = dict()
        for key, parent in self.parents.items():
            # Reconsider the deepcopy
            self.children[key] = copy.deepcopy(parent)
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1


    def Show_Best(self, fitter) -> None:
        """
        Determines the fittest of the parallel "silos" and displays it.

        Parameters:
        fitter:  A function that returns true if the parent's fitness is superior.
        """
        best = self.parents[0]
        if self.evolveCalled:
            for parent in self.parents.values():
                if fitter(parent, best):
                    best = parent
        best.Start_Simulation(show="GUI")


    def Mutate(self) -> None:
        """
        A function that calls solution's mutate method on all of the children.
        """
        for child in self.children.values():
            child.Mutate()


    def Select(self, fitter) -> None:
        """
        For each "silo" within parallel hill climber, selects whether the parent or child will be kept based on a fitness function.

        Parameters:
        fitter:  a function that returns True if the child's fitness exceeds the parent's.
        """
        for key in self.parents.keys():
            parent = self.parents[key]
            child = self.children[key]
            if fitter(parent, child):
                self.parents[key] = child