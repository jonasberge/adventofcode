from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 71

  def test_solution(self, problem):
    assert problem.solve_1() == 29759


class part_2:
  @use_example(2)
  def test_example_2(self, problem):
    assert problem.own_ticket_values() == [12, 11, 13]

  def test_solution(self, problem):
    assert problem.solve_2() == 1307550234719
