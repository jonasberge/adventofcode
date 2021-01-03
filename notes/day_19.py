from collections import defaultdict, deque
from copy import copy, deepcopy
import re

from lib.input import read_lines


input = read_lines(19)

FIRST_RULE = 0

pattern = r"^(\d+):\s(?:\"(\w)\"|(\d+)(?:\s(\d+))?(?:\s\|\s(\d+)(?:\s(\d+))?)?)$"
pattern = re.compile(pattern)


def parse_rules(lines):
  rules = {}

  for line in lines:
    if not line:
      break

    match = re.match(pattern, line)
    rule, char, a1, a2, b1, b2 = match.groups()
    rule = int(rule)

    if char:
      rules[rule] = char
      continue

    parts = []
    if a1 and a2: parts.append((int(a1), int(a2)))
    if b1 and b2: parts.append((int(b1), int(b2)))
    if a1 and not a2: parts.append((int(a1),))
    if b1 and not b2: parts.append((int(b1),))
    rules[rule] = parts

  return rules























class Element:
  pass

class Reference(Element):
  def __init__(self, rule):
    self.rule = rule

class Terminal(Element):
  def __init__(self, word):
    self.word = word






























































class Cursor:
  def __init__(self, rule, option=0, index=0, parser=None):
    self.rule_number = rule
    self.rule_option = option
    self.option_index = index

    self.parser = parser

  def rule(self): return self.parser.rules[self.rule_number]
  def option(self): return self.rule()[self.rule_option]

  def value(self):
    if self.is_terminal():
      return self.rule()
    return self.option()[self.option_index]

  def is_reference(self):
    return isinstance(self.rule(), list) \
      and isinstance(self.option(), tuple) \
      and isinstance(self.value(), int)

  def is_terminal(self):
    return isinstance(self.rule(), str)

  def has_next(self):
    if self.is_terminal():
      return False
    return self.option_index + 1 in range(len(self.option()))

  def next(self):
    self.option_index += 1

  def __repr__(self):
    return '({}, {}, {})'.format(
      self.rule_number,
      self.rule_option,
      self.option_index
    )


class State:
  def __init__(self):
    self._stack = []

  def push(self, cursor):
    self._stack.append(cursor)

  def pop(self): return self._stack.pop()
  def top(self): return self._stack[-1]

  def __bool__(self): return bool(self._stack)
  def __len__(self): return len(self._stack)

  def __copy__(self):
    new = type(self)()
    new._stack = copy(self._stack)
    return new

  def __repr__(self):
    return '-{}-'.format(
      ''.join(repr(self._stack))
    )


class DoneParsing(Exception): pass
class FailedParsing(Exception): pass
class ContinueParsing(Exception): pass


class Parser:
  def __init__(self, rules):
    self.rules = rules

    origin = State()
    origin.push(self.make_cursor(0, 0, 0))
    self.step_states = [origin]
    self.matched_states = []

  def make_cursor(self, *args, **kwargs):
    return Cursor(*args, parser=self, **kwargs)

  def step(self, char):

    if not self.step_states:
      if not self.matched_states:
        raise FailedParsing

      convert_states = self.matched_states
      self.matched_states = []

      for state in convert_states:
        while len(state) > 1 and not state.top().has_next():
          state.pop()
        if len(state) == 1 and not state.top().has_next():
          raise DoneParsing
        state.top().next()

      self.step_states = convert_states

      print('!', self.step_states)
      print('!', self.matched_states)
      print()

      raise ContinueParsing

    new_states = []
    matched_states = []

    for state in self.step_states:
      cursor = state.top()

      if cursor.is_terminal():
        if cursor.value() == char:
          matched_states.append(state)

      elif cursor.is_reference():
        next_rule_number = cursor.value()
        new_cursor = self.make_cursor(next_rule_number)
        for rule_option in range(len(new_cursor.rule())):
          new_state = copy(state)
          new_state.push(self.make_cursor(next_rule_number, rule_option))
          new_states.append(new_state)

    self.step_states = new_states
    self.matched_states = matched_states

    print(self.step_states)
    print(self.matched_states)
    print('->>>', end=' ')
    for state in matched_states:
      if state:
        print(state.top().value(), end=',')

    print()






def main(rules, word):

  # parser = Parser({
  #   0: [(4, 1, 5)],
  #   1: [(2, 3), (3, 2)],
  #   2: [(4, 4), (5, 5)],
  #   3: [(4, 5), (5, 4)],
  #   4: 'a',
  #   5: 'b'
  # })

  # parser = Parser({
  #   0: [(1, 2)],
  #   1: 'a',
  #   2: [(1, 3), (3, 1)],
  #   3: 'b'
  # })

  # word = 'abb'
  # rules = {
  #   0: [(1, 4)],
  #   1: [(20,)],
  #   20: [(21,)],
  #   21: [(22,)],
  #   21: [(23,)],
  #   23: [(2,)],
  #   2: [(3, 4)],
  #   3: 'a',
  #   4: 'b'
  # }

  # for key, stuff in rules.items():
  #   print('{}: {}'.format(key, stuff))
  # print()

  parser = Parser(rules)
  it = iter(word)

  try:
    char = next(it)
  except StopIteration:
    return False

  while True:
    try:
      print('> Stepping')
      parser.step(char)
    except ContinueParsing:
      print('caught:', ContinueParsing.__name__)
      try:
        char = next(it)
      except StopIteration:
        return False
    except FailedParsing:
      print('caught:', FailedParsing.__name__)
      return False
    except DoneParsing:
      print('caught:', DoneParsing.__name__)
      break

  print('Parser is done!')

  try:
    next(it)
  except StopIteration:
    print('Word is empty!')
  else:
    print('More to parse! Damn it!')
    return False

  print('Success!')

  return True






