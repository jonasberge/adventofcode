from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 165

  def test_solution(self, problem):
    assert problem.solve_1() == 3059488894985


class part_2:
  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_2() == 208

  def test_solution(self, problem):
    assert problem.solve_2() == 2900994392308
