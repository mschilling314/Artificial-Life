import generate
from simulation import SIMULATION



# generate

def Simulate(gui="DIRECT", solutionID=0):
    simulation = SIMULATION(pretty=gui, solnID = solutionID)
    simulation.Run()
    simulation.Get_Fitness()


if __name__ == '__main__':
    Simulate(gui="GUI", solutionID=0)
    # Simulate(gui="GUI", solutionID=0)
    Simulate(gui="GUI", solutionID=1)
    
