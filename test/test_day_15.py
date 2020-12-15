from test.helper import use_example, skip


@use_example(1)
def test_example_1(problem):
  assert problem.solve_1() == 436

@use_example(2)
def test_example_2(problem):
  assert problem.solve_1() == 1

@use_example(3)
def test_example_3(problem):
  assert problem.solve_1() == 10

@use_example(4)
def test_example_4(problem):
  assert problem.solve_1() == 27

@use_example(5)
def test_example_5(problem):
  assert problem.solve_1() == 78

@use_example(6)
def test_example_6(problem):
  assert problem.solve_1() == 438

@use_example(7)
def test_example_7(problem):
  assert problem.solve_1() == 1836

def test_solution(problem):
  assert problem.solve_1() == 1294
