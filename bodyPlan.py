class BODYPLAN:
    def __init__(self) -> None:
        self.bodyEdgeMatrix = [[0, 4],
                           [0, 1]]
        # self.bodyEdgeMatrix = [[1]]
        self.sizzles = {0: [1,2,0.5],
                        1: [.5, .5, 1]}


    def maxHeight(self):
        res = self.sizzles[0][2]
        for size in self.sizzles.values():
            if size[2] > res:
                res = size[2]
        return res