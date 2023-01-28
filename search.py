import generate
import simulate
import hillclimber


def run_sim():
    hc = hillclimber.HILL_CLIMBER()
    hc.Evolve()
    # generate.Generate()
    # simulate.Simulate()


for i in range(5):
    run_sim()
    