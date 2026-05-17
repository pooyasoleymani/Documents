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
