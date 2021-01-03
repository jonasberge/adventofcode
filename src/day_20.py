from collections import defaultdict, deque
from copy import copy, deepcopy
import re
from math import inf, sqrt, prod as multiply
from enum import Enum
import itertools

from lib.input import read_lines


input = read_lines(20)

seamonster_patterns = [
  # https://stackoverflow.com/a/5616910
  r"(?=..................#.)",
  r"(?=#....##....##....###)",
  r"(?=.#..#..#..#..#..#...)"
]


# 1. inner tiles will match = all four sides
# 2. edge (but not corner) tiles will match >= three of their sides
# 3. corner tiles will match >= two of their sides with other tiles


class Orientation(Enum):
  VERTICAL = 0
  HORIZONTAL = 1

class Direction(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

  @property
  def x_offset(self):
    if self == self.LEFT: return -1
    if self == self.RIGHT: return 1
    return 0

  @property
  def y_offset(self):
    if self == self.TOP: return -1
    if self == self.BOTTOM: return 1
    return 0

  def get_orientation(self):
    if self == self.TOP or self == self.BOTTOM:
      return Orientation.VERTICAL

    if self == self.RIGHT or self == self.LEFT:
      return Orientation.HORIZONTAL

    raise Exception

  def get_rotation_angle(self, other):
    x = (2 + self.value - other.value) % 4
    return x * 90


class Side:
  def __init__(self, direction, value):
    self.direction = direction
    self.value = value
    self.flipped = ''.join(reversed(value))

  def fixed_for_rotation(self, direction_of_origin):
    """ the side's value modified for comparing
        two sides in a rotation context.

        BOTTOM -> reverse BOTTOM or LEFT
        LEFT   -> reverse BOTTOM or LEFT
        TOP    -> reverse TOP    or RIGHT
        RIGHT  -> reverse TOP    or RIGHT
    """

    do_fix = False

    if direction_of_origin in (Direction.BOTTOM, Direction.LEFT):
      if self.direction in (Direction.BOTTOM, Direction.LEFT):
        do_fix = True

    if direction_of_origin in (Direction.TOP, Direction.RIGHT):
      if self.direction in (Direction.TOP, Direction.RIGHT):
        do_fix = True

    if do_fix:
      return Side(self.direction, self.flipped)

    return self


class Transform:
  def __init__(self, flip_orientation, rotation_angle):
    self.flip_orientation = flip_orientation
    self.rotation_angle = rotation_angle

  def __repr__(self):
    return '{}({}, {})'.format(
      self.__class__.__name__,
      self.flip_orientation.name if self.flip_orientation else None,
      self.rotation_angle
    )


class Match:
  def __init__(self, direction, transform):
    self.direction = direction
    self.transform = transform


def rotate_str_list(original):
  return [''.join(row) for row in zip(*original[::-1])]

def rotate_str_list_angle(original, angle):
  step, full = 90, 360
  if not angle % step == 0:
    raise ValueError
  angle = angle % full
  while angle > 0:
    original = rotate_str_list(original)
    angle -= step
  return original

def flip_str_list_vertical_axis(original):
  return list(''.join(reversed(row)) for row in original)

def flip_str_list_horizontal_axis(original):
  return original[::-1]


class Tile:
  def __init__(self, id, data):
    self.id = id
    self.data = data
    self.sides = self._compute_sides()

  def _compute_sides(self):
    return [
      Side(Direction.TOP, self.data[0]),
      Side(Direction.BOTTOM, self.data[-1]),
      Side(Direction.LEFT, ''.join(l[0] for l in self.data)),
      Side(Direction.RIGHT, ''.join(l[-1] for l in self.data))
    ]

  def get_matching_side(self, other_tile):

    for side in self.sides:
      for other_side in other_tile.sides:

        other_side = other_side.fixed_for_rotation(side.direction)
        angle = side.direction.get_rotation_angle(other_side.direction)

        if side.value == other_side.value:
          return Match(side.direction, Transform(None, angle))

        if side.value == other_side.flipped:
          orientation = other_side.direction.get_orientation()
          return Match(side.direction, Transform(orientation, angle))

    return None

  def transform_by(self, transform):
    data = self.data
    if transform.flip_orientation == Orientation.VERTICAL:
      data = flip_str_list_vertical_axis(data)
    elif transform.flip_orientation == Orientation.HORIZONTAL:
      data = flip_str_list_horizontal_axis(data)
    data = rotate_str_list_angle(data, transform.rotation_angle)
    return Tile(self.id, data)

  def without_sides(self):
    return Tile(self.id, [
      row[1:-1]  # remove first and last columns
      for row in self.data[1:-1]  # remove first and last row
    ])


class Step:
  def __init__(self, tile, x, y):
    self.tile = tile
    self.x = x
    self.y = y


def arrange_image(tiles):
  origin = tiles[0]
  initial = Step(origin, 0, 0)

  steps = deque()
  steps.append(initial)
  visited = set([ origin.id ])

  matrix = {}
  matrix[0, 0] = origin

  while steps:
    step = steps.popleft()
    x, y = step.x, step.y

    for other_tile in tiles:
      if other_tile.id in visited:
        continue

      match = step.tile.get_matching_side(other_tile)
      if not match:
        continue

      transformed_tile = other_tile.transform_by(match.transform)
      dx, dy = match.direction.x_offset, match.direction.y_offset

      nx, ny = x + dx, y + dy
      assert (nx, ny) not in matrix

      matrix[nx, ny] = transformed_tile
      next_step = Step(transformed_tile, nx, ny)

      steps.append(next_step)
      visited.add(other_tile.id)

  min_x, min_y = inf, inf
  max_x, max_y = -inf, -inf

  for pos, tile in matrix.items():
    min_x = min(min_x, pos[0])
    max_x = max(max_x, pos[0])
    min_y = min(min_y, pos[1])
    max_y = max(max_y, pos[1])

  x_len = max_x - min_x + 1
  y_len = max_y - min_y + 1

  assert x_len == y_len
  assert x_len * y_len == len(matrix)

  result = {}
  for position, tile in matrix.items():
    x, y = position
    result[x - min_x, y - min_y] = tile

  return result


def combine_tiled_image(tiled_image):
  tiled_image = {
    pos: tile.without_sides()
    for pos, tile in tiled_image.items()
  }

  tile_length = len(tiled_image[0, 0].data)
  num_tiles = int(sqrt(len(tiled_image)))
  image_length = tile_length * num_tiles

  image_matrix = {}

  for pos, tile in tiled_image.items():
    x, y = pos[0] * tile_length, pos[1] * tile_length
    for dy, row in enumerate(tile.data):
      for dx, char in enumerate(row):
        image_matrix[x + dx, y + dy] = char

  image = []

  for x in range(image_length):
    current = ''
    for y in range(image_length):
      current = current + image_matrix[x, y]
    image.append(current)

  return image


def parse_tile(it):
  match = re.match(r"^Tile (\d+):$", next(it))

  data = []
  for line in it:
    if not line:
      break
    data.append(line)

  return Tile(int(match.groups()[0]), data)

def parse_tiles():
  it = iter(input)
  while True:
    try:
      yield parse_tile(it)
    except StopIteration:
      return

def parse_tiled_image():
  tiles = list(parse_tiles())
  return arrange_image(tiles)

def parse_image():
  tiled_image = parse_tiled_image()
  return combine_tiled_image(tiled_image)


def print_tile(tile):
  print('ID:', tile.id)
  print('\n'.join(tile.data))
  print()


def multiply_corner_tile_ids():
  tiled_image = parse_tiled_image()
  high = sqrt(len(tiled_image)) - 1

  return multiply([
    tiled_image[0, 0].id,
    tiled_image[0, high].id,
    tiled_image[high, 0].id,
    tiled_image[high, high].id
  ])



"""
                    #
  #    ##    ##    ###
   #  #  #  #  #  #

"""
def count_sea_monsters(image):
  patterns = seamonster_patterns
  matches = []
  amount = 0

  for i in range(len(image)):

    old_matches, matches = matches, []
    for p, start in old_matches:
      if p + 1 == len(patterns):
        amount += 1
        continue

      for m in re.finditer(patterns[p + 1], image[i]):
        # print(p + 1, m.start(), '[{}]'.format(start))
        if m.start() == start:
          matches.append((p + 1, start))

    for m in re.finditer(patterns[0], image[i]):
      # print('->', patterns[0], image[i], m.start())
      matches.append((0, m.start()))

  return amount


def all_image_rotations(image):
  return [
    rotate_str_list_angle(image, 90 * 0),
    rotate_str_list_angle(image, 90 * 1),
    rotate_str_list_angle(image, 90 * 2),
    rotate_str_list_angle(image, 90 * 3),
  ]

def all_image_transformations(image):
  return itertools.chain.from_iterable([
    all_image_rotations(image),
    all_image_rotations(flip_str_list_horizontal_axis(image)),
    all_image_rotations(flip_str_list_vertical_axis(image))
  ])


def part_2():
  image = parse_image()

  max_amount = 0
  for transformed in all_image_transformations(image):
    amount = count_sea_monsters(transformed)
    max_amount = max(max_amount, amount)

  total_hashes = sum(line.count('#') for line in image)
  seamonster_hashes = sum(p.count('#') for p in seamonster_patterns)

  return total_hashes - seamonster_hashes * max_amount


solve_1 = lambda: multiply_corner_tile_ids()
solve_2 = lambda: part_2()
