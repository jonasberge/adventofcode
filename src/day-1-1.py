from os import path


# read and sanitize input

directory = path.dirname(__file__)
input_file = path.join(directory, '../inputs/day-1.txt')

with open(input_file) as f:
  input = f.readlines()

input = [ int(line.strip()) for line in input ]


# solve

input = sorted(input)
current = lambda: input[i] + input[j]

goal = 2020
i, j = 0, len(input) - 1


while current() != goal:

  if current() > goal:  # subtract something, make j smaller
    j -= 1
  else:  # add something, make i greater
    i += 1


print(i, j)
print(input[i], input[j])
print('sum = {}'.format(current()))

output = input[i] * input[j]
print('product = {}'.format(output))
