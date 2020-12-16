from math import prod
from itertools import chain
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

  def __repr__(self):
    return self.name


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
  values = list(map(int, values))
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


def parse_input():
  lines = iter(input)
  rules = parse_rules(lines)
  own_ticket = parse_own_ticket(lines)
  nearby_tickets = parse_nearby_tickets(lines)

  for ticket in chain([own_ticket], nearby_tickets):
    assert len(ticket) == len(rules)

  return rules, own_ticket, nearby_tickets


def split_valid_tickets(tickets, rules):
  valid_tickets = []
  invalid_values = []

  for ticket in tickets:
    all_valid = True
    for value in ticket.values:
      valid = False
      for rule in rules:
        if value in rule:
          valid = True
          break
      if not valid:
        invalid_values.append(value)
        all_valid = False
        break

    if all_valid:
      valid_tickets.append(ticket)

  return valid_tickets, invalid_values


def valid_tickets(tickets, rules):
  return split_valid_tickets(tickets, rules)[0]

def invalid_tickets(tickets, rules):
  return split_valid_tickets(tickets, rules)[1]


def sum_invalid():
  rules, own_ticket, nearby_tickets = parse_input()
  return sum(invalid_tickets(nearby_tickets, rules))


def own_ticket_values(predicate=lambda r: True):
  rules, own_ticket, nearby_tickets = parse_input()
  other_tickets = valid_tickets(nearby_tickets, rules)

  rule_candidates = [set() for _ in range(len(rules))]

  for k, ticket in enumerate(other_tickets):
    for i, value in enumerate(ticket.values):

      valid_rules = set()
      for j, rule in enumerate(rules):
        if value in rule:
          valid_rules.add(j)

      if k == 0:
        rule_candidates[i] |= valid_rules
      else:
        rule_candidates[i] &= valid_rules

  rule_candidates = sorted(enumerate(rule_candidates), key=lambda x: len(x[1]))
  used_rules = set()

  column_for_rule = [None for _ in range(len(rules))]

  for index, candidates in rule_candidates:
    selected = candidates - used_rules
    assert len(selected) == 1
    used_rules |= selected

    selected = list(selected)[0]
    column_for_rule[selected] = index

  values = []

  for index, rule in enumerate(rules):
    if not predicate(rule):
      continue

    column = column_for_rule[index]
    values.append(own_ticket.values[column])

  return values


solve_1 = lambda: sum_invalid()
solve_2 = lambda: prod(own_ticket_values(lambda r: r.name.startswith('departure')))
