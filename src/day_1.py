from math import prod as multiply

from lib.input import read_lines


input = [ int(line.strip()) for line in read_lines(1) ]
goal = 2020


def sum_two():
  """ finds two numbers in the input
      that are equal to the goal when summed.
  """

  sorted_input = sorted(input)
  current = lambda: sorted_input[i] + sorted_input[j]

  goal = 2020
  i, j = 0, len(input) - 1

  while current() != goal:
    if current() > goal:
      j -= 1  # subtract something
    else:
      i += 1  # add something

  return sorted_input[i], sorted_input[j]


def solve():
  return multiply(sum_two())
