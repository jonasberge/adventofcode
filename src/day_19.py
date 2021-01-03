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


def create_regex(rules, start=FIRST_RULE):
  first = FRULE.format(str(start))
  result = "({})".format(first)

  todo = deque()
  todo.append(first)

  while todo:
    current = todo.popleft()
    replace, involved = rules[current]

    result = result.replace(current, '({})'.format(replace))
    for r in involved:
      todo.append(r)

  return re.compile(result)


def count_matches():
  it = iter(input)
  rules = parse_rules(it)
  regex = create_regex(rules)
  regex = re.compile(r"^" + regex.pattern + r"$")
  return sum(bool(regex.match(line)) for line in it)


def try_match_start(regex, string):
  match = regex.match(string)
  if not match:
    return False, string

  _, end = match.span()
  return True, string[end:]


def try_match_end(regex, string):
  match = re.match(r"(.*)" + regex.pattern + r"$", string)
  if not match:
    return False, string

  prefix = match.groups()[0]
  return True, prefix


def match_special(rules, line):
  p42 = create_regex(rules, 42).pattern
  p31 = create_regex(rules, 31).pattern

  r42, r31 = re.compile(p42), re.compile(p31)
  r_start = re.compile(p42 + r"+")

  s = line

  # start matching from the end.
  # count the number of matches of rule #31 at the end,
  # then apply rule #42 as often as that to the end as well.
  # finally match rule #8 at least once from the start.
  # if all attempts matched and the remaining string is empty,
  # then the string matches the modified rules.

  c1 = 0
  while True:
    matched, s = try_match_end(r31, s)
    if matched: c1 += 1
    else: break

  if c1 < 1:
    return False

  for _ in range(c1):
    matched, s = try_match_end(r42, s)
    if not matched:
      return False

  matched, s = try_match_start(r_start, s)
  return matched and len(s) == 0


def count_modified_matches():
  it = iter(input)
  rules = parse_rules(it)
  return sum(match_special(rules, line) for line in it)


solve_1 = lambda: count_matches()
solve_2 = lambda: count_modified_matches()
