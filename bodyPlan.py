import random


class BODYPLAN:
    """
    A class that contains the directed graph of an indirect encoding of the bodyplan.

    Attributes:
    bodyEdgeMatrix (list[list[int]]):  Gives the adjacency matrix of the directed graph.
    sizzles (dict[lis[float]]): Provides the size of each type of bodypart.
    """
    def __init__(self) -> None:
        self.bodyEdgeMatrix = [[0, 4],
                           [0, 1]]
        # self.bodyEdgeMatrix = [[1]]
        self.sizzles = {0: [1,2,0.5],
                        1: [.5, .5, 1]}


    def maxHeight(self) -> float:
        """
        A function that returns the maximum height within the bodyplan.
        """
        res = self.sizzles[0][2]
        for size in self.sizzles.values():
            if size[2] > res:
                res = size[2]
        return res
    

    def mutateSizes(self, node: int) -> None:
        """
        A function that alters the sizes within a bodyplan.

        Parameters:
        node:  Which node we modify the size of.
        """
        for i in range(len(self.sizzles[node])):
            self.sizzles[node][i] *= random.gauss(1, 0.3)