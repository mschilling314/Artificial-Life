import solution


class HILL_CLIMBER:
    def __init__(self) -> None:
        self.parent = solution.SOLUTION()


    def Evolve(self):
        self.parent.Evaluate()