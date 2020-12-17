## Advent of Code

Workspace and solutions to fun problems found on [adventofcode.com](https://adventofcode.com/).

### Initialize

```
$ make install
$ . venv/bin/activate
```

### Configure

Make sure you are [logged in](https://adventofcode.com/auth/login), then open the page of [any puzzle's input text](https://adventofcode.com/2020/day/1/input) and copy the content of the `session` cookie. Create an `.env` file and define a variable `SESSION=<clipboard>` containing the copied value. This step is necessary for downloading the input and the full lore of a problem.

### Solve

Now you can run the following command to start with your first puzzle:

```
$ make touch 1
```

This creates a solution script and a corresponding test file. Additionally, the puzzle input is downloaded and saved to - in this case - `inputs/day-1.txt`. Relevant files for solving the problem are then opened in your editor (`subl`).

### Run

To run e.g. the first part of your first solution execute the command below. You can also omit the second parameter to execute both solutions at once and in sequence.

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

### Lore

After you at least solved the first part of a problem you can download the entire description/lore of both parts, convert it into a neat little Markdown file and save the content to the [`lore`](/lore) folder.

```
$ make lore 1
```

---

#### License

MIT License. See [`LICENSE`](/LICENSE) for details.  
Copyright (c) 2020 Jonas van den Berg
