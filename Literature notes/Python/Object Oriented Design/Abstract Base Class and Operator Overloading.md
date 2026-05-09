---
Created Date: 2026-05-09
tags:
  - python
  - architecture
  - programming
---
---
## What We Learn?
1. Creating *Abstract* base class 
2. *ABC's* and type hints
3. The *collections.abc* module
4. Creating our base class 
5. Demystifying the magic – looking under the hood at the implementation of an *ABC*
6. *Operator overloading*
7. Extending *built-ins*
8. *Metaclasses*

---

**Concrete Class:** A class with complete  definition of attribute and methods.

---

- Two in *python* approaches to define similar things:
	-  **Duck Typing:** When we define two *class* with same *attribute* and *methods* , instance of two class can be used interchangeably. 
	- **Inheritance:** When two *class* definition have common aspects, a *subclass* ca share common features of a *superclass*.

---

**Abstract Class:** Abstract class can't use directly and *instantiate* but can use to *inheritance* to create *concrete class*.

---

## Creating an abstract base class
One of the most use case of *ABC* base class is *documentation*.
*abc.ABC* class introduce [[metaclass]]  a class to use create *concrete* class this *metaclass* by default is **type** in python.

- We can see abstract methods with `__abstractmethods__`  *magic method* .
```python

class MediaPlayer(ABC):
	@abstractmethod
	def play(self) -> None:
		...
		
	@abstractmethod
	def ext(self) -> None:
		...
```

---
## ABC's collections
standard library base classes is live in *collections* library
One of base class in *collections*  in *Container* this class consist of one abstract method `__contain__` built-in type like *set*, *list*, *dict* implements this method this method used in `in` operator.

```python
class OddIntegers:
	def __contains__(self, x: int) -> bool:
		return x % 2 != 0


odd = OddIntegers()

1 in odd # True
2 in odd # False
```


- Python *duck typing* is part of `isinstance()` and `issubclass()` with `__instancecheck__()` and `__subclasscheck__()` magic method and *ABC* class can provide a `__subclasshook__()` method which used by `__subclasscheck__()` method to *assert* that a give class is proper subclass of abstract base class.

---
## Abstract base class ant type hints
**Generic classes** and **abstract base classes** are not the same thing. The two concepts
overlap, but are distinct:

- *Generic classes* have an *implicit* relationship with *Any*. This often needs to be narrowed using type parameters, like`list[int]`. The list class is concrete, and when we want to extend it, we'll need to plug in a class name to replace the *Any* type. The Python *interpreter* does not use *generic class* hints in any way; they are only checked by *static analysis* tools such as *mypy*.

-  *Abstract classes* have *placeholders* instead of one or more *methods*. These *placeholder* methods require a design decision that supplies a *concrete implementation*. These *classes* are not completely *defined*. When we *extend* it, we'll need to provide a *concrete method implementation*. This is checked by *mypy*. That's not all. If we don't provide the *missing methods*, the interpreter will *raise* a *runtime exception* when we try to create an instance of an *abstract class*.

---
### Protocol
*Protocol* is another of abstract class concepts , when two *class* have same batch of the *methods* they have same *protocol*. One of *duck typing* checks.

*Example:* immutable classes implements `__hash__()` method list `set`, `tupple` and `dict` these are **Hashable Protocols** class. `list` is not **Hashable Protocol** class and we can use `dict[list[int], list[int]]` type hint.


---

### The coloctions.ABC modules
This module provide the *abstract base* class definitions for pythons *built-in collections*.

- We can use this class to: 
	1. build our *data structure*  
	2. use for *type hints* for specific *data structure*

