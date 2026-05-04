---
Created Date: 2026-02-27
tags:
  - python
  - architecture
  - programming
---
---
## What We learn
- Python's type hints
- Create classes and instantiating objects in python
- Organizing classes into packages and modules
-  How to suggest that people don't clobber an object's data, invalidating the internal state
-  Working with third-party packages available from the Python Package Index, PyPI

---
#### Two core rules of how python objects work ?
1. Everything in *python* is an *object*
2. Every object is defined by being an instance of at least one class

---

### Type Hints
Python is nothing to prevent to use specific class or type for function parameter 

```python 
def odd(x):
	return x % 2 == 0

odd("hello world") # raise TypeError 
```

-  For decrees wrong use types in python offer **type hints**
```python 
def odd(x: int) -> bool: ...
```

#### Mypy
The **mypy** tool is commonly used to *check* the *hints* for consistency.

```shell
mypy –strict src/bad_hints.py


src/bad_hints.py:12: error: Function is missing a return type
annotation
src/bad_hints.py:12: note: Use "-> None" if function does not return a
value
src/bad_hints.py:13: error: Argument 1 to "odd" has incompatible type
"str"; expected "int"
```
---


- For test we can use **assert** in code 
```python 
class Point:
	def move(self, x: int, y: int):
		self.x = x
		self.y = y 
	def reset(self):
		self.x = 0
		self.y = 0
	def calc_distance(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

point1 = Point()
point1.move(4, 3)

assert point1.calc_distance() == 5, "distance most be 5"

```


---
### Docstring
Python is self-document program languages but we can with `"""` or `'''` write *docstring*
and *doctest*

```python
class Point:
	'''
	Point class reperesent point to two demensional gemetric coordinates
	>>> p_0 = Point()
	>>> p_1 = Point(3, 4)
	>>> p_0.calc_distance()
	5.0
	'''
	def __init__(self, x: int = 0, y: int = 0) -> None:
	'''
		Initialize the position of a new poit.
		:param x: int x-coordinate
		:param y: int y-coordinate
	'''
		self.x = x
		self.y = y
		
	def move(self, x: int, y: int) -> None:
		'''
			Move the point to a new location in 2D space.
			:param x: int
			:param y: int
		'''
		self.x = x
		self.y = y 
	
	def reset(self) -> None:
	'''
		Reset the point back to : 0, 0
	'''
		self.x = 0
		self.y = 0
	
	def calc_distance(self) -> float:
	'''
		Calaculate the distance from this poinnt from 0, 0 point.
		:param: None
		:return float distance
	'''
		return math.sqrt(self.x ** 2 + self.y ** 2)
```

```sh
python -m doctest main.py
```


---

## Modules and Packages
1. *Modules* are Python files.
2. *Package* is collection of *modules* in folders.

>for *import*  modules use import and name of the module without *suffix(.py)*

- When we use `*`  for import every things we use `__all__` list in module. 
```python
from module import *
```

---
### Organizing Modules
For tell *python* that a folder is a *package* we need to create a `__init__.py` into the each folder if this file not exist we can't *import* that package.

#### Absolute import
If use *full path* of package to *import* that *package* 

```python 
from ecommerce.products import Product
```

---
#### Relative import 
If we want to work in *same package* we can use relative import 
```python 
from .database import Database
from ..contact.email import send_email
```

---
#### `__ini__.py`  is entry of contact to that module .
---
#### Package as Whole
When we want to access to a *variable* or *function* from one *module* in other place we can put that in `__init__.py` file then every one can *import* that

```python
# in ecommerce/__init__.py
from .database import db
#########################################
from ecommerce import db # instead of from ecommerce.database import db
```

---
#### Organizing our code in modules
*Module-level* code *executed* immediately at the time it is *imported*.
if we have share variable for use in other modules we can create function initialize to create that object or *singleton* 

```python
db: Optional[Database] = None

def initialize_database(connection: Optional[str] = None) -> None:
	global db
	db = Database(connection)


def get_database(connection: Optional[str] = None) -> Database:
	global db
	if not db:
		db = Database(connection)
	return db
```


---

### Access to Data 
In python interpreter has no rule to prevent to access of variable of class we can use `_` before variable to show that variable is private and we can use `__` name mangling for private attributes that need extra work for access ( `_<class name>__X`).



---
>[!IMPORTANT] **A Question We must always ask about class definitions**
> - Is there any change in *behavior* that goes with the change in *state*?
> - What *class* has *responsibility* for making this *state change*?


---
#### Forward Reference
When a *class* is defined *later* in the *file*, any reference to the yet-to-be-defined class is **forward reference**.
