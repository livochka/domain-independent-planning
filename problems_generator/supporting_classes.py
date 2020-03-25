from abc import ABC
from map import Node, Connection, Map
from random import randint

class Unit(ABC):
    """
    Abstract base class that represents a unit
    """
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
    FACT_AT = "(at {} {})"
    FACT_DESTINATION = "(destination {} {})"
    FACT_WAITING = "(waiting {})"
    FACT_PAYMENT = "(= (payment {}) {})"

    def __init__(self, map):
        self.map = map
        self.number = Person.ID
        Person.ID += 1

        start, goal, distance = self.generate_ride()
        self.location = start
        self.destination = goal
        self.payment = self.pricing_policy(distance)


    def generate_ride(self):
        start = randint(0, len(self.map) - 1)
        goal = randint(0, len(self.map) - 1)
        while goal == start:
            goal = randint(0, len(self.map) - 1)
        print(start, goal)
        distance = self.map.get_distance(start, goal)
        print(distance)
        return self.map.get_node(start), self.map.get_node(goal), distance

    def pricing_policy(self, distance, fc=30, vc=10):
        return fc + vc * distance

    def __str__(self):
        return Person.__name__.lower() + str(self.number)

    def get_initial_state(self):
        return [Person.FACT_AT.format(str(self), str(self.location)),
                Person.FACT_DESTINATION.format(str(self), str(self.destination)),
                Person.FACT_WAITING.format(str(self)),
                Person.FACT_PAYMENT.format(str(self), str(self.payment))]


class Player:

    ID = 0
    FACT_ENEMY = "(is-enemy {} {})"
    FACT_OWNS_UNIT = "(has-unit {} {})"
    PREFERENCES = "(preference {} (is-delivered {} {}))"
    VIOLATED = "(* {} (is-violated {}))"
    GOAL = "(:goal (and \n\t\t{}))"
    METRIC = "(:metric {} (+ \n\t\t{}))"

    def __init__(self, units=None, enemies=None, passengers=None):
        self.number = Player.ID
        Player.ID += 1

        self.units = units
        self.enemies = enemies
        self.passengers = passengers

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

    def add_passengers(self,passengers):
        self.passengers = passengers

    def get_initial_state(self):
        facts = []
        for enemy in self.enemies:
            facts.append(Player.FACT_ENEMY.format(str(self), str(enemy)))
        for unit in self.units:
            facts.append(Player.FACT_OWNS_UNIT.format(str(self), str(unit)))
        return facts

    def goal(self):
        preferences = []
        for pas in self.passengers:
            pref_name = '-'.join(["delivered", str(self), str(pas)])
            preferences.append(Player.PREFERENCES.format(pref_name,  str(pas), str(self)))
        return Player.GOAL.format("\n\t\t".join(preferences))

    def metric(self, maximize=False):
        optim = "maximize" if maximize else "minimize"
        preferences = []
        for pas in self.passengers:
            pref_name = '-'.join(["delivered", str(self), str(pas)])
            preferences.append(Player.VIOLATED.format(str(pas.payment), pref_name))
        return Player.METRIC.format(optim, "\n\t\t".join(preferences))



