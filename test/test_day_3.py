from test.helper import use_example


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve()[0] == 7

  def test_solution(self, problem):
    assert problem.solve()[0] == 234


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve()[1] == 336

  def test_solution(self, problem):
    assert problem.solve()[1] == 5813773056
