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


def count_multiple_slopes(slopes):
  product = 1
  for slope in slopes:
    product *= count_trees(*slope)

  return product


solve_1 = lambda: count_trees(3, 1)
solve_2 = lambda: \
  count_multiple_slopes([
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
  ])
