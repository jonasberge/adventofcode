from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


LEFT = 'L'
RIGHT = 'R'
FORWARD = 'F'

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

DEGREES = { NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270 }
DIRECTIONS = dict(reversed(d) for d in DEGREES.items())

input = read_lines(12)


class Direction:
  def __init__(self, facing):
    self.facing = facing

  def degrees(self):
    return DEGREES[self.facing]

  def rotate(self, degrees):
    rotation = (self.degrees() + degrees) % 360
    self.facing = DIRECTIONS[rotation]

  def __str__(self):
    return self.facing


class Location:
  def __init__(self, /, facing=NORTH, position=(0, 0)):
    self.direction = Direction(facing)
    self.x = position[0]
    self.y = position[1]

  def rotate(self, degrees):
    self.direction.rotate(degrees)

  def forward(self, distance):
    self.move(str(self.direction), distance)

  def move(self, direction, distance):
    if direction == NORTH: self.y += distance
    elif direction == SOUTH: self.y -= distance
    elif direction == EAST: self.x += distance
    elif direction == WEST: self.x -= distance


def navigate():
  ship = Location(facing=EAST)

  for line in input:
    action, amount = line[0], int(line[1:])

    if action == FORWARD: ship.forward(amount)
    elif action == RIGHT: ship.rotate(amount)
    elif action == LEFT: ship.rotate(-amount)
    else: ship.move(action, amount)

  return abs(ship.x) + abs(ship.y)


def part_2():
  return None


solve_1 = lambda: navigate()
solve_2 = lambda: part_2()
