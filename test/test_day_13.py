from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 295

  def test_solution(self, problem):
    assert problem.solve_1() == 2935


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_2() == 1068781

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_2() == 3417

  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_2() == 754018

  @use_example(4)
  def test_example_4(self, problem):
    assert problem.solve_2() == 779210

  @use_example(5)
  def test_example_5(self, problem):
    assert problem.solve_2() == 1261476

  @use_example(6)
  def test_example_6(self, problem):
    assert problem.solve_2() == 1202161486

  def test_solution(self, problem):
    assert problem.solve_2() == 836024966345345
