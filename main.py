import search


if __name__ == "__main__":
    x = input("To run the simulation and create new creatures, input 1.  To show the best of previous executions, 2.")
    if x == "1":
        search.run_sim()
    if x == "2":
        search.show_pickleJar()