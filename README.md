## Advent of Code

Workspace and solutions to fun problems found on [adventofcode.com](https://adventofcode.com/).

### Initialize

```
$ make venv
$ . venv/bin/activate
$ make install
```

### Configure

Make sure you are [logged in](https://adventofcode.com/auth/login), then open the page of [any puzzle's input text](https://adventofcode.com/2020/day/1/input) and copy the content of the `session` cookie. Create an `.env` file and define a variable `SESSION=<clipboard>` containing the copied value. Then you can run the following command.

```
$ make touch 1
```

This creates a solution script and a corresponding test file. Additionally, the puzzle input is downloaded and saved in `inputs/day-1.txt`. Relevant files for solving the problem are opened in your editor (`subl`).

### Run

To run e.g. the first part of your first solution execute the command below. You can also omit the second parameter to execute both solutions at once sequentially.

```
$ python solve.py 1 1
605364
$ python solve.py 1
605364
128397680
```

### Test

Execute one of these commands to run the tests. The former requires your virtualenv to be loaded, the latter doesn't.

```
$ pytest
$ make test
```

---

#### License

MIT License. See [`LICENSE`](/LICENSE) for details.  
Copyright (c) 2020 Jonas van den Berg
