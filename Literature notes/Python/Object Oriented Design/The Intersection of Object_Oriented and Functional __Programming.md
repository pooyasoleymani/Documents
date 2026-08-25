---
Created Date: 2026-05-17
tags:
  - python
  - architecture
  - programming
Next: "[[String, Serialization, and File Paths]]"
---
---
## What We Learn
- Built-in *functions* that take care of common tasks in one call
- An alternative to *method overloading*
- *Functions* as *objects*
- *File I/O* and *context managers*

---
## Python Built-in Functions

### 1. `len()` function
This function call `__len__()` method in object.
- Why should we use `len()` instead of the `__len__()`:
	- When we use `__len__()` *object* has look at method in its *namespace*, and if is *special* `__getattribute__()` method (which is called every time an *attribute* or *method* on an *object* is *accessed*) is defined on that object, it has to be called as well.

	- Another reason is *maintainability*. In the future, Python developers may want to change `len()` so that it can calculate the *length* of *objects* that *don't have* `__len__()`, for example, by *counting* the number of *items* returned in an *iterator*. They'll only have to change one *function* instead of *countless* `__len__()` methods in many objects across the board.


### 2. `revesed()` function
The `reversed()` function takes any *sequence* as input and returns a *copy* of that *sequence* in *reverse* order.
Similar to the `len() `function, `reversed() `calls the `__reversed__()` method on the class for the parameter. If that method does not exist, *reversed* builds the reversed *sequence* itself using calls to `__len__()` and` __getitem__()`, which are used to define a *sequence*.

```python
class CustomSequence:
	def __init__(self, args):
		self.aargs_list = args
	def __len__(self):
		return 5
	def __getitem__(self, index):
		return f"x{index}"

class FunkyBackwards(List):
	def __reversed__(self):
		return "BACKWARDS!"

generic = [1, 2, 3, 4, 5]
custom = CustomSequence([generic])
funky = FunkyBackwards([generic])

for sequence in generic, custom, fanky:
	print(f"{sequence.__class__.__name__}: ", end="")
	for item in reversed(sequence):
		print(f"{item}, ", end="")
	print()

# list: 5, 4, 3, 2, 1,
# CustomSequence: x4, x3, x2, x1, x0,
# FunkyBackwards: B, A, C, K, W, A, R, D, S, !,
```

>[!NOTE]
> For `CustomSequence` must define `__iter__()` 
> 


### 3. `enumerate()` function
it creates a *sequence* of *tuples*, where the first object in each *tuple* is the *index* and the second is the *original* *item*.
```python
from pathlib import Path

with Path("docs/sample_data.md").open() as source:
	for index, line in enumerate(source, start=1):
	print(f"{index:3d}: {line.rstrip()}")
```



some of the more interesting ones include the following:
-  `abs()`, `str()`, `repr()`, `pow()`, and `divmod()` map directly to the special methods __`abs__()`, `__str__()`, `__repr__()`, `__pow__(),` and __`divmod__()`

- `bytes()`, `format()`, `hash(),` and `bool() `also map directly to the special methods `__bytes__()`, `__format__()`, `__hash__()`, and `__bool__()`

- `all()` and `any()`, which accept an *iterable* object and return *True* if *all*, or *any*, of the *items* evaluate to *true* (such as a *non-empty string* or list, a *non-zero number*, an object that is not None, or the literal *True*).

- `eval()`, `exec()`, and `compile()`, which *execute* string as *code* inside the

*interpreter*. Be careful with these ones; they are not safe.

- `hasattr()`, `getattr()`, `setattr()`, and `delattr()`, which allow attributes on an object to be *manipulated* by their *string names*.

- `zip()`, which takes two or more *sequences* and returns a new sequence of *tuples*, where each tuple contains a single value from each *sequence*.



---
## An Alternative to method overloading
We'll often have to use a `typing.Union` hint to show that a parameter can have values from `Union[int, str]`. This definition clarifies the alternatives so *mypy* can confirm that we're using the overloaded function *properly*.

We have to distinguish between two varieties of overloading here:
- *Overloading* parameters to allow alternative types using `Union[...]` *hints*
- *Overloading* the *method* by using more *complex* patterns of parameters


--- 
## Default value for parameters
**Keyword only:** After the `*` , the argument must have a keyword supplied.

