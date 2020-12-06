from lib.input import read_lines, blocks


input = read_lines(6)


def answered():
  for block in blocks(input):
    answers = set()
    for line in block:
      answers.update(line)
    yield answers


def answered_by_all():
  for block in blocks(input):
    answers = [set(line) for line in block]
    intersection = set.intersection(*answers)
    yield intersection


def sum_len(collection):
  return sum(len(e) for e in collection)


def solve():
  return (
    sum_len(answered()),
    sum_len(answered_by_all())
  )
