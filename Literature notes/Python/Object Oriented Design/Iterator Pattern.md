---
Created Date: 2026-05-19
tags:
  - python
  - architecture
  - programming
Next: "[[Common Design Patterns]]"
---
---
## What we Learn
- What is design patterns are
- The iterator protocol one of the most powerful design patterns
- List, set, and dictionary comprehensions
- Generator functions, and how they build on other patterns

---
## Design pattern
 **Design patterns** are applied to *solve* a *common problem* faced by developers in some specific *situation*. The **design pattern** is a suggestion as to the ideal *solution* for that *problem*, in terms of *object-oriented design*. What's central to a *pattern* is that it is reused often in unique contexts.


---
## Iterators
In typical *design pattern* parlance, an *iterator* is an object with a `next()` method and a `done()` *method*; the latter returns *True* if there are no items left in the *sequence*.

```python
while ont iterator.done():
	item = iterator.next()
	# somthing do with the item
```


### The Iterator protocol
At the foundation, any *Collection* class definition must be *Iterable*. To be *Iterable* means implementing an `__iter__()` *method*; this method creates an *Iterator object*.
As mentioned, an *Iterator* class must define a `__next__()` *method* that the for *statement* (and other features that support *iteration*) can call to get a new element from the *sequence*. In addition, every *Iterator class* must also fulfill the *Iterable interface*.

```python
from typing import Iterable, Iterator

class CapitalIterable(Iterable[str]):
	def __init__(self, string: str) -> None:
		self.string = string
	
	def __iter__(self) -> Iterator[str]:
		return CapitalIterator(self.string)

class CapitalIterator(Iterator[str]):
	def __init__(self, string: str) -> None:
		self.words = [w.capitalize() for w in string]
		self.index = 0
	
	def __next__(self) -> str:
		if self.index == len(self.words):
			raise StopIteration()
		word = self.words[self.index]
		self.index += 1
		return word
```

- another way interact with *iterator* is `iter()` method :
```sh
>>> iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')
>>> iterator = iter(iterable)
>>> while True:
... try:
	... print(next(iterator))
... except StopIteration:
	... break
...
```

---
- **Iterable:** iterable is an *object* with *elements* that can be *iterated* over , and these *elements* can looped over *multiple* even at a same time
- **Iterator:** specific location in that *iterable* *object*  every time call `next()` on iterator update internal *state*
---
- **Comprehensions** are simple, but *powerful*, *syntaxes* that allow us to *transform* or *filter* an *iterable object* in as *little* as one *line of code*. The resultant object can be a perfectly normal *list*, *set*, or *dictionary*, or it can be a *generator* expression that can be *efficiently* consumed while keeping just one *element* in *memory* at a *time*.
---
### Generator Expression
When processing one *item* at a time, we only need the current *object* available in *memory* at any one *moment*.
If we want to *process* each *line* in the *log*, we can't use a *list comprehension*; it would create a *list* containing every *line* in the *file*. This probably wouldn't fit in *RAM* and could bring the *computer* to its knees, depending on the operating system.

```python
with full_log_path.open("r") as source:
	warning_lines = (line for line in source if "WARN" in line)
	with warning_log_path.open("w") as target:
		for line in warning_lines:
			target.write(line)
```

### Generator Functions

```python
import csv
import re
from pathlib import Path
from typing import Match, cast

def extract_and_pard_1(full_log_path: Path, warning_log_path: Path) -> None:
	with warning_log_path.open("w") as target:
		csv.write(target, delimiter="\t")
		pattern = re.compile(
			r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(\w+)] (.+)"
		)
		with full_log_path.open("r") as source:
			for line in source:
				if "WARN" in line:
					line_groups = cast(Match[str], pattern.match(line).groups())
					writer.writerow(line_groups)
```

- object-oriented solution
```python
import re  
import csv  
from pathlib import Path  
from typing import TextIO, cast, Iterator, Tuple, Match  
  
class WarningReformat(Iterator[Tuple[str, ...]]):  
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(\w+)] (.+)")  
  
    def __init__(self, source: TextIO) -> None:  
        self.sequence = source  
  
    def __iter__(self) -> Iterator[Tuple[str, ...]]:  
        return self  
    def __next__(self) -> Tuple[str, ...]:  
        line = self.sequence.readline()  
        while line and "WARN" not in line:  
            line = self.sequence.readline()  
        if not line:  
            raise StopIteration  
        return cast(Match[str], self.pattern.match(line)).groups()  
  
  
def extract_and_parse(  
        full_log_path: Path,  
        warning_log_path: Path,  
) -> None:  
    with warning_log_path.open("w") as target:  
        csv_writer = csv.writer(target)  
        with full_log_path.open("r") as source:  
            filter_reformat = WarningReformat(source)  
            for line_group in filter_reformat:  
                csv_writer.writerow(line_group)
```

-  We've defined a formal `WarningReformat` *iterator* that *emits* the *three-tuple* of the date, *warning*, and *message*. We've used a *type hint* of t`uple[str, ...] `because it *matches* the output from the `self.pattern.match(line).groups()`.


- we finally get to see true **generators** in action. This next example does exactly the same thing as the previous one: it creates an object with a `__next__() `method that raises `StopIteration` when it's out of inputs:
```python
def warnning_filer(source: Iterator[str]) -> Iterator[tuple[str, ...]]:
	pattern = re.compile(
		r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
	for line in source:
		if "WARN" in line:
			yield tuple(
				cast(Match[str], pattern.match(line)).groups())
```


>[!IMPORTANT]
> The **generator** object has `__iter__() `and `__next__() `*methods* on it, just like the one we created from a class definition in the previous example. (Using the `dir()` built-in function on it will reveal what else is part of a **generator**.) Whenever the `__next__() `method is called, the **generator** runs the function until it finds a *yield statement*. It then suspends *execution*, retaining the **current state**, and returning the value from *yield*. The next time the `__next__()` method is called, it *restores* the **state** and picks up *execution* where it left off.



---
### Yield items from another iterator
situation where we want to **yield** data from another *iterable object*, possibly a list *comprehension* or **generator** expression we *constructed* inside the **generator**, or perhaps some *external* *items* that were passed into the *function*. We'll look at how to do this with the **yield** from statement.

```python
def file_extract(
	path_iter: Itarator[Path]
) -> Iterator[tuple[str, ...]]:
	for path in path_iter:
		with path.open() as infile:
			yield from warnning_filter(infile)

def extract_and_parse_d(
	directory: Path, warning_log_path: Path) -> None:
	with warning_log_path.open("w") as target:
		writer = csv.writer(target, delimiter="\t")
		log_files = list(directory.glob("sample*.log"))
		for line_groups in file_extract(log_files):
			writer.writerow(line_groups)
```


---
### Generator Stacks
A **generator** **stack** means **generators** calling other **generators**, forming a *chain* or *pipeline*.

```python
pattern = re.compile(
	r"(?P<dt>\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d)"
	r"\s+(?P<level>\w+)"
	r"\s+(?P<msg>.*)"
)

possible_match_iter = map(pattern.match, source)
good_match_iter = filter(None, possible_match_iter)
group_iter = map(lambda m: m.groupdict(), good_match_iter)
warnings_iter = filter(lambda g: "WARN" in g["level"], group_iter)
```