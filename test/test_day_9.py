import pytest

from test.helper import use_example


class part_1:
  @use_example(1)
  def test_example_1(self, problem):
    assert problem.attack_weakness(5) == 127

  def test_solution(self, problem):
    assert problem.solve_1() == 552655238


class part_2:
  @use_example(1)
  @pytest.mark.depends(on=['part_1::test_example_1'])
  def test_example_1(self, problem):
    target = problem.attack_weakness(5)
    assert problem.break_encryption(target) == 62

  def test_solution(self, problem):
    assert problem.solve_2() == 70672245
