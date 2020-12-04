import re

from lib.describe import Is, All, Any, between, equal, match, in_
from lib.input import read_lines
from lib.util import irange


input = read_lines(4)

required = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
optional = set(['cid'])

structure = {
  'byr': Is(int, between(1920, 2002)),
  'iyr': Is(int, between(2010, 2020)),
  'eyr': Is(int, between(2020, 2030)),
  'hgt': Any([
    All([
      Is(lambda s: s[-2:], equal('cm')),
      Is(lambda s: s[:-2], int, between(150, 193))
    ]),
    All([
      Is(lambda s: s[-2:], equal('in')),
      Is(lambda s: s[:-2], int, between(59, 76))
    ])
  ]),
  'hcl': All([
    Is(len, equal(7)),
    Is(lambda s: s[:1], equal('#')),
    Is(lambda s: s[1:], match(r'^[0-9a-f]*$'))
  ]),
  'ecl': Is(in_(set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']))),
  'pid': All([
    Is(len, equal(9)),
    Is(match(r'^[0-9]*$'))
  ]),
  'cid': lambda s: True
}


def is_valid_fields(fields):
  return fields - optional == required


def is_valid_passport(passport):
  if not is_valid_fields(passport.keys()):
    return False

  for field in passport.keys():
    validator = structure[field]
    if not validator(passport[field]):
      return False

  return True


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


def solve():
  return (
    sum(int(is_valid_fields(p.keys())) for p in passports()),
    sum(int(is_valid_passport(p)) for p in passports())
  )
