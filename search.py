import generate
import simulate


def run_sim():
    generate.Generate()
    simulate.Simulate()


for i in range(5):
    run_sim()
    