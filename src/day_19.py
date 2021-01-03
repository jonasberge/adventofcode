from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


input = read_lines(19)

FRULE = '#{}_'
FIRST_RULE = 0


def parse_rules(lines):
  rules = {}

  for line in lines:
    if not line:
      break

    rule, replace = line.split(':')

    involved = re.findall(r'(\d+)', replace)
    involved = [ FRULE.format(r) for r in involved ]

    replace = re.sub(r'(\d+)', FRULE.format(r'\1'), replace)
    replace = re.sub(r'\s|"', '', replace)

    rule = FRULE.format(rule)
    rules[rule] = (replace, involved)

  return rules


def create_regex(rules):
  first = FRULE.format(str(FIRST_RULE))
  result = r"^(" + first + r")$"

  todo = deque()
  todo.append(first)

  while todo:
    current = todo.popleft()
    replace, involved = rules[current]

    result = result.replace(current, '({})'.format(replace))
    for r in involved:
      todo.append(r)

  return re.compile(result)


def count_full_matches():
  it = iter(input)
  rules = parse_rules(it)
  regex = create_regex(rules)
  return sum(bool(regex.match(line)) for line in it)


def part_2():
  return None


solve_1 = lambda: count_full_matches()
solve_2 = lambda: part_2()
