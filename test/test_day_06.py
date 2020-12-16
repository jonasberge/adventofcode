from test.helper import use_example


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 6

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_1() == 11

  def test_solution(self, problem):
    assert problem.solve_1() == 6549


class part_2:
  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_2() == 6

  def test_solution(self, problem):
    assert problem.solve_2() == 3466
