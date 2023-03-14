from simulation import SIMULATION


def Simulate(links: list[str], gui: str="DIRECT", solutionID: int=0) -> None:
    """
    Starts and runs a simulation, then gets the fitness of the simulated robot.

    Parameters:
    links:  Used to pass down the links that have sensor neurons to Robot.
    gui:  Either "DIRECT" or "GUI", tells whether to show the simulation or not.
    solutionID:  Gives the ID of the solution to pass further down for file access.
    """
    simulation = SIMULATION(pretty=gui, solnID = solutionID, lynx=links)
    simulation.Run()
    simulation.Get_Fitness()


if __name__ == '__main__':
    Simulate(gui="GUI", solutionID=0)
    # Simulate(gui="GUI", solutionID=0)
    Simulate(gui="GUI", solutionID=1)
    
