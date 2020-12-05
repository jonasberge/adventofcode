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


def highest_seat_id():
  return max(seat_id(line) for line in input)


def solve():
  return (
    highest_seat_id(),
    None
  )
