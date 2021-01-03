from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 20899048083289

  def test_solution(self, problem):
    assert problem.solve_1() == 104831106565027


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_2() == 273

  def test_solution(self, problem):
    assert problem.solve_2() == 2093
