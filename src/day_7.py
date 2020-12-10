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
  result = defaultdict(dict)

  for this, counts in mapping.items():
    for other in counts.keys():
      result[other][this] = 1

  return result


def count_recursive(bag, inverted_mapping):
  count = 0
  queue = deque([bag])
  visited = set()

  while queue:
    current = queue.popleft()
    if current in visited:
      continue

    visited.add(current)
    other = inverted_mapping[current]

    for x, o in other.items():
      if x not in visited:
        queue.append(x)

  # subtract the shiny gold bag
  return len(visited) - 1


def count_recursive_2(bag, mapping):
  queue = deque([(bag, 1)])
  count = 0

  while queue:
    b1, c1 = queue.popleft()

    other = mapping[b1]
    count += c1

    for b2, c2 in other.items():
      queue.append((b2, c1 * c2))

  return count - 1


solve_1 = lambda: count_recursive('shiny gold', invert_mapping(get_mapping()))
solve_2 = lambda: count_recursive_2('shiny gold', get_mapping())
