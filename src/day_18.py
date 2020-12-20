from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


input = read_lines(18)


def evaluate_simple(line):
  stack = deque()
  n, op = None, None

  for char in line:
    if char == '(':
      stack.append((n, op))
      n, op = None, None
      continue

    if char == ')':
      m, op_ = stack.pop()
      if n and m and op_:
        n = op_(m, n)
      continue

    if char.isdigit():
      m = int(char)
      if n and op:
        n = op(n, m)
      else:
        n = m
      continue

    if char == '+':
      op = lambda a, b: a + b
      continue

    if char == '*':
      op = lambda a, b: a * b
      continue

  return n


def part_2():
  return None


solve_1 = lambda: sum([evaluate_simple(line) for line in input])
solve_2 = lambda: part_2()
