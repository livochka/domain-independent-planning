from problems_generator.generator import TaxiProblemGenerator


def problem_formulation_to_pddl(nnodes, nplayers, npassengers, units_details, filename="demo"):

    # creates an instance of problem from taxi domain
    problem = TaxiProblemGenerator(nnodes=nnodes, nplayers=nplayers, npassengers=npassengers, units_details=units_details)

    # visualization of taxi map
    problem.visualize_map()

    # saving problem configuration as pddl
    problem.to_pddl(filename)

    return problem


if __name__ == "__main__":

    # defining general parameters of the game
    nodes_number = 10
    nplayers = 2
    npassengers = 3

    # defining the number of units for each player with units_count[0] representing number of units player1 has
    units_count = [1, 1]
    # defining location for units of player1, ... playern
    locations = [[0], [5]]  # unit of player1 located on node0 on the map, of player2 - node5
    # number of units and their locations define the units_details variable
    units_details = {"number": units_count, "location": locations}

    problem_formulation_to_pddl(nodes_number, nplayers, npassengers, units_details)



