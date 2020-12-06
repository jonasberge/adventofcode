from lib.input import read_lines


input = read_lines(6)


def answered():
  current = set()

  for line in input:
    if not line:
      yield current
      current.clear()
      continue

    found = set(line.strip())
    current.update(found)

  if current:
    yield current


def answered_by_all():
  intersection = set()
  is_first = True

  for line in input:
    if not line:
      yield intersection
      intersection.clear()
      is_first = True
      continue

    found = set(line.strip())

    if is_first:
      intersection = found
      is_first = False
    else:
      intersection &= found

  if intersection:
    yield intersection


def sum_len(collection):
  return sum(len(e) for e in collection)


def solve():
  return (
    sum_len(answered()),
    sum_len(answered_by_all())
  )

