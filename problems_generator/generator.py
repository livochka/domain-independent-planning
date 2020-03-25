from map import Node, Connection, Map
from supporting_classes import Player, Car, Person
from random import randint


class TaxiProblemGenerator:
    """
    Created to generate PDDL instances of taxi problem domain
    """

    FILE_STRUCTURE = {"objects": {}, "init": {}, "goal": {}, "metric": {}}

    def __init__(self, random_map=True, nnodes=10, nplayers=2, npassengers=4, units_details={},  map=None):
        """
        Initialization of the problem instance
        :param random_map: bool,
            if True, map would be generated randomly
        :param nnodes: int, default 10
            number of nodes, parametrization of randomly generated map
        :param map: Map, default None
            needed only if random_map = False
        :param nplayers: int,
            number of players in the game
        :param units_details: dict of type {"number" : [int_1, ..., int_n],
                                            "location": [[loc1, ..., loc_int1], ..., [loc1, ..., loc_intn]}
            parametrizes number of units each player has and their locations
        """

        if random_map:
            self.map = Map().generate_random_configuration(nnodes)
        else:
            self.map = map

        self.players = self.create_players(nplayers)
        self.units = self.create_assign_units(units_details)
        self.passengers = self.create_passengers(npassengers)

        TaxiProblemGenerator.FILE_STRUCTURE["objects"].update({"player": [str(pl) for pl in self.players]})
        TaxiProblemGenerator.FILE_STRUCTURE["objects"].update({"unit": [str(un) for un in self.units]})
        TaxiProblemGenerator.FILE_STRUCTURE["objects"].update({"person": [str(pr) for pr in self.passengers]})
        TaxiProblemGenerator.FILE_STRUCTURE["objects"].update({"location": [str(loc) for loc in self.map.get_objects()]})

        TaxiProblemGenerator.FILE_STRUCTURE["init"].update({"player": [pl.get_initial_state() for pl in self.players]})
        TaxiProblemGenerator.FILE_STRUCTURE["init"].update({"unit": [un.get_initial_state() for un in self.units]})
        TaxiProblemGenerator.FILE_STRUCTURE["init"].update({"person": [pr.get_initial_state() for pr in self.passengers]})
        TaxiProblemGenerator.FILE_STRUCTURE["init"].update({"location": self.map.get_initial_state()})

        #TaxiProblemGenerator.FILE_STRUCTURE["goal"].update({"person": [pr.goal_state() for pr in self.passengers]})

    @staticmethod
    def create_players(n):
        """
        Creates n instances of class Player
        :param n: int,
            number of players in the game
        :return: list(),
            list of Players
        """
        players = [Player() for x in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                players[i].add_enemy(players[j])
                players[j].add_enemy(players[i])
        return players

    def create_assign_units(self, units_details):
        """
        Creates units and assign them to players
        :param units_details: dict of type {"number" : [int_1, ..., int_n],
                                            "location": [[loc1, ..., loc_int1], ..., [loc1, ..., loc_intn]}
        :return: list(Unit1, Unit2, ..., Unitn)
            list of all units
        """
        all_units = []
        for i, player in enumerate(self.players):

            nunits = units_details["number"][i]
            locations = units_details["location"][i]

            for u in range(nunits):
                location = self.map.get_node(locations[u])
                unit = Car(location)
                player.add_unit(unit)
                location.add_obj(unit)

            all_units.extend(player.get_units())
        return all_units

    def create_passengers(self, npas):
        passengers = []
        for i in range(npas):
            passengers.append(Person(self.map))

        for pl in self.players:
            pl.add_passengers(passengers)

        return passengers



    def visualize_map(self):
        """
        Visualization of a map
        """
        self.map.visualize()

    def fill_objects(self):
        objects = ""
        for key in self.FILE_STRUCTURE["objects"]:
            objects += " ".join(self.FILE_STRUCTURE["objects"][key]) + " - " + key + "\n\t\t"
        return objects

    def to_pddl(self, problem_name):
        template = "(define (problem {})\n\t(:domain taxi)\n\t" \
                   "(:objects {})\n\t(:init {})\n\t{}"

        objects, init, goal = "\n\t\t", "\n\t\t", ""

        # adding objects and types data into objects variable
        for key in self.FILE_STRUCTURE["objects"]:
            objects += " ".join(self.FILE_STRUCTURE["objects"][key]) + " - " + key + "\n\t\t"

        # adding initial statements into init variable
        for key in self.FILE_STRUCTURE["init"]:
            for object_initial_states in self.FILE_STRUCTURE["init"][key]:
                init += "\n\t\t".join(object_initial_states) + "\n\t\t"
            init += "\n\t\t"
        # adding the goal and the metric
        for players in self.players:
            goal += players.goal() + "\n\n\t"
            goal += players.metric() + "\n\n\t"


        template = template.format(problem_name, objects, init, goal)




        with open("problem-{}.pddl".format(problem_name), "w") as file:
            file.writelines(template)
