from collections import defaultdict, deque
import re

from lib.input import read_lines


input = read_lines(7)

regex = re.compile(
  r'^(?:([a-z\s]+)\sbags\scontain\s)'
  r'|(?:(\d+)\s([a-z\s]+)\sbags?)(?:,\s*|.$)'
)


def get_mapping():
  result = {}

  for line in input:
    match = re.findall(regex, line)

    which = match.pop(0)[0]
    current = result[which] = {}

    for item in match:
      count, item = item[1:]
      current[item] = int(count)

  return result


def invert_mapping(mapping):
  result = defaultdict(set)

  for this, counts in mapping.items():
    for other in counts.keys():
      result[other].add(this)

  return result


def count_recursive(bag, inverted_mapping):
  count = 0
  queue = deque([bag])
  visited = set()

  while queue:
    current = queue.pop()
    if current in visited:
      continue

    visited.add(current)
    other = inverted_mapping[current]
    queue.extend(other - visited)

  # subtract the shiny gold bag
  return len(visited) - 1


def solve():
  return (
    count_recursive('shiny gold', invert_mapping(get_mapping())),
    0
  )
