import re


class Is:
  def __init__(self, *funcs):
    self._funcs = funcs

  def __call__(self, value):
    for func in self._funcs:
      value = func(value)
    return bool(value)


class _Base:
  def __init__(self, funcs):
    self._funcs = funcs


class All(_Base):
  def __call__(self, value):
    for func in self._funcs:
      if not func(value):
        return False
    return True


class Any(_Base):
  def __call__(self, value):
    for func in self._funcs:
      if func(value):
        return True
    return False


def between(lo, hi):
  def func(value):
    return value in range(lo, hi + 1)
  return func


def equal(other):
  def func(value):
    return value == other
  return func


def match(regex):
  pattern = re.compile(regex)
  def func(value):
    return bool(pattern.match(value))
  return func


def in_(collection):
  def func(value):
    return value in collection
  return func
