from collections import defaultdict, deque
from copy import copy, deepcopy
import re
from math import sqrt, prod as multiply

from lib.input import read_lines


input_ = read_lines(20)

N_CORNER = 2
N_EDGE = 3
N_INNER = 4

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

VERTICAL = 4
HORIZONTAL = 5


def get_x_offset(direction):
  if direction == LEFT: return -1
  if direction == RIGHT: return 1
  return 0

def get_y_offset(direction):
  if direction == BOTTOM: return -1
  if direction == TOP: return 1
  return 0

def get_orientation(direction):
  if direction == TOP or direction == BOTTOM: return VERTICAL
  if direction == RIGHT or direction == LEFT: return HORIZONTAL
  raise Exception


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
      (direction, side, ''.join(reversed(side)))
      for direction, side in [
        (TOP, self.data[0]),
        (BOTTOM, ''.join(self.data[-1])),
        (LEFT, ''.join(l[0] for l in self.data)),
        (RIGHT, ''.join(l[-1] for l in self.data))
      ]
    ]

  def count_matching_sides(self, other, /, break_at=None):
    amount = 0

    for side in self.sides:
      direction, original, flipped = side

      for other_side in other.sides:
        other_direction, other_original, other_flipped = other_side

        if original == other_original or original == other_flipped \
            or flipped == other_original or flipped == other_flipped:
          amount += 1
          if break_at and amount == break_at:
            break

    return amount

  def has_matching_sides(self, other):
    return 1 == self.count_matching_sides(other, break_at=1)

  def match_sides(self, other):
    # first option: self original, other original
    for side in self.sides:
      direction, original, flipped = side
      orientation = get_orientation(direction)

      for other_side in other.sides:
        other_direction, other_original, other_flipped = other_side
        other_original, other_flipped = \
          fix_for_rotation(other_original, other_flipped, \
            direction, other_direction)

        if original == other_original:
          angle = get_rotation_angle(direction, other_direction)
          return TileMatch(other, direction, None, angle)

    # second option: self original, other flipped
    for side in self.sides:
      direction, original, _ = side
      orientation = get_orientation(direction)

      for other_side in other.sides:
        other_direction, other_original, other_flipped = other_side
        other_original, other_flipped = \
          fix_for_rotation(other_original, other_flipped, \
            direction, other_direction)

        flip_orientation = get_orientation(other_direction)
        if original == other_flipped:
          angle = get_rotation_angle(direction, other_direction)
          return TileMatch(other, direction, flip_orientation, angle)

    raise Exception('no matches')


def get_rotation_angle(direct, other_dir):
  x = (2 + direct - other_dir) % 4
  return x * 90

def fix_for_rotation(side, other, direction, other_direction):
  # bottom -> reverse bottom or left
  # left   -> reverse bottom or left
  # top    -> reverse top    or right
  # right  -> reverse top    or right

  if direction in (BOTTOM, LEFT):
    if other_direction in (BOTTOM, LEFT):
      side, other = other, side

  if direction in (TOP, RIGHT):
    if other_direction in (TOP, RIGHT):
      side, other = other, side

  return side, other


class TileMatch:
  def __init__(self, tile, direction, flip_orientation, rotation_angle):
    self.tile = tile
    self.direction = direction
    self.flip_orientation = flip_orientation
    self.rotation_angle = rotation_angle


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


def print_tile(tile):
  print('ID:', tile.id)
  print('\n'.join(tile.data))
  print()


# after solving part one you can see that there are
# - exactly 100 tiles matching 4 sides
# - exactly 40 tiles matching 3 sides and
# - exactly 4 tiles matching 2 sides
#
# this means that we can put tiles into the three groups
# named above without overlapping or ambiguity.

def multiply_corner_tile_ids():
  tiles = list(parse_tiles(input_))
  matched = get_matched_tiles(tiles)

  assert len(matched[N_CORNER]) == 4
  return multiply(tile.id for tile, _ in matched[N_CORNER])


solve_1 = lambda: multiply_corner_tile_ids()
solve_2 = lambda: count_sea_monsters()