- If default value of the function parameter is a *mutable* object we to create this in body of the function
```python
def bad_default(tag: str, hidtory: List[str] = []) -> List[str]:
	history.append(tag)
	return history

def good_default(tag: str, history: Optional[List[str]] = None) -> List[str]:
	history = [] if history is None else history
	history.append(tag)
	return history
```


---
## Variable argument lists
1. One thing that makes Python really slick is the ability to write *methods* that accept an *arbitrary* number of *positional* or *keyword* arguments without *explicitly* naming them. We can also pass *arbitrary* *lists* and *dictionaries* into such *functions*. In other languages, these are sometimes called **variadic arguments**, `varargs`.

```python
from urllib.parse import urlparse
from pathlib import Path

def get_pages(*links: str) -> None:
	for link in links:
		url = urlparse(linnk)
		name = "index.html" if url.path in ("", "/") else url.path
		target = Path(ulr.netloc.replace(".", "_")) / name
		print(f"Create {target} from {link!r}")
```

2.  We can also accept *arbitrary* *keyword* *arguments*. These arrive in the function as a *dictionary*. They are specified with *two asterisks* (as in`**kwargs`) in the *function* *declaration*. This tool is commonly used in *configuration* *setups*.

```python
class Options(Dict[str, Any]):
	default+options: dict[str, Any] = {
		"port": 21,
		"host": "localhost",
		"username": None,
		"password": None,
		"debug": False	
	}
	
	def __init__(self, **kwargs: Any) -> None:
		super().__init__(self.default_options)
		self.update(kwargs)
```

- The following example is somewhat contrived, but demonstrates the *four types* of *parameters* in action:
```python
from __future__ import annotations
import contextlib
import os
import subprocess
import sys
from typing import TextIO
from pathlib import Path

def doctest_everything(  
        output: TextIO,  
        *directories: Path,  
        verbose: False,  
        **stems: str  
) -> None:  
    def log(*args, **kwargs) -> None:  
        if verbose:  
            print(*args, **kwargs)  
    with contextlib.redirect_stdout(output):  
        for directory in directories:  
            log(f"Searching in {directory}")  
            for path in directory.glob("**/*.md"):  
                if any(  
                    parent.stem == ".tox"  
                    for parent in path.parents  
                ): continue  
                log(  
                    f"File {path.relative_to(directory)}, "  
                    f"{path.stem}"  
                )  
                if stems.get(path.stem, "").upper() == "SKIP":  
                    log("Skipped")  
                    continue  
                options = []  
                if stems.get(path.stem, "").upper() == "ELLIPSIS":  
                    options.append("ELLIPSIS")  
                search_path = directory / "src"  
                print(  
                    f"cd {Path.cwd()!r}; "  
                    f"PYTHONPATH= {search_path!r}, doctest '{path}' -v"  
                )  
                option_args = (  
                    ["-o", ",".join(options) if options else []]  
                )  
                subprocess.run(  
                    ["python3", "-m", "doctest", "-v"] + option_args + [str(path)],  
                    cwd=directory,  
                    env={"PYTHONPATH": str(search_path)},  
                )


doctest_log = Path("doctest.log")
with doctest_log.open('w') as log:
	doctest_everything(
		log,
		Path.cwd() / "ch_04",
		Path.cwd() / "ch_05",	
		verbose=True
	)


doctest_everything(
	sys.stdout,
	Path.cwd() / "ch_02",
	Path.cwd() / "ch_03",
	examples="ELLIPSIS",
	examples_38="SKIP",
	case_study_2="SKIP",
	case_study_3="SKIP",
)
```


---
## Unpacking arguments
we can use the `*` *operator* inside a *function call* to *unpack* it into the *arguments*.



---
## Functions are objects, too
we'd like an *object* that is a **callable** *function*. This is most frequently done in **event-driven programming**, such as *graphical* *tool kits* or *asynchronous* *servers*.


