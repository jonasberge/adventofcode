from os import path


# read and sanitize input

directory = path.dirname(__file__)
input_file = path.join(directory, '../inputs/day-1.txt')

with open(input_file) as f:
  input = f.readlines()

input = [ int(line.strip()) for line in input ]


def solve(input, goal):
  """ finds two numbers in the input
      that are equal to the goal when summed.
  """

  input = sorted(input)
  current = lambda: input[i] + input[j]

  goal = 2020
  i, j = 0, len(input) - 1

  while current() != goal:
    if current() > goal:
      j -= 1  # subtract something
    else:
      i += 1  # add something

  return input[i], input[j]


goal = 2020
a, b = solve(input, goal)

assert a + b == goal

product = a * b
print(product)
