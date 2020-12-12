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


class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def rotate_around_origin(self, degrees):
    degrees %= 360
    if degrees == 180: self.x, self.y = -self.x, -self.y
    elif degrees == 90: self.x, self.y = self.y, -self.x
    elif degrees == 270: self.x, self.y = -self.y, self.x

  def move(self, direction, distance):
    if direction == NORTH: self.y += distance
    elif direction == SOUTH: self.y -= distance
    elif direction == EAST: self.x += distance
    elif direction == WEST: self.x -= distance


class Location(Position):
  def __init__(self, /, position=(0, 0), facing=NORTH):
    super().__init__(position[0], position[1])
    self.direction = Direction(facing)

  def rotate(self, degrees):
    self.direction.rotate(degrees)

  def forward(self, distance):
    self.move(str(self.direction), distance)


def manhattan(x, y):
  return abs(x) + abs(y)


def actions():
  for line in input:
    yield line[0], int(line[1:])


def navigate():
  ship = Location(facing=EAST)

  for action, amount in actions():
    if action == FORWARD: ship.forward(amount)
    elif action == RIGHT: ship.rotate(amount)
    elif action == LEFT: ship.rotate(-amount)
    else: ship.move(action, amount)

  return manhattan(ship.x, ship.y)


def navigate_2():
  ship = Location(facing=EAST)
  waypoint = Position(10, 1)

  for action, amount in actions():
    if action == FORWARD:
      ship.x += amount * waypoint.x
      ship.y += amount * waypoint.y
    elif action == RIGHT: waypoint.rotate_around_origin(amount)
    elif action == LEFT: waypoint.rotate_around_origin(-amount)
    else: waypoint.move(action, amount)

  return manhattan(ship.x, ship.y)


solve_1 = lambda: navigate()
solve_2 = lambda: navigate_2()
