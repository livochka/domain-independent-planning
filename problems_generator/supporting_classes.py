from abc import ABC
from map import Node, Connection, Map

class Unit(ABC):

    def __init__(self, name, location):
        self._location = location
        self._name = name

    def add_location(self, location):
        self._location = location


class Car(Unit):

    def __init__(self, name, location=None):
        super().__init__(name, location)


class Player:

    def __init__(self, name, units=None, enemies=None):
        self._name = name
        self._units = units
        self._enemies = enemies

    def add_enemy(self, enemy_player):
        if self._enemies:
            self._enemies.append(enemy_player)
        else:
            self._enemies = [enemy_player]

    def add_unit(self, unit):
        if self._units:
            self._units.append(unit)
        else:
            self._units = [unit]


class TaxiProblem:

    def __init__(self):
        pass
