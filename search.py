import parallelHillClimber


def run_sim():
    """
    Creates a parallelHillClimber, runs evolution, then shows the best result.
    """
    phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
    # phc.Show_Best()
    phc.Evolve()
    input("Press enter to continue.\n")
    phc.Show_Best(lambda x, y: x.fitness > y.fitness)


if __name__ == "__main__":
    run_sim()
    