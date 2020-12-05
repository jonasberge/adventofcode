from lib.input import read_lines


input = read_lines(5)

replace = {
  'F': 0,
  'B': 1,
  'L': 0,
  'R': 1
}


def seat_id(line):
  for char, to in replace.items():
    line = line.replace(char, str(to))
  return int(line, 2)


def seat_ids():
  return [ seat_id(line) for line in input ]


def highest_seat_id():
  return max(seat_ids())


def my_seat_id():
  seats = set(seat_ids())

  other = [
    seat
    for seat in seats
    if seat - 1 not in seats and seat - 2 in seats
    or seat + 1 not in seats and seat + 2 in seats
  ]

  assert len(other) == 2, 'the condition is ambiguous'

  return max(other) - 1


def my_seat_id_2():
  seats = sorted(seat_ids())

  for i in range(len(seats)):
    if i == len(seats) - 1:
      break

    p1, n1 = seats[i:i + 2]

    if n1 == p1 + 2:
      return p1 + 1


def solve():
  return (
    highest_seat_id(),
    my_seat_id_2()
  )
