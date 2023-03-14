import random
import numpy as np


class BODYPLAN:
    """
    A class that contains the directed graph of an indirect encoding of the bodyplan.

    Attributes:
    bodyEdgeMatrix (np.array):  Gives the adjacency matrix of the directed graph, all entries must be ints.
    sizzles (dict[list[float]]): Provides the size of each type of bodypart.
    """
    def __init__(self, 
                 adjacencyMatrix: np.array=np.array([[0, 2],
                                                     [0, 1]]),
                 size: dict[int, list[float]]={0: [1,2,0.5],
                                               1: [.5, .5, 1]}) -> None:
        self.bodyEdgeMatrix = adjacencyMatrix
        # self.bodyEdgeMatrix = [[1]]
        self.sizzles = size


    def maxHeight(self) -> float:
        """
        A function that returns the maximum height within the bodyplan.
        """
        res = self.sizzles[0][2]
        for size in self.sizzles.values():
            if size[2] > res:
                res = size[2]
        return res
    

    def addNode(self, weightsIn: list[list[int]]=[], weightsOut: list[list[int]]=[], size: list[float]=[0.5, 0.5, 0.5]) -> None:
        """
        Meant to add a node, signifying the addition of a new bodypart, and modifying the bodyplan.

        Parameters:
        weightsIn:  Integer list of list, weight = [sourceNode, weightOfEdge]
        weightsOut:  Integer list of list, weight = [sourceNode, weightOfEdge]
        size:  Gives the (initial) size of the new part
        """
        node = len(self.sizzles)
        self.bodyEdgeMatrix = np.hstack((self.bodyEdgeMatrix, np.zeros((self.bodyEdgeMatrix.shape[0], 1))))
        self.bodyEdgeMatrix = np.vstack((self.bodyEdgeMatrix, np.zeros((1, self.bodyEdgeMatrix.shape[1]))))
        for weight in weightsIn:
            self.modifyEdge(weight[0], node, weight[1])
        for weight in weightsOut:
            self.modifyEdge(node, weight[0], weight[1])
        self.sizzles[node] = size
    

    def mutateSizes(self, node: int) -> None:
        """
        A function that alters the sizes within a bodyplan.

        Parameters:
        node:  Which node we modify the size of.
        """
        if node not in self.sizzles:
            return
        for i in range(len(self.sizzles[node])):
            self.sizzles[node][i] *= random.gauss(1, 0.3)


    def modifyEdge(self, sourceNode: int, destNode: int, newWeight: int):
        """
        Allows the modification of existing edges within the bodyplan, changing the number of parts allowed.

        Parameters:
        sourceNode:  The origin node.
        destNode:  The destination node.
        newWeight:  The new weight of the edge, in [0, 4].
        """
        if newWeight < 0:
            newWeight = 0
        if newWeight > 4:
            newWeight = 4
        if (sourceNode not in self.sizzles) or (destNode not in self.sizzles):
            # Prevents indexing errors.
            return
        self.bodyEdgeMatrix[sourceNode, destNode] = newWeight


    def deleteNode(self, node:int) -> None:
        """
        Doesn't actually delete the node, just sets it's weights to zero so that it can't be reached.

        Parameters: 
        node: The node to be "deleted".
        """
        for i in len(self.sizzles):
            self.modifyEdge(i, node, 0)
            self.modifyEdge(node, i, 0)
