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
- If we want to implement the `__gt__`, `__ne__`, `__ge__`, `__le__`, `__eq__` best practice is implement just `__lt__` and `__eq__` and use `@total_ordering` *decorator* in top of *dataclass*.


---
## Dictionaries
- Useful containers that allow us to *map* objects directly to other objects.
- Dictionary use *hash* of *key* to locate the *values* , *keys* must be *immutable* .
- If *key* not in *dictionary* it *raise* **KeyError** to handle that.
- `setdefault()` method if *key* exist return *value* of key if not exist set *key* with *value* and return *value*

>[!IMPORTANT]
>We can, however, *create* our own *class* of *objects* that are both *mutable* and provide a *hash value*; this is *unsafe* because a change to the *object's state* can make it *difficult* to find the *key* in the **dictionary**.


 
### Dictionary use cases
- We can have dictionaries where all the values are different *instances* of *objects* with the same *type*.
- The second *design* is to have each *key* represent some aspect or *attribute* of a single *object*; the values often have *distinct* *types*. We may, for example, represent a stock with `{'name': 'GOOG', 'current': 1245.21, 'range': (1252.64, 1245.18)}`

---
## default dict
In **defaultdict** don't need use `setdefault()` if key not exist

```python
def letter_frequency(sentence: str) -> dic[str, int]:
	frequencies: dict[str, int] = {}
	for latter in sequence:
		frequency = frequencies.setdefault(latter, 0)
		frequencies[latter] = frequency + i
	return frequencies
	

def letter_frequency(sentence: str) -> defaultdict[str, int]:
	frequencies: defaultdict[str, int] = defaultdict(int)
	for latter in sequence:
		frequencies[latter] = frequency + i
	return frequencies
```

- We can give *class* to *defaultdict* constructor:
```python
@dataclass
class Prices:
	current: float = 0.0
	high: float = 0.0
	low: float = 0.0

portfilo = collection.defaultdict(Prices)
portfilo["GOOG"]
portfilo["APPL"] = Prices(current=122.25, high=137.98, low=53.15)
pprint(portfilo) 
#  defaultdict(<class 'dc_stocks.Prices'>, {'AAPL': Prices(current=122.25, high=137.98, low=53.15), 'GOOG': Prices(current=0.0, high=0.0, low=0.0)})
```

---
## Counter
The **Counter** object behaves like a beefed-up *dictionary* where the keys are the items being counted and the values are the quantities of such items. One of the most useful functions is the `most_common()` method. It returns a list of `(key,count) `tuples in descending order by the *count*.

---
## Lists
In Python, lists should normally be used when we want to store several *instances* of the same *type* of *object*; *lists* of *strings* or *lists* of numbers. We'll often use a type *hint* `list[T] `to specify the type, `T,` of object kept in the *list*, for example, `list[int] `or `list[str].`


>*Don't* use *lists* for *collecting* **different attributes** of individual items. *Tuples*, *named tuples*, *dictionaries*, and *objects* would all be more *suitable* for *collecting* different kinds of *attribute values*.


