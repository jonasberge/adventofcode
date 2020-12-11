from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 37

  def test_solution(self, problem):
    assert problem.solve_1() == 2448


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_2() == 26

  def test_solution(self, problem):
    assert problem.solve_2() == 2234
