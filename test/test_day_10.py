from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve()[0] == 7 * 5

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve()[0] == 22 * 10

  def test_solution(self, problem):
    assert problem.solve()[0] == 2400


@skip
class part_2:
  def test_solution(self, problem):
    assert problem.solve()[1] == 0000
