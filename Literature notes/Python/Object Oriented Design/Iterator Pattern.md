---
Created Date: 2026-05-19
tags:
  - python
  - architecture
  - programming
Next: "[[Common Design Patterns]]"
---
---
## What we Learn
- What is design patterns are
- The iterator protocol one of the most powerful design patterns
- List, set, and dictionary comprehensions
- Generator functions, and how they build on other patterns

---
## Design pattern
 **Design patterns** are applied to *solve* a *common problem* faced by developers in some specific *situation*. The **design pattern** is a suggestion as to the ideal *solution* for that *problem*, in terms of *object-oriented design*. What's central to a *pattern* is that it is reused often in unique contexts.


---
## Iterators
In typical *design pattern* parlance, an *iterator* is an object with a `next()` method and a `done()` *method*; the latter returns *True* if there are no items left in the *sequence*.

```python
while ont iterator.done():
	item = iterator.next()
	# somthing do with the item
```


### The Iterator protocol
At the foundation, any *Collection* class definition must be *Iterable*. To be *Iterable* means implementing an `__iter__()` *method*; this method creates an *Iterator object*.
As mentioned, an *Iterator* class must define a `__next__()` *method* that the for *statement* (and other features that support *iteration*) can call to get a new element from the *sequence*. In addition, every *Iterator class* must also fulfill the *Iterable interface*.

```python
from typing import Iterable, Iterator

class CapitalIterable(Iterable[str]):
	def __init__(self, string: str) -> None:
		self.string = string
	
	def __iter__(self) -> Iterator[str]:
		return CapitalIterator(self.string)

class CapitalIterator(Iterator[str]):
	def __init__(self, string: str) -> None:
		self.words = [w.capitalize() for w in string]
		self.index = 0
	
	def __next__(self) -> str:
		if self.index == len(self.words):
			raise StopIteration()
		word = self.words[self.index]
		self.index += 1
		return word
```

- another way interact with *iterator* is `iter()` method :
```sh
>>> iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')
>>> iterator = iter(iterable)
>>> while True:
... try:
	... print(next(iterator))
... except StopIteration:
	... break
...
```

---
- **Iterable:** iterable is an *object* with *elements* that can be *iterated* over , and these *elements* can looped over *multiple* even at a same time
- **Iterator:** specific location in that *iterable* *object*  every time call `next()` on iterator update internal *state*
---
- **Comprehensions** are simple, but *powerful*, *syntaxes* that allow us to *transform* or *filter* an *iterable object* in as *little* as one *line of code*. The resultant object can be a perfectly normal *list*, *set*, or *dictionary*, or it can be a *generator* expression that can be *efficiently* consumed while keeping just one *element* in *memory* at a *time*.
---
