from os import path


INPUTS_DIR = path.abspath(path.join(path.dirname(__file__), '../inputs'))


def file_for_day(day):
  return path.join(INPUTS_DIR, 'day-{}.txt'.format(day))


def read_lines(day):
  with open(file_for_day(day)) as file:
    return [ line.strip() for line in file.readlines() ]


def blocks(lines):
  block = []

  for line in lines:
    if not line:
      yield block
      block.clear()
      continue

    block.append(line)

  if block:
    yield block