"""


def get_matched_tiles(tiles):
  matches = defaultdict(list)

  for tile in tiles:
    tile_matches = []

    amount = 0
    for other in tiles:
      if tile.id == other.id: continue
      if tile.has_matching_sides(other):
        amount += 1
        tile_match = tile.match_sides(other)
        tile_matches.append(tile_match)

    matches[amount].append((tile, tile_matches))

  return matches


class Step:
  def __init__(self, tile, x, y):
    self.tile = tile
    self.x = x
    self.y = y


def assemble_tiles(tiles, matched):

  # n_corner = N_CORNER
  # n_edge = 4 * (side_length - 2)
  # n_inner = amount - n_corner - n_edge
  # edges = matched[N_EDGE]
  # inner = matched[N_INNER]


  # print({
  #   n: len(matches)
  #   for n, matches in matched.items()
  # })

  # matches_for_tile = {}
  # for amount, matches in matched.items():
  #   for tile, tile_matches in matches:
  #     matches_for_tile[tile.id] = tile_matches

  # d = { id_: len(x) for id_, x in matches_for_tile.items() }
  # print(len(list(filter(lambda x: x[1] == 2, d.items()))))
  # exit()

  tiles_by_id = {}
  for tile in tiles:
    tiles_by_id[tile.id] = tile

  amount = len(tiles)
  side_length = int(sqrt(amount))

  corners = matched[N_CORNER]
  origin, _ = corners[3]
  initial = Step(origin, 0, 0)

  steps = deque()
  steps.append(initial)
  visited = set([ origin.id ])

  matrix = {}
  matrix[0,0] = origin

  c, m = 0, 5

  while steps:
    current = steps.popleft()
    tile = current.tile
    x, y = current.x, current.y

    for match in matches_for_tile[tile.id]:
      direction = match.direction
      if match.tile.id not in visited:
        x_off, y_off = get_x_offset(direction), get_y_offset(direction)
        nx, ny = x + x_off, y + y_off
        matrix[nx,ny] = match.tile
        steps.append(Step(match.tile, nx, ny))
        visited.add(match.tile.id)

    # if c == m: break
    # c += 1

  min_x, min_y = 100000000, 100000000
  max_x, max_y = -10000000, -10000000

  for pos, tile in matrix.items():
    print(pos, tile.id)

    min_x = min(min_x, pos[0])
    max_x = max(max_x, pos[0])

    min_y = min(min_y, pos[1])
    max_y = max(max_y, pos[1])

  print()
  print((min_x, min_y), (max_x, max_y))
  print()

  x_len = max_x - min_x + 1
  y_len = max_y - min_y + 1

  print(x_len, y_len)
  print('#items:', len(matrix))

  # print_tile(first_tile)

  # for tile, matches in corners:

  # id_ = 1427
  # tile = next(filter(lambda t: t.id == id_, tiles))
  # matches = matches_for_tile[id_]

  # # for tile, matches in corners:
  # print_tile(tile)
  # print('MATCHES:')
  # print(list(m.tile.id for m in matches_for_tile[tile.id]))
  # print()
  # for match in matches:
  #   print(match.direction, match.flip_orientation, match.rotation_angle)
  #   print_tile(match.tile)
  # print()
  # print()

  # matrix = [[None] * side_length for _ in range(side_length)]

  # origin = corners[0]
  # matrix[0][0] = origin

  pass


# unfortunately we can't get away with not assembling the image.
# so let's do that..
#
# actually! we could brute force this as such:
# sum all #-characters. then try all possibilities
# where you subtract n*X, where n is anything > 0
# and X is the number #-characters in a sea monster.
#
# but - let's refrain from doing so.

# generally speaking: it's possible - if not likely - that
# certain tile edges match some other tile's edge, while in
# the resulting image those tiles are not neighbours.
#
# a general solution that copes with this is harder to program
# but currently it just looks like this won't happen, as the
# first part had exactly 100, 40 and 4 tiles in each group.
#
# so let's choose to simplify here and make
# the algorithm a little more naive.

def count_sea_monsters():
  tiles = list(parse_tiles(input_))
  matched = get_matched_tiles(tiles)
  matrix = assemble_tiles(tiles, matched)

  return None

"""
