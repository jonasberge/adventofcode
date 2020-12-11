from importlib import import_module
from sys import argv, exit


if __name__ == '__main__':
  if len(argv) not in (2, 3): exit(1)

  day = argv[1]
  part = int(argv[2]) if len(argv) == 3 else None

  try: module = import_module('src.day_{}'.format(day))
  except Exception as e:
    raise e

  if part:
    if part not in (1, 2):
      raise Exception('Part number must be either 1 or 2')
    solve = module.solve_1 if part == 1 else module.solve_2
    print(solve())
    exit()

  print(module.solve_1(), flush=True)
  print(module.solve_2())
