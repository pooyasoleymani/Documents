---
Created Date: 2026-05-18
tags:
  - python
  - architecture
  - programming
Next: "[[Iterator Pattern]]"
---
---
## What we Learn
- The *complexities* of *strings*, *bytes*, and *byte arrays*
- The ins and outs of *string* *formatting*
- The *mysterious* **regular expression**
- How to use the `pathlib` *module* to *manage* the `filesystem`
- A few ways to *serialize* data, including *Pickle* and *JSON*


---
## Strings
In python **string** is *immutable* sequence of **Unicode** *characters* (*UTF-8*) 

- **The important rule is this:** we *encode* our *characters* to create *bytes*; we *decode* *bytes* to recover the *characters*.
-  The `b""` *prefix* tell us these are *bytes*

---
### String manipulation
Like other *sequences*, **strings** can be *iterated* over (character by *character*), *indexed*,
*sliced*, or *concatenated*. The *syntax* is the same as for *lists* and *tuples*.

Be careful with the `isdigit()`, `isdecimal()`, and `isnumeric()` methods, as they are more nuanced than we would expect.

```python
s = "hello world"
s1 = s.split(" ") # ["hello", "world"]
s2 = "#".join(s1) # "hello#world"
```

---
### String formatting
Python has powerful *string* *formatting* and *templating*  *mechanisms*   , `f""` prefix one of them that called *f-string*.

---
### Escape braces
When we want to use `{` or `}` in *f-string* must use double braces .
```python
template = f"public class {classnema} {{...}}"
```

---
### Making it look right
we can format output string with `:` after name or content in *braces* 
```python
speed = 5
name = "Test Distance"
fuel_per_hr = 2.2
d = 4
print(f"{'leg':16s} {'dist':5s} {'time':4s} {'fuel':4s}")
print(f"{name:16s} {d:5.2f} {d/speed:4.1f} {d/speed*fuel_per_hr:4.0f}") 
```

---
### Custom formatters
we can use the specifiers used in the `datetime.strftime()` function, as follows:
```python 
import datetime
important = datetime.datetime(2019, 10, 26, 13, 14)
print(f"{important:%Y-%m-%d %I:%M%p}") # 2019-10-26 01:14PM
```


---
### Strings are Unicode
If you get a *string* of *bytes* from a *file* or a *socket*, for example, they won't be in *Unicode*. They will, in fact, be the built-in type *bytes*. *Bytes* are *immutable* *sequences* of...well, *bytes*. *Bytes* are the basic *storage* *format* in *computing*. They represent *8 bits*, usually described as an *integer* between *0* and *255*, or a *hexadecimal* equivalent between `0x00` and `0xFF`. *Bytes* don't represent *anything* specific; a *sequence* of *bytes* may *store* *characters* of an *encoded* *string*, or *pixels* in an *image*, or represent an *integer*, or part of a *floating-point* value.

```python
print(list(map(hex, b'abc'))) # ['0x61', '0x62', '0x63']
print(list(map(bin, b'abd'))) # ['0b1100001', '0b1100010', '0b1100011']
```


>[!NOTE]
>Many *I/O* operations only know how to deal with *bytes*, even if the *bytes* *object* is the *encoding* of *textual* data. It is therefore vital to know how to *convert* between *bytes* values and *Unicode* *str* values.



---
### Decoding bytes to text
If we have an *array* of *bytes* from somewhere we can convert it to *Unicode* using the `decode()` on *bytes class*.
common ones include `ASCII`, `UTF-8`, `latin-1`, and `cp-1252`. Of these, `UTF-8` is one of the most commonly used.
The `\x` *character* **escapes** within the *byte string*, and each says the next two characters represent a *byte* using *hexadecimal digits*.

```python
characters = b'\x63\x6c\x69\x63\x68\xc3\xa9' #  --> b'clich\xc3\xa9'
characters.decode('utf-8') # In UTF-8 --> 'cliché'
characters.decode('iso8859-5') #  --> 'clichУЉ'
characters.decode('utf-8') # In UTF-8 --> 'Ä%ÑÄÇCz'
```


---
### Encoding text to bytes
The flip side of converting *bytes* to *Unicode* is situations where we convert outgoing *Unicode* into *byte* *sequences*. This is done with the `encode()` method on the *str class*, which, like the `decode()` method, requires an *encoding* *name*.

The *exception* in the last case is not always the desired behavior; there may be cases where we want the unknown *characters* to be *handled* in a different way.

- The *encode* method takes an *optional string* argument named *error* that can define how such characters should be handled.
	- **strict:** When a *byte* sequence is encountered that does not have a *valid* representation in the requested *encoding* an *exception raised*.
	- **replace:** *Character* is replaced with a different *character*.
	- **ignore:** Discards any *bytes* it doesn't understand.
	- **xmlcharrefreplace:** Create an **XML** entity representing the *Unicode* character.

- We can get default *encoding* with `sys.getdefaultencoding()`.


---
### Mutable byte strings
`bytearraye` built-in behaves something like a *list* . 
*constructor*  for the class can accept a *bytes object*  to initialize.

- `ord()` function convert *character* to *integer*.


---
## Regular Expressions
In the real world, *string-parsing* in most programming languages is handled by **regular expressions**

