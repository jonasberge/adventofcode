from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 8

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_1() == 2

  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_1() == 3

  def test_solution(self, problem):
    assert problem.solve_1() == 165


class part_2:
  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_2() == 12

  def test_solution(self, problem):
    assert problem.solve_2() == 274
