---
Created Date: 2026-05-09
tags:
  - python
  - architecture
  - programming
Next: "[[Python Data Structure]]"
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

**Concrete Class:** A class with complete definition of attribute and methods.

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


- Python *duck typing* is part of `isinstance()` and `issubclass()` with `__instancecheck__()` and `__subclasscheck__()` magic method and *ABC* class can provide a `__subclasshook__()` method which used by `__subclasscheck__()` method to *assert* that a give class is proper subclass of *abstract base* class.

---
## Abstract base class and type hints
**Generic classes** and **Abstract Base Classes** are not the same thing. The two concepts
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


- Create *look-up dictionary* a *concrete Mapping* implementation need below implements:

	- The *Sized abstraction* requires an implementation for the` __len__()` method. This lets an instance of our *class* respond to the `len() `function with a useful answer.

	- The *Iterable abstraction* requires an *implementation* for the` __iter__()` method. This lets an *object* work with the for statement and the `iter()` function.

	- The *Container* *abstraction* requires an *implementation* for the `__contains__()` method. This permits the in and not in operators to work.

	-  The *Collection abstraction* combines *Sized*, *Iterable*, and *Container* without introducing additional *abstract methods*.

	-  The *Mapping abstraction*, based on *Collection*, requires, among other things, `__getitem__()` for `[]`  operator ,` __iter__(),` and `__len__()`. It has a default definition for `__contains__()`, based on whatever `__iter__()` method we provide. The *Mapping* definition will provide a few other methods, also.


- Implement *Immutable  Mapping* :
```python
import bisect

BaseMapping = Mapping[Comparable, Sample]  
class LookUp(BaseMapping):  
    @overload  
    def __init__(self, source: BaseMapping) -> None:  
        ...  
    @overload  
    def __init__(self, source: Iterable[tuple[Comparable, Any]]) -> None:  
        ...  
    def __init__(  
            self,  
            source: Union[Iterable[tuple[Comparable, Any]], BaseMapping, None] = None,  
    ) -> None:  
        sorted_pairs: Sequence[Tuple[Comparable, Any]]  
        if isinstance(source, Sequence):  
            sorted_pairs = sorted(source)  
        elif isinstance(source, Mapping):  
            sorted_pairs = sorted(source.items())  
        else:  
            sorted_pairs = []  
        self.keys_list = [p[0] for p in sorted_pairs]  
        self.value_list = [p[1] for p in sorted_pairs]  
  
    def __len__(self) -> int:  
        return len(self.keys_list)  
    def __iter__(self) -> Iterator[Comparable]:  
        return iter(self.keys_list)  
    def __contains__(self, key: object) -> bool:  
        index = bisect.bisect_left(self.keys_list, key)  
        return key == self.keys_list[index]  
    def __getitem__(self, key: object) -> Any:  
        index = bisect.bisect_left(self.keys_list, key)  
        if key == self.keys_list[index]:  
            return self.value_list[index]  
        raise KeyError(key)

```


-  These two *definitions* have distinct *type hints*. To make it clear to *mypy*, we need to provide *overloaded* method definitions. This is done with a special *decoration* from the typing module, **@overload**

- We can implement *Comparable class*
```python
class Comparable(Protocol):  
    def __eq__(self, other: Any) -> bool: ...  
    def __ne__(self, other: Any) -> bool: ...  
    def __gt__(self, other: Any) -> bool: ...  
    def __ge__(self, other: Any) -> bool: ...  
    def __le__(self, other: Any) -> bool: ...  
    def __lt__(self, other: Any) -> bool: ...
```


---


>[!IMPORTANT]
> *Abstract* gives us a *runtime* assurance that the *concrete subclass* really does implement all the required methods.


---
### Create your own abstract base class
We have two general paths to creating *classes* that are *similar*: 
1. we can leverage *duck typing* 
2. we can define *common abstractions*.

When we leverage *duck typing*, we can formalize the related types by creating a *type hint* using a *protocol* definition to *enumerate* the common *methods*, or a `Union[] `to enumerate the common types. There are an almost unlimited number of influencing factors that suggest one or the other approach. While *duck typing* offers the most *flexibility*, we may sacrifice the ability to use *mypy*. An *abstract* *base* *class* definition can be wordy and potentially *confusing*.

