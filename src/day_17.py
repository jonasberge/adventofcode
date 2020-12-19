from collections import defaultdict
from itertools import product
from copy import deepcopy

from lib.input import read_lines


ACTIVE = '#'
INACTIVE = '.'

input = read_lines(17)


def neighbours(*pos):
  if len(pos) == 1:
    yield (pos[0] - 1,)
    yield (pos[0] + 1,)
    return

  lhs, rhs = pos[:1], pos[1:]
  l_begin, l_prev = None, None

  lhs_gen = neighbours(*lhs)
  rhs_gen = neighbours(*rhs)

  for l, r in product(lhs_gen, rhs_gen):
    if l_begin == None:
      l_begin = l[0]

    yield l + r

    if l_prev == None or l[0] > l_prev:
      yield l + rhs
      l_prev = l[0]

    if l[0] == l_begin:
      yield lhs + r


def cycle(states):
  counts = defaultdict(int)

  for position, state in states.items():
    for neighbour in neighbours(*position):
      if state == ACTIVE:
        counts[neighbour] += 1
      else:
        counts[neighbour]

  new_states = deepcopy(states)

  for position, state in counts.items():
    if states[position] == ACTIVE:
      if counts[position] not in (2, 3):
        new_states[position] = INACTIVE
        continue
    if states[position] == INACTIVE:
      if counts[position] == 3:
        new_states[position] = ACTIVE
        continue

  return new_states


def solve(dimension):
  states = defaultdict(lambda: INACTIVE)

  for x, line in enumerate(input):
    for y, state in enumerate(line):
      states[(x, y) + (0,) * (dimension - 2)] = state

  for _ in range(6):
    states = cycle(states)

  return sum(1 for x in states.values() if x == ACTIVE)


solve_1 = lambda: solve(3)
solve_2 = lambda: solve(4)
