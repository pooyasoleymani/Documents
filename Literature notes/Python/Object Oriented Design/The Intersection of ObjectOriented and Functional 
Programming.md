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
We'll often have to use a typing.Union hint to show that a parameter can have values from `Union[int, str]`. This definition clarifies the alternatives so *mypy* can confirm that we're using the overloaded function *properly*.

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