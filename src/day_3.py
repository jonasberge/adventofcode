from lib.input import read_lines


X, Y = 0, 1


input = read_lines(3)
width, height = len(input[0]), len(input)


def is_tree(x, y):
  return input[y][x] == '#'


def count_trees(right, down):
  trees = 0
  position = [0, 0]

  while position[Y] < height:
    trees += int(is_tree(*position))
    position[X] += right
    position[Y] += down

    # forest repeat's to the right
    position[X] %= width

  return trees


def solve():
  return (
    count_trees(3, 1)
  )
