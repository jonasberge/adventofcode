from math import prod as multiply

from lib.input import read_lines


input = read_lines(1)
input = [ int(line) for line in input ]
input = sorted(input)


def sum_two(goal):
  """ finds two numbers in the input
      that are equal to the goal when summed.
  """

  i, j = 0, len(input) - 1

  while True:
    current = input[i] + input[j]

    if current > goal:
      j -= 1  # subtract something
    elif current < goal:
      i += 1  # add something
    else: break

    if j < 0 or i >= len(input):
      raise Exception()

  return input[i], input[j]


def sum_three(goal):
  """ finds three numbers in the input
      that are equal to the goal when summed.
  """

  for number in input:
    sub_goal = goal - number
    try: a, b = sum_two(sub_goal)
    except: continue
    return number, a, b

  raise Exception()


def solve():
  goal = 2020
  return (
    multiply(sum_two(goal)),
    multiply(sum_three(goal))
  )
