from collections import defaultdict, deque
from copy import copy, deepcopy
import re
from math import sqrt, prod as multiply

from lib.input import read_lines


input = read_lines(20)

N_CORNER = 2
N_EDGE = 3
N_INNER = 4


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


def count_matching_sides(tile, all_tiles):
  amount = 0

  for other in all_tiles:
    if tile.id == other.id:
      continue

    for side in tile.sides:
      original, flipped = side
      for other_side in other.sides:
        other_original, other_flipped = other_side
        if original == other_original or original == other_flipped \
            or flipped == other_original or flipped == other_flipped:
          amount += 1
          break

  return amount


def grouped_tiles(tiles):
  matches = defaultdict(list)

  for tile in tiles:
    num_matches = count_matching_sides(tile, tiles)
    matches[num_matches].append(tile)

  return matches


# after solving part one you can see that there are
# - exactly 100 tiles matching 4 sides
# - exactly 40 tiles matching 3 sides and
# - exactly 4 tiles matching 2 sides
#
# this means that we can put tiles into the three groups
# named above without overlapping or ambiguity.

def multiply_corner_tile_ids():
  tiles = list(parse_tiles(input))
  grouped = grouped_tiles(tiles)

  assert len(grouped[N_CORNER]) == 4
  return multiply(tile.id for tile in grouped[N_CORNER])


# unfortunately we can't get away with not assembling the image.
# so let's do that..

def count_sea_monsters():
  tiles = list(parse_tiles(input))
  grouped = grouped_tiles(tiles)

  amount = len(tiles)
  side_length = int(sqrt(amount))

  n_corner = N_CORNER
  n_edge = 4 * (side_length - 2)
  n_inner = amount - n_corner - n_edge

  #

  return None


solve_1 = lambda: multiply_corner_tile_ids()
solve_2 = lambda: count_sea_monsters()