### Function objects and **callbacks**
The fact that *functions* are *top-level objects* is most often used to pass them around to be *executed* at a *later date*, for example, when a certain *condition* has been *satisfied*.
**Callbacks** are common as part of building a *user interface*: when the user *clicks* on something or *long-running* tasks like file transfer.
```python
from __future__ import annotation
from dataclasses import dataclass, field
import time
import heapq
from typing import Callable, Any, List, Optional

Callback = Callable[[int], None]

@dataclass(frozen=True, order=True)
class Task:
	scheduled: int
	callback: Callback = filed(compare=False)
	delay: int = field(default=0, compare=False)
	limit: int = field(default=1, compare=False)
	
	def repeat(self, current_timeL int) -> Optional["Task"]
		if self.delay > 0 and self.limit > 2:
			return Task(
				current_time + self.delay,
				cast(Callback, self.callback), # type: ignore [misc]
				self.delay,
				self.limit -1
			)
		elif self.dealy > 0 and self.limit == 2:
			return Task(
				current_time + self.delay,
				cast(Callback, self.callback), # type: ignore [misc]
			)
		else:
			return None
		
```


- Here's the overall *Scheduler* *class* that uses these *Task* objects and their *associated* **callback functions**:
```python
class Schedule:  
    def __init__(self) -> None:  
        self.tasks: List[Task] = []  
  
    def enter(  
            self,  
            after: int,  
            task: Callback,  
            delay: int = 0,  
            limit: int = 1,  
    ) -> None:  
        new_task = Task(after, task, delay, limit)  
        heapq.heappush(self.tasks, new_task)  
  
    def run(self) -> None:  
        current_time: int = 0  
        while self.tasks:  
            next_task: Task = heapq.heappop(self.tasks)  
            if (delay := next_task.scheduled - current_time) > 0:  
                time.sleep(delay)  
            current_time = next_task.scheduled  
            next_task.callback(current_time)  
            if again := next_task.repeat(current_time):  
                heapq.heappush(self.tasks, again)
```

- More importantly, the *after*, *delay*, and *limit* parameters should have some *validation* checks. For example, a *negative* value of *after* or *delay* should *raise* a *ValueError exception*. There's a special method name, `__post_init__()`, that a *dataclass* can use for **validation**.

- set of callback functions that test *scheduler class*:
```python
import datetime

def format_time(message: str) -> None:
	now = datetime.datetime.now()
	print(f"{now:%I:%M:%S}: {message}")
	
def one(timer: float) -> None:
	format_time("Called One")
	
def two(timer: float) -> None:
	format_time("Called two")

def three(timer: float) -> None:
	format_time("Called three")

class Repeater:
	def __init__(self) -> None:
		self.counter = 0
	
	def four(self, timer: float) -> None:
		self.counter += 1
		format_time(f"Called Four: {self.counter}")
```


- If *order* matters to your *application*, you'll need an *additional attribute* to *distinguish* among items *scheduled* at the *same time*; a *priority number* is often used for this.



--- 
### Using Functions to patch a class
- We can *patch* method of the objects
```python
class A:
	def show_something(self) -> None:
		print("Class A")

a_object = A()
a.show_something() # Class A

def patched_show_something() -> None:
	print("Class is not A")

a.show_something = patched_show_something
a.show_something() # Class is not A
```

- If we create new object from *class A* object doesn't have *patched* method.
- If we want to *patched* method invoke in every objects of class must *patch* **class**.


>[!IMPORTANT] **Monkey Patching**
> Often, replacing or adding *methods* at *runtime* (called *monkey patching*) is used in *automated* *testing*. If *testing* a *client server* application, we may not want to actually connect to the *server* while *testing* the *client*; this may result in *accidental* transfers of funds or embarrassing *test* emails being sent to real people.



---
### Callable objects
Any object can be made *callable* by giving it a `__call__()` method that accepts the *required* *arguments*.

```python
class Repater2:
	def __init__(self):
		self.counter = 0
	
	def __call__(self, timer: float) -> None:
		self.counter += 1
		format_time(f"Called four: {self.counter}")
```


- Different kind of callable objects:
	-  Python *functions*, build with the `def` statement. and ordinary *functions* are *stateless*.
	- **Callable objects** is instances of a class with `__call__()` method. *callable* objects can be *stateful*.


---
## File I/O
*OS* represent *file* as *sequence* of *bytes* , not text.
Python `open()` function is used to open *OS* file  and return a python *file* object.

> All programming languages have to talk to *OS*  using the same *system calls*. 

- `read()` method buffer all content of file  in memory.
- `readline()` method return single line from file.
- `readlines()` method return list of *lines* like read method this is not safe
- In *binary* file don't have new line character `\n` we give number of the *bytes* to read 


### Placing it in context
We need close file after finished work with files for that we can use `try/except/finaly` or *context manager* in files.