```python
class Die(abc.ABC):
	def __init__(self) -> None:
		self.face: int
		self.roll()
		
	@abc.abstractmethod
	def roll(self) -> None:
		...
		
	def __repr__(self) -> str:
		return f"{self.face}"
		

class D6(Die):
	def roll(self) -> None:
		self.face = random.randint(1, 6)


class Dice(abc.ABC):
	def __init__(self, n: int, die_class: Type[Die]) -> None:
		self.diec = [die_class() for _ in range(n)]
		
	@abc.abstractmethod
	def roll(self) -> None:
		...
	
	@peroperty
	def total(self) -> int:
		return sum(d.face for d in self.dice)


class SimpleDice(Dice):
	def roll(self) -> None:
		for d in self.dice:
			d.roll()
```

-  The `__init__()` method expects an integer, `n`, and the class used to create `Die` instances.
- The *type hint* is `Type[Die]`, telling *mypy* to be on the lookup for any subclass of the *abstract* base class *Die*.

-  Here another *subclass* that provides a dramatically different set of methods
```python
class YachtDice(Dice):
	def __init__(self) -> None:
		super().__init__(6, D6)
		self.saved: Set[int] = set()
	
	def saving(self, positions: Iterable[int]) -> "YachtDice"
		if not all(0 <= n < 6 for n in positions):
			raise ValueErrror("Invalid position")
		self.saved = set(positions)
		return self
	
	def roll(self) -> None:
		for n, d in enumerate(self.dice):
			if n not in self.saved:
				d.roll()
			self.saved = set()
```


---
### Demystifying the magic
Every Python class that *inherit* from *abstract* base class  *inherit* `__abstractmethods__` *froze set* and when implement every methods names are removed from set.

```python
Die.__abstractmethods__ # frozenset({'roll'})
```
---
#### What is Class?
1. A class is another with two limited *jobs*:
	1. It is *special methods* to *create* and *manage* instances of the *class*.
	2. It also a *container* for *method* definitions for *objects* of the *class*.
2. The **type** *class* is internal object that build our application *classes* . **type** *class* create our *class* and *class* build our *objects*.

---
#### What is **type** class?
The **type** class is a [[metaclass]] that responsible to create *classes* .
Every *object* is instance of the **type** .
Because **type** is a *class*  it can be *extended* .
A class **abc.ABCMeta** is *extended* **type** class to check for methods decorated with *@abstractmethod* and when we *extended* **abc.ABC** we creating new class that uses the **ABCMeta** *metaclass*.
We can see this wit `__mro__` 

```python 
class DieM(metaclass=abc.ABCMeta):
	def __init__(self) -> None:
		self.face: int
		self.roll()
		
	@abc.abstractmethod
	def roll(self) -> None:
		...
```

- When we used **metaclass** as keyword parameter when defining the *components* that make up a class this means *extensions* to **type** will be used to create the final class *objects*.

---
## Operator overloading
Every operators in python `+ - / *` are implemented by *special methods* on *classes*. 
For example `+` operator is `__add__` and `__radd__` (reverse add) .
for check that operator we can use `A.__op__(B)` if value is `NotImlemented` we override that operator.
```python
class DDice:  
    def __init__(self, *die_class: Type[Die]) -> None:  
        self.dices: List[Die] = [dc() for dc in die_class]  
        self.adjust: int = 0  
  
    def plus(self, adjust: int) -> 'DDice':  
        self.adjust = adjust  
        return self  
  
    def roll(self) -> None:  
        for d in self.dices:  
            d.roll()  
  
    @property  
    def total(self) -> int:  
        return sum(d.face for d in self.dices) + self.adjust  
  
    def __add__(self, die_class: Any) -> 'DDice':  
        if isinstance(die_class, type) and issubclass(die_class, Die):  
            new_classes = [type(d) for d in self.dices] + [die_class]  
            new = DDice(*new_classes)  
            return new  
        elif isinstance(die_class, int):  
            new_classes = [type(d) for d in self.dices]  
            new = DDice(*new_classes).plus(die_class)  
            return new  
  
        return NotImplemented  
        
    def __radd__(self, die_class: Any) -> 'DDice':  
        if isinstance(die_class, type) and issubclass(die_class, Die):  
            new_classes = [die_class] + [type(d) for d in self.dices]  
            new = DDice(*new_classes)  
            return new  
        elif isinstance(die_class, int):  
            new_classes = [type(d) for d in self.dices]  
            new = DDice(*new_classes).plus(die_class)  
            return new  
  
        return NotImplemented

	def __mul__(self, n: Any) -> "DDice": # for * operation
		if isinstance(n, int):
			new_classes = [type(d) for d in self.dice for _ in range(n)]
			return DDice(*new_classes).plus(self.adjust)
		else:
			return NotImplemented
	def __rmul__(self, n: Any) -> "DDice":
		if isinstance(n, int):
			new_classes = [type(d) for d in self.dice for _ in range(n)]
			return DDice(*new_classes).plus(self.adjust)
		else:	
			return NotImplemented
	
#####################################################################
# Mutable object
	def __iadd__(self, die_class: Any) -> 'DDice':  
        if isinstance(die_class, type) and issubclass(die_class, Die):  
            self.dice += [die_class]   
            return self
        elif isinstance(die_class, int):  
            self.adjust += die_class 
            return self
  
        return NotImplemented
```

