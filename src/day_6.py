from lib.input import read_lines


input = read_lines(6)


def answers():
  current = set()

  for line in input:
    if not line:
      yield current
      current.clear()

    found = set(line.strip())
    current.update(found)

  if current:
    yield current


def sum_answers():
  return sum(len(answer) for answer in answers())


def solve():
  return (
    sum_answers(),
    0
  )