Some common problem that *regex* can solve them:
- Is this string a *valid* URL?
- What is the date and time of all warning messages in a log file?
- Which users in `/etc/passwd` are in a given group?
- What username and document were requested by the URL a visitor typed?

---
### Matching Pattern
```python
import re
from typing import Pattern, Match

def matchy(pattern: Pattern[str], text: str) -> None:
	if match := re.match(pattern, text):
		print(f"{pattern=!r} matches at {match=!r}")
	else:
		print(f"{pattern=!r} not found in {text=!r}")
```


---
## Filesystem paths
Most *operating systems* provide a `filesystem`, a way of *mapping* a *logical abstraction* of *directories* (often depicted as folders) and *files* to the *bits* and bytes stored on a *hard drive* or another *storage device*.
Programmer interact with `filesystem`  with *system calls* .
- In python `os.path` module use for interact with *OS* *Filesystem* interface
- `pathlib` module is *object-oriented* representation of *paths* and *files*.

```python
from pathlib import Path
path = Path("/Users") / "dusty" / "subdir" / "file.ext"
```

- *Example*: this code counting number of code exclude comments and white spaces:
```python
from pathlib import Path  
from typing import Callable  
  
  
def scan_python_1(path: Path) -> int:  
    sloc = 0  
    with path.open() as source:  
        for line in source:  
            line = line.strip()  
            if line and not line.startswith("#"):  
                sloc += 1  
    return sloc  
  
def count_sloc(path: Path, scanner: Callable[[Path], int]) -> int:  
    if path.name.startswith("."):  
        return 0  
    elif path.is_file():  
        if path.suffix != ".py":  
            return 0  
        return scanner(path)  
    elif path.is_dir():  
        count = sum(  
            count_sloc(name, scanner) for name in path.iterdir()  
        )  
        return count  
    else:  
        return 0
```


more methods and attributes of a Path object:

- `.absolute()` returns the *full path* from the *root* of the `filesystem`. This helps show where *relative paths* came from.
-  `.parent` returns a *path* to the *parent directory*.
- ` .exists() `checks whether the file or *directory exists*.
-  `.mkdir()` creates a *directory* at the current path. It takes *Boolean* *parents* and `exist_ok` arguments to indicate that it should *recursively* create the directories if necessary and that it shouldn't raise an *exception* if the directory *already exists*.


---
## Serializing objects
*encoding* and *decoding* is also described as **serializing** and **deserializing**.

### Pickle module
The Python **pickle** module is an *object-oriented* way to store object *state* directly in a *special storage format*. It essentially *converts* an *object's state* (and all the *state* of all the *objects* it holds as *attributes*) into a *series* of *bytes* that can be *stored* or *transported* however we see fit.
```sh
>>> import pickle
>>> some_data = [
... "a list", "containing", 5, "items",
... {"including": ["str", "int", "dict"]}
... ]
>>> with open("pickled_list", 'wb') as file:
... pickle.dump(some_data, file)

>>> with open("pickled_list", 'rb') as file:
... loaded_data = pickle.load(file)

>>> print(loaded_data)
['a list', 'containing', 5, 'items', {'including': ['str', 'int',
'dict']}]

>>> assert loaded_data == some_data
```

> If we use `id()` realized that they are not same objects


### Customizing pickles
With most common *Python* objects, *pickling* just works. Basic *primitive* *types* such as *integers*, *floats*, and *strings* can be *pickled*, as can any *container* *objects*, such as *lists* or *dictionaries*, provided the contents of those *containers* are also *picklable*.

##### Unpicklabel attribute
it has something to do with *dynamic attribute* values subject to change. For example, if we have an open *network* `socket`, `open file`, running `thread`, `subprocess`, `processing pool`, or `database` *connection stored* as an *attribute* on an *object*, it will not make sense to *pickle* these *objects*.

```python
from threading import Timer
import datetime
from urllib.request import urlopen


class URLPolling:
	def __init__(self, url: str) -> None:
		self.url: url
		self.content = ""
		self.last_update: datetime.datetime
		self.timer: Timer
		self.update()
	
	def update(self) -> None:
		self.content = urlopen(self.url).read()
		self.last_update = datetime.datetime.now()
		self.schedule()
	
	def schedule(self) -> None:
		self.timer = Timer(3600, self.update)
		self.timer.setDaemon(True)
		self.timer.start()
```

```sh
>>>import pickle
>>>poll = URLPooling("http://dusty.phillips.codes")
>>>pickle.dupms(poll)
Trackback 
...
TypeError: cannot pickle "_thread.lock" object
```

When pickle tries to serialize an object, it simply tries to store the state, the value of the object's `__dict__` attribute; `__dict__` is a dictionary mapping all the attribute names on the object to their values. Luckily, before checking `__dict__`, pickle checks to see whether a `__getstate__()` method exists.

```python
def __getstate__(self) -> dict[str, Any]:
	pickleable_state = self.__dict__.copy()
	if "timer" in pickleable_state:
		del pickleable_state["time"]
	return pickleable_state

# for loads() method we must define __setstate__()

def __setstate(self, pickleable_state: dict[str, Any]) -> None:
	self.__dict__ = pickleable_state
	self.schedule()
```


This is a *common pattern* for working with *pickled* *objects* that have **dynamic state** that must be *recovered*.


---
### Serializing objects using JSON