1. **Mutable** object implements `__iadd__` , etc and *return* `self`.
2. **Immutable** object don't implements `__iop__` and return *new* object.

---
## Extending built-ins
Python have two group of collections that we want to extended:
1. **Immutable objects:** object that after construct we can't change them like: *string*, *bytes*, *tuples* 
2. **Mutable objects:** object that we can change them like: *lists*, *dictionary* and *sets*

We want to create dictionary that reject duplicate values:
```python
from typing import Dict, cast, Any, Mapping, Iterable, Tuple, Union
from collection import Hashable

class NoDupDict(Dict[Hashable, Any]):  
    def __setitem__(self, key: Hashable, value: Any):  
        if key in self:  
            raise ValueError(f"duplicate {key!r}")  
  
    def __init__(self, init: DictInt = None, **kwargs: Any) -> None:  
        if isinstance(init, Mapping):  
            super().__init__(init, **kwargs)  
        elif isinstance(init, Iterable):  
            for k, v in cast(Iterable[Tuple[Hashable, Any]], init):  
                self[k] = v  
        elif init is None:  
            super().__init__(**kwargs)  
        else:  
            super().__init__(init, **kwargs)
```


- We still have to implement `update()`, `setdefault()`, `__or__()`, and `__ior__()` to *extend* all the methods that can *mutate* a dictionary.

---
## Metaclasses
Every empty class object in python create by *type class* and we can extend *type class* to create custom *metaclass* .

*Example*: we want to logging  `roll()`  function in every *Die* *subclasses* we can do this with metaclass.
1. Extending *ABCMeta* metaclass . we need to support *abc.abstractmethod* decoration.
2. Inject *logger* attribute into each class, *logger* is part of any *instances* of *class*.
3. Wrap the *concrete* `roll()` method into function that log message.

```python
import abc  
import logging  
import random  
from functools import wraps  
from typing import Type, List, Any, Iterable, cast, Mapping, Union, Tuple, Dict, TypeAlias, Hashable

class DieMeta(abc.ABCMeta):  
    def __new__(  
            cls: Type[type],  
            name: str,  
            base: tuple[type, ...],  
            namespace: dict[str, Any],  
            **kwargs: Any  
    ) -> "DieMeta":  
        if "roll" in namespace and  not getattr(namespace["roll"], "__isabstractmethod__", False):  
            namespace.setdefault("logger", logging.getLogger(name))  
            original_roll = namespace["roll"]  
  
            @wraps(original_roll)  
            def logging_roll(self: "DieLog") -> None:  
                original_roll(self)  
                self.logger.error(f"rolled {self.face}")  
  
            namespace["roll"] = logging_roll  
        new_object = cast("DieMeta", abc.ABCMeta.__new__(cls ,name, base, namespace, **kwargs))  
        return new_object
        

# use metaclass

class DieLog(metaclass=DieMeta):
	logger: logging.Logger

	def __init__(self) -> None:
		self.face: int
		self.roll()
		
	@abc.abstractmethod
	def roll(self) -> None:
		...
		
	def __repr__(self) -> str:
		return f"{self.face}"


class D6L(DieLog):
	def roll(self) -> None:
	"""Some documentation on D6L"""
		self.face = random.randrange(1, 7)
```


## Extending the list class with two subclass 
Python built-in class have two constructor:
1. `list()` to create empty list .
2. `list(x)` to create list from *iterable* source data.

We need to `@overload` decorator to clear for *mypy*:

