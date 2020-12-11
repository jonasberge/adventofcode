from collections import deque

from lib.input import read_lines


OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'

input = read_lines(11)
input = [list(row) for row in input]


class State:
  def __init__(self, matrix):
    self.matrix = matrix

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
          for u in range(i - 1, i + 2):
            for v in range(j - 1, j + 2):
              if (u, v) == (i, j):
                continue

              occupied[u + 1][v + 1] += 1

    changed = 0

    for i in range(self.rows()):
      for j in range(self.cols()):
        old = self.matrix[i][j]
        if old == FLOOR:
          continue

        amount = occupied[i + 1][j + 1]
        if amount == 0: new = OCCUPIED
        elif amount >= 4: new = EMPTY
        else: continue

        self.matrix[i][j] = new
        changed += old != new

    return changed


def occupied_after_stable():
  state = State(input)
  changed = None

  while changed != 0:
    changed = state.step()

  return state.count_occupied()


def part_2():
  return None


solve_1 = lambda: occupied_after_stable()
solve_2 = lambda: part_2()
