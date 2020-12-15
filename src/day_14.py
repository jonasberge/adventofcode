from itertools import combinations
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


class Program_v2(Program):
  def __init__(self):
    super().__init__()
    self._floating_masks = []

  def set_mask(self, value):
    and_mask = value.replace('1', 'X').replace('0', '1').replace('X', '0')
    self._and_mask = int(and_mask, 2)
    self._or_mask = int(value.replace('X', '0'),  2)

    floating_bits = []
    for index, bit in enumerate(value):
      if bit == 'X':
        position = len(value) - index - 1
        floating_bits.append(position)

    self._floating_masks.clear()
    for ones in range(len(floating_bits) + 1):
      for make_one in combinations(floating_bits, ones):
        mask = 0
        for bit in make_one:
          mask |= (2**bit)
        self._floating_masks.append(mask)

  def __setitem__(self, address, value):
    address &= self._and_mask
    address |= self._or_mask

    for mask in self._floating_masks:
      write_to = address | mask
      self._memory[write_to] = value


def solve(program):

  for line in input:
    match = re.match(pattern, line)
    which, address, value = match.groups()

    if which == 'mask':
      program.set_mask(value)
    elif which == 'mem':
      address, value = int(address), int(value)
      program[address] = value

  return sum(value for value in program._memory.values())


solve_1 = lambda: solve(Program())
solve_2 = lambda: solve(Program_v2())
