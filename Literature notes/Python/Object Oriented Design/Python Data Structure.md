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
class Stock(NamedTuple):
	symbol: str
	current: float
	high: float
	low: float

stock = Stock("Apple", 123.3, 137.98, 53.15) 

# Usage
stock[2] # 137.98
stock.high # 137.98
symbol, current, high, low = stock # unpacking 
```


>[!NOTE] 
> Names are provided in *class-level* but we are *not*  create *class-level* attributes the *class* names are used to *build* the` __init__()` method . this work do in **metaclasses**.



- **tuples** can contain *mutable* data but in this state we can't use `hash()` for tuple.
```python
t = ("Relayer", ["Gate of Delirium", "Sound Chaser"])
t[1].append("To be over")

hash(t) # TypeError
```



- We can add *method*  to named tuple:
```python
class Stock(NamedTuple):
	symbol: str
	current: float
	high: float
	low: float
	
	@property
	def midle(self) -> float:
		return (self.high + self.low) /2


stock = Stock("Apple", 123.3, 137.98, 53.15) 
stock.midle # 95.565
```

---
## Dataclassess
*dataclasses* let us define *ordinary* objects with a *clean* syntax for specifying *attributes*.
The *dataclass* function is applied as a class *decorator*, using the `@` *operator*.
Names are provided in _class-level_ but we are _not_ create _class-level_ attributes the _class_ names are used to _build_ the `__init__()` method .

```python

@dataclass
class Stock:
	symbol: str
	current: float
	high: float
	low: float
```

- By default *dataclass* implement `__eq__` and `__rper__`
- We can set default value for *attributes*
-  If we want to compare `__qt__` , ... we can set `@dataclass(order=Trure)`
-  For set dataclass *Immutable* like *NamedTuple* we do `@dataclass(frozen=True, order=True)`
- we have  `__post_init__()` for after `__init__` call for some use case.


---
## Dictionaries
- Useful containers that allow us to *map* objects directly to other objects.
- Dictionary use *hash* of *key* to locate the *values* , *keys* must be *immutable* .
- If *key* not in *dictionary* it *raise* **KeyError** to handle that.
- `setdefault()` method if *key* exist return *value* of key if not exist set *key* with *value* and return *value*

>[!IMPORTANT]
>We can, however, *create* our own *class* of *objects* that are both *mutable* and provide a *hash value*; this is *unsafe* because a change to the *object's state* can make it *difficult* to find the *key* in the **dictionary**.


 
