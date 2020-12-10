from copy import deepcopy
from functools import partial
import re

from lib.input import read_lines


input = read_lines(8)

pattern = re.compile(r"([a-z]+)\s((?:\+|-)\d+)")


def instructions():
  for line in input:
    match = re.match(pattern, line)
    operation, argument = match.groups()
    yield operation, int(argument)


def parse_code():
  program = Program()

  for operation, argument in instructions():
    program.add_instruction(operation, argument)

  return program


class System:
  def __init__(self):
    self._accumulator = 0
    self._counter = 0

    self._operations = {}

    operations = self.Operations
    for name in dir(operations):
      if name.startswith('__'):
        continue

      method = getattr(self.Operations, name)
      if not callable(method):
        continue

      operation = partial(method, self)
      self._operations[name] = operation

  def execute(self, operation, *args):
    execute = self._operations[operation]
    return execute(*args)

  def load(self, program):
    self._counter = 0  # reset program counter.
    return Process(self, program)

  def accumulate(self, by):
    self._accumulator += by

  def jump(self, offset):
    self._counter += offset

  def accumulator(self):
    return self._accumulator

  def program_counter(self):
    return self._counter

  def increment_counter(self):
    self._counter += 1

  class Operations:
    pass


class Program:
  def __init__(self):
    self.instructions = []

  def add_instruction(self, operation, *args):
    instruction = (operation, args)
    self.instructions.append(instruction)

  def __len__(self):
    return len(self.instructions)


#
# "Ein Prozess ist ein Programm in Ausführung."
#   - Stefan Karsch
#

class Process:
  def __init__(self, system, program):
    self._system = system
    self._program = program

  def is_running(self):
    counter = self._system.program_counter()
    return counter in range(len(self._program.instructions))

  def step(self):
    counter = self._system.program_counter()
    operation, arguments = self._program.instructions[counter]

    self._system.execute(operation, *arguments)
    self._system.increment_counter()


class Console(System):
  class Operations:
    def acc(self, by):
      self.accumulate(by)

    def jmp(self, offset):
      # subtract 1 because the process will increment
      # the program counter after this operation.
      self.jump(offset - 1)

    def nop(self, _):
      pass


def find_loop(program):
  visited = set()
  is_looping = False

  system = Console()
  process = system.load(program)

  while process.is_running():
    program_counter = system.program_counter()

    if program_counter in visited:
      is_looping = True
      break

    visited.add(program_counter)
    process.step()

  return system.accumulator(), is_looping


def alternative_programs():
  original_program = parse_code()

  for i in range(len(original_program)):

    instruction = original_program.instructions[i]
    operation, arguments = instruction

    if operation in ('jmp', 'nop'):
      new_operation = 'nop' if operation == 'jmp' else 'jmp'
      new_instruction = (new_operation, arguments)

      alternative_program = deepcopy(original_program)
      alternative_program.instructions[i] = new_instruction

      yield alternative_program


def fix_code():
  """ naive approach of just trying every combination. """

  for program in alternative_programs():
    accumulator, is_looping = find_loop(program)
    if not is_looping:
      return accumulator

  raise Exception('Code cannot be fixed by flipping a single operation')


solve_1 = lambda: find_loop(parse_code())[0]
solve_2 = lambda: fix_code()
