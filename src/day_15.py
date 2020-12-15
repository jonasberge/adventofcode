from lib.input import read_lines


input = read_lines(15)
input = input[0].split(',')
input = list(map(int, input))


class Game:
  def __init__(self):
    self._memory = {}
    self._last = None
    self._turn = 1

  def add(self, number):
    self._last = number
    self._last_spoken_on = self._memory.get(number, None)
    self._memory[number] = self._turn
    self._turn += 1

  def step(self):
    last_spoken = self._last_spoken_on
    number = self._turn - last_spoken - 1 if last_spoken else 0
    self.add(number)

  @property
  def turn(self):
    return self._turn

  @property
  def last(self):
    return self._last


def solve(turns):
  game = Game()
  for number in input:
    game.add(int(number))

  steps = turns - len(input)
  for step in range(steps):
    game.step()

  return game.last


solve_1 = lambda: solve(2020)
solve_2 = lambda: solve(30000000)
