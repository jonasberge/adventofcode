import re

from lib.input import read_lines
from lib.util import irange


input = read_lines(4)

required = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
optional = set(['cid'])

eye_colors = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])


def is_valid_keys(keys):
  return keys - optional == required


def is_valid_passport(passport):
  if not is_valid_keys(passport.keys()):
    return False

  if not int(passport['byr']) in irange(1920, 2002): return False
  if not int(passport['iyr']) in irange(2010, 2020): return False
  if not int(passport['eyr']) in irange(2020, 2030): return False

  hgt = passport['hgt']
  if len(hgt) < 3: return False
  if hgt.endswith('cm'):
    if not int(hgt[:-2]) in irange(150, 193): return False
  elif hgt.endswith('in'):
    if not int(hgt[:-2]) in irange(59, 76): return False
  else: return False

  hcl = passport['hcl']
  if len(hcl) != 7: return False
  if not hcl.startswith('#'): return False
  elif set(hcl[1:]) - set('0123456789abcdef'): return False

  if not passport['ecl'] in eye_colors: return False

  pid = passport['pid']
  if len(pid) != 9: return False
  if set(pid) - set('0123456789'): return False

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
    sum(int(is_valid_keys(p.keys())) for p in passports()),
    sum(int(is_valid_passport(p)) for p in passports())
  )
