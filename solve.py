from importlib import import_module
from sys import argv, exit


if __name__ == '__main__':
  if len(argv) != 2: exit(1)

  day = argv[1]

  try: module = import_module('src.day_{}'.format(day))
  except Exception as e:
    raise e

  print(module.solve())
