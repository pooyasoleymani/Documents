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

