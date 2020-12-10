from os import path
from importlib import import_module, reload as reload_module

from pytest import fixture
from unittest import mock

from lib.input import ROOT_PATH
from lib.input import file_for_day


INPUTS_EXAMPLES_DIR = 'inputs/examples'
INPUTS_EXAMPLES_PATH = path.join(ROOT_PATH, INPUTS_EXAMPLES_DIR)


def load_solution(day):
  module = import_module('src.day_{}'.format(day))
  reload_module(module)
  return module


@fixture(params=[(False, None)], ids=[1])
def problem(request):
  use_example, example = request.param

  test_file = path.basename(request.node.fspath)
  test_file = path.splitext(test_file)[-2].split('_')
  day = int(test_file[-1])

  if not use_example:
    return load_solution(day)

  with mock.patch('lib.input.file_for_day') as mock_file_for_day:
    # file_path = file_for_day(day, example, INPUTS_EXAMPLES_PATH)
    file_path = path.join(INPUTS_EXAMPLES_PATH, 'day-{}'.format(day), 'example-{}.txt'.format(example))
    mock_file_for_day.return_value = file_path
    return load_solution(day)
