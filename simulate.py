import generate
from simulation import SIMULATION



# generate

def Simulate(gui="DIRECT"):
    simulation = SIMULATION(pretty=gui)
    simulation.Run()
    simulation.Get_Fitness()
