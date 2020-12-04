import re

from lib.input import read_lines


input = read_lines(4)

required = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
optional = set(['cid'])


def is_valid(keys):
  return keys - optional == required


def passports():
  current = {}

  for line in input:
    if not line:
      yield current
      current.clear()

    found = re.findall(r"(\w+):([^\s]+)", line)
    current.update(found)

  if current:
    yield current


def count_valid_keys():
  count = 0

  for passport in passports():
    count += int(is_valid(passport.keys()))

  return count


def solve():
  return (
    count_valid_keys(),
  )
