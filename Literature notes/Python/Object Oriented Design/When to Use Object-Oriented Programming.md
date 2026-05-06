---
Created Date: 2026-05-06
tags:
  - python
  - architecture
  - programming
---
---
## What We Learn
- How to recognize objects
- Data and behaviors, once again
- Wrapping data behaviors using properties
- The Don't Repeat Yourself principle and avoiding repetition

---
## Treat Object as Object
We separate *objects* in our *problem domain* a special *class*.
*Identifying objects* is very important task in *object-oriented-analysis*.

>[!NOTE] *Remember*
>*Object* are things that have both *data* and *behaviors*.

- If we want to create polygon object to calculate distance we can implement this in problem in function
```python
polygon = [(1, 1), (1, 2), (2, 2), (2, 1)]

def distance(p1, p2):
	return hypot(p1[0] - p2[0], p1[1] - p2[1])

def perimeter(polygon):
	pairs = zip(polygon, polygon[1:]+polygon[:1])
	 return sum(
		distance(p1, p2) for p1, p2 in pairs
	)
```

- If we want to add some method and attribute best practice is use object-oriented for this scenario
```python
from __future__ import annotations
from math import hypot
from typing import Tuple, List

class Piont:
	def __init__(self, x: float, y: float) -> None:
		self.x = x
		self.y = y
	
	def distance(self, other: "Point") -> float:
		return hypot(self.x - other.x, self.y - other.y)

Pair = Tuple[float, float]
Point_or_Tuple = Union[Point, Pair]

class Polygon:
	def __init__(self, vertics: Optional[Iterable[Point_or_Tuple]] = None) -> None:
		self.vertics: List[Point] = []
		if vertics:
			for point_or_tuple in vertics:
				self.vertics.append(self.make_point(point_or_tuple))
	
	@staticmethod
	def make_point(item: Poin_or_tuple) -> Point:
		return item if isinstance(item, Point) else Point(*item)
```


---
## Adding behaviors to class data with properties

- One of the most important things in *object-oriented design* is separation between *data*, and **behavior**.
- For add *getter* and *setter* to class we can use *property* function , this function have act like *proxies*.
```python
class Color:
	def __init__(self, rgb: int, name: str) -> None:
		if not name:
			raise ValueError("name can't be empty")
		self._name = name
		self._rgb = rgb
	
	def _set_name(self, name: str) -> None:
		if not name:
			raise ValueError("name can't be empty")
		self._name = name
	
	def _get_name(self) -> str:
		return self._name
		
	name = property(_get_name, _set_name)
```


- we can set *delete* and *document* function in *property*   
- **Decorators** one of way that we can use *property*
- We can use *properties* for *lazy attributes*, where we want to defer the computation because it's *costly* and *rarely* needed
```python
class WebPage:
	def __init__(self, url: str) -> None:
		self.url = url
		self._content: Optional[bytes] = None
		
	@property
	def content(self):
		if self._content is None:
			print("retriving new page")
			with urlopen(self.url) as response:
				self._content = response.read()
		return self._content
```

