from collections import deque

from lib.input import read_lines


input = read_lines(9)
input = [ int(line) for line in input ]


"""

...
<X[k-25] ... X[k-1]>
<X[k]>
...

for an X[k] there is at least one
i and j for which the following holds:

X[k] = X[k-i] + X[k-j]  and
1 <= i,j <= 25  and
i <> j

find an algorithm which proves this
and which is able to detect if an
element does not conform to it.


solution:

for every number, subtract one of the
previous 25 numbers and check if the
result is equal to one of them.

"""


def attack_weakness(size):
  history = deque()
  previous = set()

  numbers = deque(input)

  for _ in range(size):
    number = numbers.popleft()
    history.append(number)
    previous.add(number)

  while numbers:
    number = numbers.popleft()
    is_valid = False

    for other in previous:
      if number - other in previous:
        is_valid = True
        break

    if not is_valid:
      return number

    left = history.popleft()
    previous.remove(left)

    history.append(number)
    previous.add(number)

  raise Exception('No attack surface')


def solve():
  return (
    attack_weakness(25),
    0
  )
