---
Created Date: 2026-02-17
tags:
  - cpp
  - programming
Next: "[[Understand special member function generation]]"
---
---

- If we’re working in a *mathematical* *domain*, we might find it convenient to have a class representing *polynomials*.
```cpp
class Polynomial {
	public: 
	using RootsType = std::vector<double>;
	// Computing the roots of a polynomial can be expensive
	
	RootsType roots() const
	{
	if (!rootsAreValid) { // if cache not valid
		 // compute roots,
		// store them in rootVals
	rootsAreValid = true;
	}
	return rootVals;
	}
	private:
	mutable bool rootsAreValid{ false }; // see Item 7 for info
	mutable RootsType rootVals{};
}
```



> That’s a classic use case for *mutable*, and that’s why it’s part of the declarations for these data members.



- This client code is perfectly *reasonable*. *roots* is a *const member function*, and that means it represents a read operation. Having multiple *threads* perform a read operation without *synchronization* is safe.
```cpp
Polynomial p;

/*------- Thread 1 ------- */ 
auto rootsOfP = p.roots();
/*------- Thread 2 ------- */
 auto valsGivingZero = p.roots();
```


- The problem is that roots is declared *const*, but it’s *not thread safe*.
```cpp
class Polynomial {

public: 
	using RootType = std::vector<double>;
	
	RootType roots() const 
	{
		std::lock_guard<std::mutex> g(m); // lock mutex
		if (!rootAreValid)
		{
			...
			rootAreValid = true;
		}
		return rootVals;
	} // unlock mutex

private:

mutable std::mutex m;
mutable bool rootAreValid {false};
mutable RootType rootVals{};
}
```

> The *std::mutex m* is declared *mutable*, because *locking* and *unlocking* it are *non-const member* functions, and within roots (a *const member function*), m would otherwise be considered a *const object*.


> **std::mutex is a move-only type**



- Because operations on **std::atomic** variables are often *less* *expensive* than **mutex** *acquisition* and *release*, you may be tempted to lean on **std::atomics** more heavily than you should. For example, in a class *caching* an expensive-to-compute *int*, you might try to use a pair of **std::atomic** variables instead of a *mutex*:

>[!IMPORTANT]
>There’s a lesson here. For a **single variable** or memory location requiring *synchronization*, use of a **std::atomic** is adequate, but once you get to *two or more* variables or memory locations that require manipulation as a unit, you should reach for a **mutex**.

```cpp
class Widget {
public:
...
	int magicValue() const
	{
	std::lock_guard<std::mutex> guard(m); // lock m
	if (cacheValid) return cachedValue;
	else {
		auto val1 = expensiveComputation1();
		auto val2 = expensiveComputation2();
		cachedValue = val1 + val2;
		cacheValid = true;
		return cachedValue;
	}
	} // unlock m
		
	...
	
	private:
		mutable std::mutex m;
		mutable int cachedValue; // no longer atomic
		mutable bool cacheValid{ false }; // no longer atomic
};
```

---



>[!IMPORTANT] **Thing to Remember**
>• Make *const member functions* **thread safe** unless you’re certain they’ll never
be used in a concurrent context.
• Use of **std::atomic** variables may offer *better performance* than a **mutex**, but
they’re suited for manipulation of only a *single variable or memory location*.
