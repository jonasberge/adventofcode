from collections import defaultdict, deque

from lib.input import read_lines


input = read_lines(10)
input = [ int(line) for line in input ]
input = sorted(input)

input.insert(0, 0)  # charging outlet
input.append(input[-1] + 3)  # built-in adapter


def differences(tolerance):
  counts = defaultdict(int)

  for i in range(len(input) - 1):
    r, s = input[i:i + 2]
    counts[s - r] += 1

  return counts[1] * counts[tolerance]


def arrangements(tolerance):
  """ solution: use dynamic programming by going backward.

      e.g. numbers: 1, 3, 4, 6
      solutions: 1346, 136, 146

      iterate starting at the last (i.e. largest) element.
      notation: X => N = a+b+c (U, V, W): X -> U, X -> V, X -> W
      - X is the current number.
      - N is the number of possibilities to arrange starting at X.
      - a+b+c are the N's of U, V and W respectively.
        some elements may be omitted.
      - U, V and W are nodes after X which are in range
        i.e. X < U,V,W <= X+3
      - i -> j denotes a possible connection between i and j

      I.   6 => 1 (): 6
      II.  4 => 1 (6): 4 -> 6
      III. 3 => 2 (4, 6): 3 -> 4, 3 -> 6
      IV.  1 => 3 = 2 + 1 (3, 4): 1 -> 3, 1 -> 4

      => U, V and W are reused from previous results (dp).
  """

  ratings = deque(input)
  dp = dict()

  # initialize with the last element.
  dp[ratings.pop()] = 1

  while ratings:
    rating = ratings.pop()
    possibilities = 0

    for other in range(rating + 1, rating + tolerance + 1):
      if other in dp:
        possibilities += dp[other]

    dp[rating] = possibilities

  return dp[input[0]]


solve_1 = lambda: differences(3)
solve_2 = lambda: arrangements(3)
