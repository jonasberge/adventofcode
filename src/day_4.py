import re

from lib.input import read_lines


input = read_lines(4)

required = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
optional = set(['cid'])


def is_valid(keys):
  return keys - optional == required


def count_valid():
  if input[-1:]:
    input.append('')

  keys = set()
  count = 0

  for line in input:
    if not line:
      count += int(is_valid(keys))
      keys = set()
      continue

    found = re.findall(r"(\w+):[^\s]+", line)
    keys.update(found)

  return count


def solve():
  return (
    count_valid(),
  )
