from collections import defaultdict
from copy import deepcopy

from lib.input import read_lines


ACTIVE = '#'
INACTIVE = '.'

input = read_lines(17)


def neighbours(x, y, z):
  for i in range(x - 1, x + 2):
    for j in range(y - 1, y + 2):
      for k in range(z - 1, z + 2):
        if (i, j, k) != (x, y, z):
          yield (i, j, k)


def create_dimension(Type):
  return defaultdict(lambda: defaultdict(lambda: defaultdict(Type)))


def cycle(states):
  counts = create_dimension(int)

  for z, z_axis in states.items():
    for y, y_axis in z_axis.items():
      for x, state in y_axis.items():
        for i, j, k in neighbours(x, y, z):
          if state == ACTIVE:
            counts[k][j][i] += 1
          else:
            counts[k][j][i]

  new_states = deepcopy(states)

  for z, z_axis in counts.items():
    for y, y_axis in z_axis.items():
      for x, state in y_axis.items():
        if states[z][y][x] == ACTIVE:
          if counts[z][y][x] not in (2, 3):
            new_states[z][y][x] = INACTIVE
            continue
        if states[z][y][x] == INACTIVE:
          if counts[z][y][x] == 3:
            new_states[z][y][x] = ACTIVE
            continue

  return new_states


def part_1():
  states = create_dimension(lambda: INACTIVE)

  for x, line in enumerate(input):
    for y, state in enumerate(line):
      states[0][y][x] = state

  for _ in range(6):
    states = cycle(states)

  count = 0

  for z, z_axis in sorted(states.items()):
    print('z = {}'.format(z))
    for y, y_axis in sorted(z_axis.items()):
      for x, state in sorted(y_axis.items()):
        if state == ACTIVE:
          count += 1
        print((x, y), state)
      print()
    print()
    print()

  return count


def part_2():
  return None


solve_1 = lambda: part_1()
solve_2 = lambda: part_2()
