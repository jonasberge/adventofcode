from collections import defaultdict

from lib.input import read_lines


input = read_lines(10)
input = [ int(line) for line in input ]
input = sorted(input)

input.insert(0, 0)  # charging outlet
input.append(input[-1] + 3)  # built-in adapter


def differences(accuracy):
  counts = defaultdict(int)

  for i in range(len(input) - 1):
    r, s = input[i:i + 2]
    counts[s - r] += 1

  return counts[1] * counts[3]


def solve():
  return (
    differences([-3, -2, -1]),
    0
  )
