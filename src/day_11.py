from copy import deepcopy

from lib.input import read_lines


OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'

input = read_lines(11)
input = [list(row) for row in input]


class State:
  def __init__(self, matrix, empty_treshold, neighbours):
    self.matrix = deepcopy(matrix)
    self.empty_treshold = empty_treshold
    self.neighbours = neighbours

  def rows(self): return len(self.matrix)
  def cols(self): return len(self.matrix[0])

  def count_occupied(self):
    return sum(
      value == OCCUPIED
      for row in self.matrix
      for value in row
    )

  def step(self):
    occupied = [
      [0 for _ in range(self.cols() + 2)]
      for _ in range(self.rows() + 2)
    ]

    for i, row in enumerate(self.matrix):
      for j, state in enumerate(row):
        if state == OCCUPIED:
          for u, v in self.neighbours(i, j, self):
            occupied[u + 1][v + 1] += 1

    changed = 0

    for i in range(self.rows()):
      for j in range(self.cols()):
        old = self.matrix[i][j]
        if old == FLOOR:
          continue

        amount = occupied[i + 1][j + 1]
        if amount == 0: new = OCCUPIED
        elif amount >= self.empty_treshold: new = EMPTY
        else: continue

        self.matrix[i][j] = new
        changed += old != new

    return changed


def adjacent(i, j, state):
  for u in range(i - 1, i + 2):
    for v in range(j - 1, j + 2):
      if (u, v) == (i, j):
        continue
      yield (u, v)


def visible(i, j, state):
  """ x = min(i, j)
      y = min(rows - i, cols - j)

      diagonals:
      (0, j) -> (rows - 1, j)
      (i, 0) -> (i, cols - 1)
      (i - x, j - x) -> (i + y, j + y)
      (i + x, j - x) -> (i - y, j + y)
  """

  rows = state.rows()
  cols = state.cols()

  is_empty = lambda m, n: state.matrix[m][n] != FLOOR

  # north
  for u in reversed(range(i)):
    if is_empty(u, j):
      yield u, j
      break

  # east
  for v in range(j + 1, cols):
    if is_empty(i, v):
      yield i, v
      break

  # south
  for u in range(i + 1, rows):
    if is_empty(u, j):
      yield u, j
      break

  # west
  for v in reversed(range(j)):
    if is_empty(i, v):
      yield i, v
      break

  # north-east
  for d in range(1, min(i + 1, cols - j)):
    u, v = i - d, j + d
    if is_empty(u, v):
      yield u, v
      break

  # south-east
  for d in range(1, min(rows - i, cols - j)):
    u, v = i + d, j + d
    if is_empty(u, v):
      yield u, v
      break

  # south-west
  for d in range(1, min(rows - i, j + 1)):
    u, v = i + d, j - d
    if is_empty(u, v):
      yield u, v
      break

  # north-west
  for d in range(1, min(i + 1, j + 1)):
    u, v = i - d, j - d
    if is_empty(u, v):
      yield u, v
      break


def occupied_after_stable(state):
  changed = None
  while changed != 0:
    changed = state.step()

  return state.count_occupied()


solve_1 = lambda: occupied_after_stable(State(input, 4, neighbours=adjacent))
solve_2 = lambda: occupied_after_stable(State(input, 5, neighbours=visible))
