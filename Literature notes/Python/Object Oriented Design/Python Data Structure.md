---
Created Date: 2026-05-13
tags:
  - python
  - architecture
  - programming
Next: "[[The Intersection of Object\x02Oriented and Functional \r

  Programming]]"
---
---
## What We learn
- *Tuples* and *named tuples*
- *Dataclasses*
- *Dictionaries*
- *Lists* and *sets*
- Three types of *queues*

---
## Empty Objects
we've *extended* in every *class* we have created: the *object*.
We can *instantiate* but we can't set attributes on an *object* because this make new memory allocation for that we write *class* 

>[!NOTE]
> It is possible to restrict *arbitrary properties* on our own *classes* using` __slots__`

---
## Tuple and Named Tuple
*Tuples* are *objects* that can *store* a *specific* *number* of other *objects* in *sequence*. They are *immutable*, meaning we can't *add*, *remove*, or *replace* *objects* on the fly.

### Named Tuple via typing.NamedTuple
The way of create *immutable* grouping of data values. When we want to create *named tuple* we are creating a *subclass* of `typing.NamedTuple` , we don't need to write an `__init__()` method its created for us. *class* have a number of the *methods* including `__hash__`, `__repr__`, `__eq__` this will be based on the *generic tuple* with add benefit of *names* for the various *item*.

```python
class stock(NamedTuple):
	symbol: str
	current: float
	high: float
	low: float

stock = 
```