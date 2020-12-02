import re

from lib.input import read_lines


input = read_lines(2)


class Rule:
  def __init__(self, letter, min, max):
    self.letter = letter
    self.range = range(min, max + 1)

  def is_valid(self, password):
    return password.count(self.letter) in self.range


def count_valid():
  valid_count = 0

  for line in input:
    match = re.match(r"^(\d+)-(\d+)\s(\w):\s(\w*)$", line)
    lo, hi, letter, password = match.groups()
    lo, hi = int(lo), int(hi)

    rule = Rule(letter, lo, hi)
    if rule.is_valid(password):
      valid_count += 1

  return valid_count


def solve():
  return count_valid()
