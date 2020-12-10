from test.helper import use_example


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve()[0] == 357

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve()[0] == 70 * 8 + 7

  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve()[0] == 14 * 8 + 7

  @use_example(4)
  def test_example_4(self, problem):
    assert problem.solve()[0] == 102 * 8 + 4

  def test_solution(self, problem):
    assert problem.solve()[0] == 935


class part_2:
  def test_solution(self, problem):
    assert problem.solve()[1] == 743
