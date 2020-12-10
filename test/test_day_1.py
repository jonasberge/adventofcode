from test.helper import use_example


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 514579

  def test_solution(self, problem):
    assert problem.solve_1() == 605364


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_2() == 241861950

  def test_solution(self, problem):
    assert problem.solve_2() == 128397680
