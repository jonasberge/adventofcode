from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


input = read_lines(14)

pattern = re.compile(r"^(mem|mask)(?:\[([0-9]+)\])?\s=\s([0-9X]+)$")


class Program:
  def __init__(self):
    self._and_mask = 0
    self._or_mask = 0
    self._memory = {}

  def set_mask(self, value):
    self._and_mask = int(value.replace('1', '0').replace('X', '1'), 2)
    self._or_mask = int(value.replace('X', '0'),  2)

  def __setitem__(self, address, value):
    value &= self._and_mask
    value |= self._or_mask
    self._memory[address] = value

  def __getitem__(self, address):
    return self._memory[address]


def part_1():
  program = Program()

  for line in input:
    match = re.match(pattern, line)
    which, address, value = match.groups()

    if which == 'mask':
      program.set_mask(value)
    elif which == 'mem':
      address, value = int(address), int(value)
      program[address] = value

  return sum(value for value in program._memory.values())


def part_2():
  return None


solve_1 = lambda: part_1()
solve_2 = lambda: part_2()
