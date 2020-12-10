from functools import wraps

import pytest


def use_example(example):
  def decorator(f):
    # note: the order of the decorators matter.
    # wraps() needs to come last, otherwise it wouldn't be
    # possible to put any other decorators after @use_example().
    @pytest.mark.parametrize('problem', \
      [(True, example)], indirect=['problem'], ids=lambda p: p[1])
    @wraps(f)
    def wrapper(*args, **kwargs):
      return f(*args, **kwargs)
    return wrapper

  return decorator


skip = pytest.mark.skip