def parse(word, rules):

  word_iter = iter(word)

  c = next(word_iter)

  n = []
  m = [
    [ State(0, 0, 0) ]
  ]

  count = 0

  while True:
    n = m
    m = []

    for steps in n:
      s = []
      for state in steps:
        s.append(state)

      last = s[-1]
      number = rules[last.rule][last.option][last.index]

      if isinstance(rules[number], str):
        if rules[number] == c:
          while s:
            print('next?', s[-1], s[-1].has_next(rules))
            if s[-1].has_next(rules):
              break
            s.pop()

          if not s:
            raise Exception  ## ??

          top = s[-1]
          top.step()
          m.append(copy(s))  # to be safe, likely no copy needed

        continue

      current_number = number

      remaining_options = [ list(reversed(range(len(rules[current_number])))) ]
      taken_options = [ [] ]


        # take = remaining_options[-1].pop()
        # push = State(current_number, take, 0)

        # s.append(push)
        # taken_options.append(take)

        # current_number = rules[push.rule][push.option][push.index]

        # if isinstance(current_number, str):



        # remaining_options.append(list(reversed(range(len(rules[current_number])))))





    print(m)

    count += 1
    if count == 2:
      break

  pass


def part_1():

  lines = iter(input)
  rules = parse_rules(lines)

  # return main(rules, 'bbabbbaaaaaabbabbaabaaabbaababbbabbbabbbababbbbbbbbabbbbbbabaaaa')

  count = 0

  for word in lines:
    print('match?', main(rules, word), word)

    if main(rules, word):
      count += 1

  return count


def part_2():
  return None


solve_1 = lambda: part_1()
solve_2 = lambda: part_2()








"""

POS: 0, 0

-: 0
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

"""

"""

    0
   / \
  1   2------|
  |   |      |
  a   |      |
     / \    / \
    1   3  3   1
    |   |  |   |
    a   b  b   a

"""


# class StopStepping(Exception):
#   pass


# class State:
#   def __init__(self, rule, option, index):
#     self.rule = rule
#     self.option = option
#     self.index = index

#     self.steps = deque()

#   def step(self, rules):
#     option = rules[self.rule][self.option]
#     if self.index + 1 in range(len(option)):
#       return State(self.rule, self.option, self.index + 1)
#     return False

#   def is_end(self, rules):
#     option = rules[self.rule][self.option]
#     return self.index == len(option) - 1

#   def __repr__(self):
#     return '{}({}, {}, {})'.format(
#       self.__class__.__name__,
#       self.rule, self.option, self.index
#     )


# class StateMachine:
#   def __init__(self, rules):
#     self._rules = rules
#     self._states = []
#     self._has_done = False

#     for option in range(len(rules[0])):
#       self._states.append(State(0, option, 0))

#   def is_done(self):
#     return self._has_done

#   def step(self, char):
#     if not self._states:
#       raise StopStepping

#     new_states = []

#     matched_char = False
#     has_done = False

#     for state in self._states:
#       next_rule = self._rules[state.rule][state.option][state.index]

#       print('next', next_rule)

#       # rule is ended by a terminal.
#       if isinstance(self._rules[next_rule], str):
#         if self._rules[next_rule] == char:
#           next_state = state.step(self._rules)
#           if next_state:
#             new_states.append(next_state)
#           else:
#             has_done = True
#         matched_char = True
#         continue

#       steps = deque()
#       steps.append(state)

#       # inter_states = []

#       for i, options in enumerate(self._rules[next_rule]):
#         new_state = State(next_rule, i, 0)
#         new_state.steps = copy(steps)
#         new_states.append(new_state)

#       # new_states = inter_states


#     if new_states:
#       for new in new_states:
#         print(' new', new, new.steps)

#     self._has_done = has_done
#     self._states = new_states

#     return matched_char


# def check(word, rules):

#   state_machine = StateMachine(rules)

#   it = iter(word)
#   char = next(it)

#   while True:
#     try:
#       matched = state_machine.step(char)
#     except StopStepping:
#       break

#     if not matched:
#       continue

#     try:
#       char = next(it)
#     except StopIteration:
#       break

#   try:
#     next(it)
#     is_empty = False
#   except StopIteration:
#     is_empty = True

#   return is_empty and state_machine.is_done()


#   # print('matched:', state_machine.step(word[0]))
#   # print('matched:', state_machine.step(word[1]))
#   # print('matched:', state_machine.step(word[1]))
#   # print('matched:', state_machine.step(word[2]))

#   # print('has_done:', state_machine.is_done())

#   # return 0
