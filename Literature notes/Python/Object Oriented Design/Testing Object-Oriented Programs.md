---
Created Date: 2026-05-24
tags:
  - python
  - architecture
  - programming
Next: "[[Concurrency]]"
---
---
## What we Learn
- The importance of *unit testing* and *test-driven development*
- The standard library *unittest module*
- The *pytest* tool
- The *mock* module
- *Code coverage*

---
## Why tests?
• To ensure that code is working the way the developer thinks it should
• To ensure that code continues working when we make changes
• To ensure that the developer understood the requirements
• To ensure that the code we are writing has a maintainable interface
• Using tests to drive development
• Managing different objectives for testing
• Having a consistent pattern for test scenarios


---
## Test-driven development
We don't write any *code* until after we have written the *tests* that will prove it works. The *first time* we run a *test*, it should *fail*, since the code hasn't been written. Then, we write the *code* that ensures the *test passes*, and then write another *test* for the next segment of *code*.

There are two goals of the test-driven methodology. 
1.  Ensure that *tests* really get *written*.
2. writing *tests* first forces us to consider *exactly* how the *code* will be used.


---
## Type of Tests
1. **Unit tests:** Confirm the *software components* work in *isolation*. the **Coverage tools** use to ensure that all the lines of *code* is part of *unit test*. 
2. **Integration tests:** Confirm *software components* work when *integrated* (*System tests*). 


---
## Testing patterns
Writing code is often challenging. We need to figure out what the *internal state* of the *object* is, what *state* changes it undergoes, and *determine* the other *objects* it *collaborates* with.

**Tests is simpler than class definitions.**
```gherkin
GIVEN some precondition(s) for a scenario
WHEN we exercise some method of a class
THEN some state change(s) or side effect(s) will occur that we can confirm
```

```python
def average(data: list[Optional[int]]) -> Optional[float]:  
    """  
    Given a list, data [1, 2, None ,3, 4].
	When we compute m = average(data).
	Then the result, m, is 2.5    
	"""    
	pass
```


---
## Unit testing with unittest
Most important of this module is `TestCase` *class*
- `Given` in scenario implemented with `setUp()` method.

```python
import unittest  
  
class CheckNumber(unittest.TestCase):  
    def test_int_float(self):  
        self.assertEqual(1, 1.0)  
  
if __name__ == '__main__':  
    unittest.main()
```


---
## Unit test with pytest
It doesn't require *test cases to* be *subclasses* of `unittest.TestCase`. Instead, it takes advantage of the fact that Python *functions* are *first-class objects* and allows any properly named *function* to behave like a *test*. Rather than providing a bunch of custom *methods* for *asserting* *equality*, it uses the *assert* *statement* to verify *results*.

```python
def test_int_float() -> None:
	assert 1 == 1.0

# Or Class base tests

class TestNumbers:
	def test_int_float(self) -> None:
	assert 1 == 1.0
	
	def test_str_int(self) -> None:
		assert "1" == 1
```


---
### pytest's setup and teardown functions
If we are writing **class-based tests**, we can use two *methods* called `setup_method()` and `teardown_method()`. They are called *before* and *after* each test *method* in the *class* to perform *setup* and *cleanup* duties, respectively.

 The `setup_class()` and `teardown_class()` *methods* are expected to be *class* *methods*; they accept a single argument representing the *class* in question (there is no *self* *argument* because there's no *instance*; instead, the *class* is *provided*). These methods are run by pytest when the *class* is *initiated* rather than on each *test* run.

Finally, we have the `setup_module()` and `teardown_module()` *functions*, which are run by *pytest* *immediately* before and after *all* *tests* (in *functions* or *classes*) in that *module*.
```python
from __future__ import annotations
from typing import Any, Callable

def setup_module(module: Any) -> None:
	print(f"setting up MODULE {module.__name__}")

def teardown_module(module: Any) -> None:
	print(f"tearing down MODULE {module.__name__}")

def test_a_function() -> None:
	print("RUNNING TEST FUNCTION")

class BaseTest:
	@classmethod
	def setup_class(cls: type["BaseTest"]) -> None:
		print(f"setting up CLASS {cls.__name__}")

	@classmethod
	def teardown_class(cls: type["BaseTest"]) -> None:
		print(f"tearing down CLASS {cls.__name__}\n")

	def setup_method(self, method: Callable[[], None]) -> None:
		print(f"setting up METHOD {method.__name__}")
	
	def teardown_method(self, method: Callable[[], None]) -> None:
		print(f"tearing down METHOD {method.__name__}")

class TestClass1(BaseTest):
	def test_method_1(self) -> None:
		print("RUNNING METHOD 1-1")
	
	def test_method_2(self) -> None:
		print("RUNNING METHOD 1-2")
	
class TestClass2(BaseTest):
	def test_method_1(self) -> None:
		print("RUNNING METHOD 2-1")
	
	def test_method_2(self) -> None:
		print("RUNNING METHOD 2-2")
```