```python
class SamplePartition(list[SampleDict], abc.ABC):  
    @overload  
    def __init__(self, *, training_subset: float = 0.8) -> None:  
        ...  
  
    @overload  
    def __init__(  
            self,  
            iterable: Optional[Iterable[SampleDict]] = None,  
            *,  
            training_subset: float = 0.8  
    ) -> None:  
        ...  
  
    def __init__(  
            self,  
            iterable: Optional[Iterable[SampleDict]] = None,  
            *,  
            training_subset: float = 0.8  
    ) -> None:  
        self.training_subset = training_subset  
        if iterable:  
            super().__init__(iterable)  
        else:  
            super().__init__()  
  
    @abc.abstractproperty  
    @property    def training(self) -> List[TrainingKnownSample]:  
        ...  
  
    @abc.abstractproperty  
    @property    def testing(self) -> List[TestingKnowSample]:  
        ...
```


- with an *iterable* source of `SampleDict` objects as the only *positional parameter*.
-  This tells *mypy* that we're working with a *dictionary* that has only the *five* supplied *keys* and no *others*.
```python
class SampleDict(TypedDict):  
    sepal_length: float  
    sepal_width: float  
    petal_length: float  
    petal_width: float  
    species: str
```


## A shuffling strategy for partitioning
We can use `random.shuffle()` to handle to randomize shuffling.

```python
class ShufflingSamplePartitioning(SamplePartition):  
    def __init__(self, iterable: Optional[SampleDict],*, training_subset: float = 0.8) -> None:  
        super().__init__(iterable, training_subset=training_subset)  
        self.split: Optional[int] = None  
  
    def shuffle(self):  
        if not self.split:  
            random.shuffle(self)  
            self.split = int(len(self) * self.training_subset)  
  
    @property  
    def training(self) -> List[TrainingKnownSample]:  
        self.shuffle()  
        return [TrainingKnownSample(*sd) for sd in self[: self.split]]  
  
    @property  
    def testing(self) -> List[TestingKnowSample]:  
        self.shuffle()  
        return [TestingKnowSample(**sd) for sd in self[self.split :]]


data = [
{

	"sepal_length": i + 0.1,
	"sepal_width": i + 0.2,
	"petal_length": i + 0.3,
	"petal_width": i + 0.4,
	"species": f"sample {i}",
	} for i in range(10)
]


ssp = ShufflingSamplePartitioning(training_subset=0.67)
for d in data:
	ssp.append(data)

```


## An Incremental Strategy for partitioning
Let's define a subclass of `SamplePartition` that makes a *random* choice between testing and training on each `SampleDict` object that is presented via initialization, or the `append()` or `extend()` methods.

```python
class DelingPartition(abc.ABC):  
    @abc.abstractmethod  
    def __init__(self, items: Optional[Iterable[SampleDict]], *, training_subset: Tuple[int, int] = (8, 10)) -> None:  
        ...  
  
    @abc.abstractmethod  
    def extend(self, items: Iterable[SampleDict]) -> None:  
        ...  
  
    @abc.abstractmethod  
    def append(self, item: SampleDict) -> None:  
        ...  
  
    @property  
    @abc.abstractmethod    def testing(self) -> List[TestingKnowSample]:  
        ...  
  
    @property  
    @abc.abstractmethod    def training(self) -> List[TrainingKnownSample]:  
        ...  
  
  
class CountingDealingPartitioning(DelingPartition):  
    def __init__(self, items: Iterable[SampleDict], *, training_subset: Tuple[int, int] = (8, 10)) -> None:  
        self.training_subset = training_subset  
        self.counter = 0  
        self._training: List[TrainingKnownSample] = []  
        self._testing: List[TestingKnowSample] = []  
        if items is not None:  
            self.extend(items)  
  
    def extend(self, items: Iterable[SampleDict]) -> None:  
        for sample in items:  
            self.append(sample)  
  
    def append(self, item: SampleDict) -> None:  
        n, d = self.training_subset  
        if self.counter % d < n:  
            self._training.append(TrainingKnownSample(**item))  
        else:  
            self._testing.append(TestingKnowSample(**item))  
        self.counter += 1  
  
    @property  
    def training(self) -> List[TrainingKnownSample]:  
        return self._training  
  
    @property  
    def testing(self) -> List[TestingKnowSample]:  
        return self._testing
```
