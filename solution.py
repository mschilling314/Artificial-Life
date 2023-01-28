import numpy as np


class SOLUTION:
    def __init__(self) -> None:
        self.weights = np.random.rand(3, 2)
        self.weights = 2 * self.weights - 1