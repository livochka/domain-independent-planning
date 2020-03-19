from abc import ABC
from map import Node, Connection, Map
from random import randint

class Unit(ABC):

    FACT_AT = "(at {} {})"
    FACT_EMPTY = "(empty {})"

    def __init__(self, number, location=None):
        self.location = location
        self.number = number

    def __str__(self):
        return self.__class__.__name__.lower() + str(self.number)

    def add_location(self, location):
        self.location = location

    def get_initial_state(self):
        return [Unit.FACT_AT.format(str(self), str(self.location)),
                Unit.FACT_EMPTY.format(str(self))]


class Car(Unit):
    """
    Represents a unit of subtype car
    """

    ID = 0

    def __init__(self, location=None):
        """
        :param location: Node,
            location on the map that assigned to the Car
        """
        super().__init__(Car.ID, location)
        Car.ID += 1


class Person:

    ID = 0

    def __init__(self, map):
        self.map = map

        start, goal, distance = self.generate_ride()
        self.location = start
        self.destination = goal
        self.payment = None

    def generate_ride(self):
        start = randint(len(self.map))
        goal = randint(len(self.map))
        while goal == start:
            goal = randint(len(self.map))
        distance = self.map.get_distance(start, goal)
        return self.map.get_node(start), self.map.get_node(goal), distance

    def pricing_policy(self, distance, fc=50, vc=10):
        return fc + vc * distance



class Player:

    ID = 0
    FACT_ENEMY = "(is-enemy {} {})"
    FACT_OWNS_UNIT = "(has-unit {} {})"
    FACT_TOTAL_REVENUE = "(= (total-revenue {}) 0)"

    def __init__(self, units=None, enemies=None):
        self.number = Player.ID
        Player.ID += 1

        self.units = units
        self.enemies = enemies

    def __str__(self):
        return Player.__name__.lower() + str(self.number)

    def add_enemy(self, enemy_player):
        if self.enemies:
            self.enemies.append(enemy_player)
        else:
            self.enemies = [enemy_player]

    def add_unit(self, unit):
        if self.units:
            self.units.append(unit)
        else:
            self.units = [unit]

    def get_units(self):
        return self.units

    def get_initial_state(self):
        facts = [Player.FACT_TOTAL_REVENUE.format(str(self))]
        for enemy in self.enemies:
            facts.append(Player.FACT_ENEMY.format(str(self), str(enemy)))
        for unit in self.units:
            facts.append(Player.FACT_OWNS_UNIT.format(str(self), str(unit)))

        return facts
