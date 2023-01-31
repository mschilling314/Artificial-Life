import generate
import simulate
import parallelHillClimber


def run_sim():
    phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
    phc.Show_Best()
    phc.Evolve()
    phc.Show_Best()


if __name__ == "__main__":
    run_sim()
    