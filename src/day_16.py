from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


input = read_lines(16)

pattern = re.compile(r"^([a-z\s]+):\s([0-9]+)-([0-9]+)\sor\s([0-9]+)-([0-9]+)")


class Rule:
  def __init__(self, name, ranges=[]):
    self.name = name
    self.ranges = ranges

  def __contains__(self, item):
    for range_ in self.ranges:
      if item in range_:
        return True
    return False


class Ticket:
  def __init__(self, values=[]):
    self.values = values

  def __len__(self):
    return len(self.values)


def parse_rules(lines):
  result = []
  for line in lines:
    if not line:
      break

    match = re.match(pattern, line)
    name, a_from, a_to, b_from, b_to = match.groups()
    a_from, a_to = int(a_from), int(a_to)
    b_from, b_to = int(b_from), int(b_to)

    rule = Rule(name, [
      range(a_from, a_to + 1),
      range(b_from, b_to + 1)
    ])

    result.append(rule)

  return result


def parse_ticket(line):
  values = line.split(',')
  values = map(int, values)
  return Ticket(values)


def parse_own_ticket(lines):
  is_own_ticket = False

  for line in lines:
    if is_own_ticket:
      return parse_ticket(line)
    if line == 'your ticket:':
      is_own_ticket = True

  assert False


def parse_nearby_tickets(lines):
  parse_tickets = False
  tickets = []

  for line in lines:
    if parse_tickets:
      ticket = parse_ticket(line)
      tickets.append(ticket)
      continue
    if line == 'nearby tickets:':
      parse_tickets = True

  assert len(tickets)
  return tickets


def part_1():
  lines = iter(input)
  rules = parse_rules(lines)
  _ = parse_own_ticket(lines)
  tickets = parse_nearby_tickets(lines)

  invalid_values_sum = 0

  for ticket in tickets:
    for value in ticket.values:
      valid = False
      for rule in rules:
        if value in rule:
          valid = True
          break
      if not valid:
        invalid_values_sum += value

  return invalid_values_sum

  for rule in rules:
    print(rule.name, rule.ranges)

  for ticket in tickets:
    print(ticket.values)

  return None



def part_2():
  return None


solve_1 = lambda: part_1()
solve_2 = lambda: part_2()
