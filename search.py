import parallelHillClimber


def run_sim():
    """
    Creates a parallelHillClimber, runs evolution, then shows the best result.
    """
    phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
    # phc.Show_Best()
    phc.Evolve()
    x = input("Press enter to show the best solution found, or 1 to show the pickle jar.\n")
    if x == '1':
        phc.showPickleJar()
    else:
        phc.Show_Best(lambda x, y: x.fitness > y.fitness)


def show_pickleJar():
    phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
    phc.showPickleJar()


if __name__ == "__main__":
    run_sim()
    