from collections import defaultdict, deque
from copy import copy, deepcopy
import re
from math import sqrt, prod as multiply

from lib.input import read_lines


input = read_lines(20)


# 1. middle tiles will match = all four sides
# 2. edge (but not corner) tiles will match >= three of their sides
# 3. corner tiles will match >= two of their sides with other tiles


class Tile:
  def __init__(self, id, data):
    self.id = id
    self.data = data
    self._sides = self._compute_sides()

  @property
  def sides(self):
    return self._sides

  def _compute_sides(self):
    return [
      (side, ''.join(reversed(side)))
      for side in [
        self.data[0],
        self.data[-1],
        ''.join(l[0] for l in self.data),
        ''.join(l[-1] for l in self.data)
      ]
    ]


def parse_tile(it):
  match = re.match(r"^Tile (\d+):$", next(it))
  id_, = match.groups()
  id_ = int(id_)

  data = []
  for line in it:
    if not line:
      break
    data.append(line)

  return Tile(id_, data)


def parse_tiles(lines):
  it = iter(lines)
  while True:
    try:
      yield parse_tile(it)
    except StopIteration:
      return


def part_1():
  tiles = list(parse_tiles(input))

  amount = len(tiles)
  side_length = int(sqrt(amount))

  n_corner = 4
  n_edge = 4 * (side_length - 2)
  n_inner = amount - n_corner - n_edge

  print(amount, side_length)
  print(n_corner, n_edge, n_inner)

  matches_corner = list()

  for tile in tiles:

    print(tile.id)
    print('\n'.join(tile.data))
    print(tile.sides)
    print()

    matches = 0

    for other in tiles:
      if tile.id == other.id:
        continue

      has_match = False

      for side in tile.sides:
        original, flipped = side
        for other_side in other.sides:
          other_original, other_flipped = other_side
          if original == other_original or original == other_flipped \
              or flipped == other_original or flipped == other_flipped:
            has_match = True
            break

      if has_match:
        matches += 1

    print('matches:', matches)
    print()
    print()

    if matches == 2:
      matches_corner.append(tile)

  assert len(matches_corner) == 4
  return multiply(tile.id for tile in matches_corner)


def part_2():
  return None


solve_1 = lambda: part_1()
solve_2 = lambda: part_2()
