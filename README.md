# Thought Machine - Test exercise

### Thoughts
The task was quite interesting and I've even got a bit carried away providing extra options.
The solution is based on the idea that report formats are more or less in line with provided examples, but the solution can be tweaked endlessly to support any text reprots, provided some level of consistency is there.

---

### Installation
As requested, the project only uses standard libraries, so no extra requirements have to be satisfied.

I was using `Python 3.9.7`, but any `Python 3` should do.

---

### Execution

To run against a report file, execute:
> `python3 main.py -f /path/to/file.txt` where `path/to/file.txt` can **either be relative or absolute.**

#### Additional arguments:
> `--file` - specify filepath

> `-d` or `--dir` - specify the directory to process multiple files

> `--failed` - displays a list of failed scenarios

> `--skipped` - displays a list of skipped scenarios, with reasons for skipping

> `--full` - displays reports unchanged
