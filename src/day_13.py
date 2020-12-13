from math import prod

from lib.input import read_lines


input = read_lines(13)


def times():
  values = input[1].split(',')
  for index, time in enumerate(values):
    if time == 'x':
      continue
    yield index, int(time)


def earliest_departure():
  earliest = int(input[0])
  departure = earliest * 2  # something big
  bus_id = None

  for _, time in times():
    first = (earliest // time) * time
    if first < earliest:
      first += time

    if first < departure:
      departure = first
      bus_id = time

  return bus_id * (departure - earliest)


#
# "Jah."
#   - Fotios Giannakopoulos
#
class ChineseRemainder:
  # assumes all m's are coprime.
  # ... which they conveniently are!
  # (because they are all primes)
  def __init__(self, mjs, bjs):
    self.mjs = mjs
    self.bjs = bjs
    self.m = prod(mjs)

  def solve(self):
    x = 0

    for i in range(len(self.mjs)):
      bj = self.bjs[i]
      mj = self.mjs[i]
      sj = self.m // mj
      kj = False

      # sj * kj ≡ 1 (mod mj)
      for candidate in range(mj):
        if sj * candidate % mj == 1:
          kj = candidate

      x += kj * sj * bj

    x0 = x % self.m
    return x0


def match_departure_times():
  mjs, bjs = [], []

  for index, time in times():
    bjs.append((time - index) % time)
    mjs.append(time)

  return ChineseRemainder(mjs, bjs).solve()


solve_1 = lambda: earliest_departure()
solve_2 = lambda: match_departure_times()
