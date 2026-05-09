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
