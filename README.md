## Advent of Code

Workspace and solutions to fun problems found on [adventofcode.com](https://adventofcode.com/).

### Initialize

```
$ make venv
$ . venv/bin/activate
$ make install  # (venv)
```

### Configure

Make sure you are [logged in](https://adventofcode.com/auth/login), then open the page of [any puzzle's input text](https://adventofcode.com/2020/day/1/input) and copy the content of the `session` cookie. Create an `.env` file and define a variable `SESSION=<clipboard>` containing the copied value. Then you can run the following command.

```
$ make new 1
```

This creates a solution script and a corresponding test file and opens them in your editor (`subl`). Additionally, the puzzle input is downloaded and saved in `inputs/day-1.txt`.

### Test

Execute one of these commands to run the tests. The former requires your virtualenv to be loaded, the latter doesn't.

```
$ pytest  # (venv)
$ make test
```

---

#### License

MIT License. See [`LICENSE`](/LICENSE) for details.  
Copyright (c) 2020 Jonas van den Berg
