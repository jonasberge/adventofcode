from collections import deque

from lib.input import read_lines


input = read_lines(18)


def evaluate_simple(line):
  stack = deque()
  n, op = None, None

  for char in line:
    if char == '(':
      stack.append((n, op))
      n, op = None, None
      continue

    if char == ')':
      m, op_ = stack.pop()
      if n and m and op_:
        n = op_(m, n)
      continue

    if char.isdigit():
      m = int(char)
      if n and op:
        n = op(n, m)
      else:
        n = m
      continue

    if char == '+':
      op = lambda a, b: a + b
      continue

    if char == '*':
      op = lambda a, b: a * b
      continue

  return n


class State:
  def __init__(self):
    self._ns = deque()
    self._ops = deque()

  def push_n(self, n): self._checked_append(self._ns, n)
  def push_op(self, op): self._checked_append(self._ops, op)

  def pop_n(self): return self._ns.pop()
  def pop_op(self): return self._ops.pop()

  def ns(self): return len(self._ns)
  def ops(self): return len(self._ops)

  def _checked_append(self, stack, value):
    stack.append(value)
    self._check_invariant()

  def _check_invariant(self):
    assert len(self._ns) - len(self._ops) in (1, 0)

  def __bool__(self):
    return bool(self._ns) and bool(self._ops)


def finish(state):
  o_state = State()
  a = state.pop_n()

  while state:
    b = state.pop_n()
    op = state.pop_op()

    if op == '+':
      a = a + b
      continue

    if op == '*':
      o_state.push_n(a)
      o_state.push_op(op)
      a = b
      continue

    assert False

  assert o_state.ns() == o_state.ops()

  while o_state:
    b = o_state.pop_n()
    op = o_state.pop_op()

    if op == '*':
      a = a * b

  return a


def evaluate_advanced(line):
  stack = deque()
  state = State()

  for char in line:
    if char.isspace():
      continue

    if char.isdigit():
      state.push_n(int(char))
      continue

    if char in ('+', '*'):
      state.push_op(char)
      continue

    if char == '(':
      stack.append(state)
      state = State()
      continue

    if char == ')':
      value = finish(state)
      state = stack.pop()
      state.push_n(value)
      continue

    assert False

  return finish(state)


solve_1 = lambda: sum([evaluate_simple(line) for line in input])
solve_2 = lambda: sum([evaluate_advanced(line) for line in input])


"""

state logic of part 2:

1 2 3 4 5 6
+ * + * +


A)
1 2 3 4
+ * + *

-

6 5
+


B)
1 2 3 4
+ * + *

-

11


C)
1 2 3
+ * +

-

11 4
*


D)
1 2 3
+ * +

11
*

4


E)
1 2
+ *

11
*

4 3
+


F)
1 2
+ *

11
*

7 2
*


G)
1
+

11 7
*  *

2


H)
-

11 7
*  *

2 1
+


I)
-

11 7
*  *

3


J)
-

11 7 3
*  *

-


K)
11 7 3
*  *

-

-


L)
11 7 3
*  *

-

-


M)
11 7 3
*  *

-

7 3
*


N)
11
*

-

21


O)
-

-

21 11
*


P)
-

-

231

"""

