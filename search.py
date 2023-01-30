import generate
import simulate
import hillclimber


def run_sim():
    hc = hillclimber.HILL_CLIMBER()
    hc.Show_Best()
    hc.Evolve()
    hc.Show_Best()
    # generate.Generate()
    # simulate.Simulate()


for i in range(1):
    run_sim()
    