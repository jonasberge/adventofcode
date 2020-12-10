from os import path
import sys


ROOT_PATH = path.abspath(path.join(path.dirname(__file__), '..'))

INPUTS_DIR = 'inputs'
INPUTS_PATH = path.join(ROOT_PATH, INPUTS_DIR)


def file_for_day(day):
  return path.join(INPUTS_PATH, 'day-{}.txt'.format(day))


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