```python
source_path = Path("requirements.txt")
with source_path.open() as source_file:
	for line in source_file:
		print(line, end='')

```

- For implement *context manager* in *class* must define `__enter__()` and `__exit__()` .
```python 
from typing import List, Optional, Type, Literal
from import TracebackType

class StringJoiner(List[str]):

	def __enter__(self) -> "StringJoiner":
		return self
		
	def __exit__(
		  self,
		  exc_type: Optinal[Type[BaseException]],
		  exc_val: Optional[BaseException],
		   exc_tb: Optional[TracebackType]
		   ) -> Literal[False]:
		self.result = "".join(self)
		return exc_type == StopIteration
```


- `@contextmanager` *decorator* is used to add some features around this function to make it work like a *context manager* class definition and doesn't have *overhead* of the *class* that define `__enter__` and `__exit__`

```python
from contextlib import contextmanager
from typing import List, Any, Iterator

class StringJoiner2(List[str]):
	def __init__(self, *args: str) -> None:
		super().__init__(*args)
		self.result = "".join(self)

@contextmanager
def joiner(*args: Any) -> Iterator[StringJoiner2]:
	string_list = StringJoiner2(*args)
	try:
		yield string_list
	finally:
		string_list.result = "".join(string_list)
```

---

### Functional Programming
For *functional design*, we're interested in *functions* to *transform* objects. A *functional design* can follow *mathematical* practices closely.

- We want to *splitting data* in case study with functional idea:
	- A **function based** on the *"Provide Training Data"* use case would transform source data into two *collections* of *samples*, a *training set* and a *testing set*. We'd like to avoid placing items in the *testing set* that are exact matches for items in the *training set*, creating some *constraints* on this *process*. We can think of this as a *mapping* from a `KnownSample` to a `TestingKnownSample` or a `TrainingKnownSample`.

	- A **function based** on the *"Set Parameters and Test Classifier"* use case would *transform* a `Hyperparameter` (the *k* value and the *distance* *algorithm*) and the *testing set* of *samples* into a *quality score*. We can think of this as a *mapping* from `TestingKnownSample` to a correct or incorrect *classification*, and a *reduction* to a single value showing the number correct out of the number of *tests*.

	-  A **function based** on the *"Make Classification Request"* use case would *transform* a `Hyperparameter` (the *k* value and the *distance algorithm*) and a *single* sample into a *classification* result.


-  The `TestingKnownSample` and the `TrainingKnownSample` classes have very minor differences. They don't introduce new attributes or methods. Here are the differences:

	- `TrainingKnownSample` *instances* are never used for *classification*.

	- `TestingKnownSample` and `UnknownSample` *instances* are used for *classification* and *testing*. We'll create a `ClassifiedKnownSample` object from a `TestingKnownSample` object by *repackaging* the `KnownSample` *instance* into a new *container*. This creates a more consistent set of *definitions*.

```python
def training_80(s: Sample, i: int) -> bool:
	returning i % 5 != 0

def training_75(s: Sample, i: int) -> bool:
	returning i % 4 != 0
	
def training_63(s: Sample, i: int) -> bool:
	returning i % 3 != 0
	

TraningList = List[TraningKnownSample]
TestingList = List[TestingKnownSample]

def partition(
	samples: Iterable[KnownSample],
	rule: Callable[[KnownSample, int], bool]
) -> Tuple[TraningList, TestingList]:

	training_samples = [
		TrainingKnownSample(s)
		for i, s in enumarate(samples) if rule(s, i)
	]
	testing_samples = [
		TestingKnownSample(s)
		for i, s in enumarate(samples) if not rule(s, i)
	]
	
	return training_samples, testing_samples
```

- This example don't *check* for duplicates between *testing samples* and *training samples*
```python
from collections import defaultdict, Counter

def partition_1p(
	samples: Itreable[KnownSample],
	rule: Callable[[KnownSample, int], bool],
) -> Tuple[TraninigList, TestingList]:
	pools: defaultdict[bool, list[KnownSample]] = defaultdict(list)
	partition = ((rule(s, i), s) for i, s in enumerate(samples))
	
	for usage_pool, sample in partition:
		pools[usage_pool].append(sample)
	
	traning = [TrainingKnownSample(s) for s in pools[True]]
	testing = [TestinggKnownSample(s) for s in pools[False]]
	
	return training, testing
```