---
Created Date: 2026-05-04
tags:
  - python
  - architecture
  - programming
---
---
## What We Learn?
- How to cause an *exception* to occur
- How to recover when an *exception* has occurred
- How to handle different *exception* types in different *type* 
- Cleaning up when an *exception* has occurred
- Creating new type of *exception*
- Using the *exception* syntax for *flow control*

---

>[!NOTE]
>There is two approaches to dealing with the unforeseen.
>1. Return a recognizable *error-signaling* value from a function, a *value* , like *None*.
>2. The other approach is to *interrupt* the normal, *sequential exception* of statements and diver to statements that handle *exception*.

---
## Raising Exception
In python normal behavior is to execute statements in the order.
**Exception** is an object that inherit from *BaseException*  and when it *raised* break normal flow of *execution* and *bubbled up*  to *call stack* and gave up and printed the *traceback* object.

*Example:*
```python
print "hello, world" 
# Syntax Error: missing oarentheses in call to 'print', do you mean print("hello, world")
```

- We can build custom class for specific type 
```python
class EvenOnly(List[int]):
	def append(self, value: int) -> None:
		if not isinstance(value, int):
			raise TypeError("Only integer can be added")
		if value % 2 != 0:
			raise ValueError("Only even number can be added")
		super().append(value)
#######################################################################		
# we need to override eternd(), insert(), __setitem__() and __init__()
#######################################################################
```

- For time we know that we never reach to *return* in order to don't give error in *mypy* use **NoReturn** in *typing* library
```python
from typing import NoReturn

def no_return() -> Noreturn:
	raise Exception("this always raised")
	return "never returned"
```


---
- There is two exception that direct inherit from *BaseException*:
	- **SystemExit** this exception call *sys.exit()* and clean up code before the program ultimately exit. this exception send signal to *OS* for exit (in Linux `kill -2 <pid>`)
	- **KeyboardIntrrupt** this exception common in command-line when we give *Ctrl + C* it can handle any cleanup task inside the *finally* block .

---
## Define our own exception
When we want an *exception*  and we find none of the build-in *exception* is suitable we introduce a new *exception* with inherit from **Exception** , and we can *raise* our *exception*.
- `Exception.__init__()` accept any argument.
```python
from decimal import Decimal

class InvalidWidrawal(ValueError):
	def __init__(self, balance: Decimal, amount: Decimal) -> None:
		super().__init__()
		self.balance = balance
		self.amount = amount
		
		def overage(self) -> Decimal:
			return self.amount - self.balance
			
	
	try:
		balance = Decimal('25.00')
		raise InvalidWidrawal(balance, Decimal('50.00'))
	except InvalidWidrawal as ex:
		print(ex.overage())
```


---
## Exceptions aren't exceptional

- Like `if` statement *exception* can be used for *decision making*, *branching*, and *message passing* and effect on *flow control*.   
-  There is situation that it shouldn't necessary to burn *CPU* cycles (*LBYL* "*Look Before You Leap*" ) 

```python 
def divide_with_if(dividend: int, divisor: int) -> None:
	if divisor == 0:
		print("you can't divide by zero)
	else:
		print(f"{dividend/divisor=}")	
```

- *Easier to Ask Forgiveness than Permission (EAFP)* styles
```python
def divide_with_exception(dividend: int, divisor: int) -> None:
	try:
		print(f"{dividend/divisor=}")
	except DivisionByZero:
		print("you can't divide by zero)
```



-  We can with *raise* an *exception* and use *try-except* have direct *control flow*
- We *Discovering* **Exceptional Data(raise)** and *Responding* **Exceptional Data(try/except)** 
```python

class OutOfStock(Exception):
	pass
	
class InvalidItem(Exception):
	pass
	
class Inventory:
	def __init__(self, stock: List[ItemType]) -> None:
		pass
	def lock(self, item_type: Item_type) -> None:
		"""Context Entry.
			Lock the item type so nobody slse can manipulate the inventory
			while we're workin.
		"""
		pass
	def unlock(self, item_type: ItemType) -> None:
		"""Context Exit.
		Unlock the item type."""
		pass
	
	def purchase(self, item_type: ItemType) -> int:
		if item.type == "Widget":
			raise OutOfStock(item_type)
		elif item_type == "Gadget":
			return 42
		else:
			raise InvalidItemType(item_type)		
```



---

### @classmethod use case
when use *classmethod* *decorator* this *method* for  class object and every *subclass* inherit from this *class* tailored for that *subclass*

```python

class KnowSample(Sample):
	@classmethod
	def from_dict(cls, row: Dict[str, str]) -> "KnowSample":
		if row["species"] not in {
			"Iris-setosa", "Iris-versicolour", "Iris-virginica"}:
			raise InvalidSampleError(f"invalid species in {row!r}")
		try:
			return cls(
				species=row["species"],
				sepal_length=float(row["sepal_length"]),
				sepal_width=float(row["sepal_width"]),
				petal_length=float(row["petal_length"]),
				petal_width=float(row["petal_width"]),
			)
		except ValueError as ex:
			raise InvalidSampleError(f"invalid {row!r}")

class TrainingKnowSample(KnowSample):
	pass
```

- It is not clear for*mypy* that work we can explicit type mapping:
```python
from typing import cast

class TarainingSample(KnowSample):
	@classmethod
	def from_dict(cls, row: Dict[str, str]) -> "TarainingSample":
		return cast(TarainingSample, super().from_dict(row))
```
