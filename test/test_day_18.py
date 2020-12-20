from test.helper import use_example, skip


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_1() == 71

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_1() == 51

  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_1() == 26

  @use_example(4)
  def test_example_4(self, problem):
    assert problem.solve_1() == 437

  @use_example(5)
  def test_example_5(self, problem):
    assert problem.solve_1() == 12240

  @use_example(6)
  def test_example_6(self, problem):
    assert problem.solve_1() == 13632

  def test_solution(self, problem):
    assert problem.solve_1() == 45840336521334


class part_2:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.solve_2() == 231

  @use_example(2)
  def test_example_2(self, problem):
    assert problem.solve_2() == 51

  @use_example(3)
  def test_example_3(self, problem):
    assert problem.solve_2() == 46

  @use_example(4)
  def test_example_4(self, problem):
    assert problem.solve_2() == 1445

  @use_example(5)
  def test_example_5(self, problem):
    assert problem.solve_2() == 669060

  @use_example(6)
  def test_example_6(self, problem):
    assert problem.solve_2() == 23340


  def test_solution(self, problem):
    assert problem.solve_2() == 328920644404583
