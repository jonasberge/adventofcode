from math import prod as multiply

from lib.input import read_lines


input = read_lines(1)
input = [ int(line) for line in input ]
input = sorted(input)

goal = 2020


def sum_two():
  """ finds two numbers in the input
      that are equal to the goal when summed.
  """

  current = lambda: input[i] + input[j]

  goal = 2020
  i, j = 0, len(input) - 1

  while current() != goal:
    if current() > goal:
      j -= 1  # subtract something
    else:
      i += 1  # add something

  return input[i], input[j]


def solve():
  return multiply(sum_two())
