---
Created Date: 2026-02-03
tags:
  - cpp
  - programming
Up: "[[Declare functions noexcept if they won’t emit exceptions.]]"
Next: "[[Make const member functions thread safe]]"
---
---
- Conceptually, **constexpr** indicates a value that’s not only *constant*, it’s known during *compilation*.
- **constexpr** **functions** are const, nor can you take for granted that their values are known during *compilation*.
- They may be placed in *read-only* memory, for example, and, especially for developers of *embedded systems*, this can be a feature of considerable importance.

```cpp
constexpr auto arraySize = 10;
std::array<int, arrySize> data;
```


- **const** doesn’t offer the same guarantee as **constexpr**, because const objects need not be initialized with values known during *compilation*:
```cpp
const auto arraySize = 10
std::array<int, arraySize> data: // error! arraySize's value not known at compilation
```


> all **constexpr** objects are *const* but but not all *const* objects are **constexpr**


### Usage Scenarios:

1. **constexpr** functions can be use in context that demand *compile-time* constant. if any of arguments not known during compilation your code will be rejected.
2. When **constexpr** function called with one or more values that are not known during *compile-time* function act like normal function.



- When a function return value not **constexpr** we can write **constexpr** function:
```cpp
// std::pow is not constexpr function

constexpr int pow(int base, int exp) noexcept {
...
};

constexpr auto numCount = 5;
std::array<int, pow(3, numCount)> res; 
```




- In C++11, all *built-in types* except *void* qualify, but user-defined types may be literal, too, because *constructors* and other *member functions* may be **constexpr**:

```cpp
class Point {
public:
	constexpr Point(double xVal = 0, double yVal = 0) noexcept :
		x(xVal), y(yVal)
		{}
	constexpr double xValue() const noexcept { return x; }
	constexpr double yValue() const noexcept { return y; }
	void setX(double newX) noexcept { x = newX; }
	void setY(double newY) noexcept { y = newY; }
private:
double x, y;
}

constexpr Point p1(9.4, 27.7); // fine, "runs" constexpr ctor during compilation

constexpr Point midPoint(const Point& p1, const Point& p2) noexcept
{
	return {
	(p1.xValue() + p2.xValue()) / 2, 
	(p1.yValue() + p2.yValue()) / 2
	}
};

constexpr auto mid = midPoint(p1, p2);
```



- **void** isn’t a literal type in *C++11*. Both these restrictions are lifted in *C++14*, so in *C++14*, even Point’s setters can be **constexpr**:
```cpp
class Point {
	public:
		
		constexpr void setX(double newX) noexcept { x = newX };
		constexpr void setY(double newY) noexcept { x = newY };
}

// return reflection of p with respect to the origin (C++14)
constexpr Point reflection(const Point& p) noexcept
{
	Point result;
	result.setX(-p.xValue())
	result.setY(-p.yValue())
	
	return result;
}

constexpr Point p1(9.4, 27.7); // as above
constexpr Point p2(28.8, 5.3);
constexpr auto mid = midpoint(p1, p2);
constexpr auto reflectedMid = reflection(mid);
```



>[!NOTE]
>The simple act of adding *I/O* to a *function* for *debugging* or *performance* tuning could lead to such a problem, because *I/O* statements are generally *not permitted* in **constexpr** *functions*.


---



>[!IMPORTANT] **Things to Remember**
>• **constexpr** objects are *const* and are initialized with values known during
*compilation*.
• **constexpr** functions can produce *compile-time* results when called with
arguments whose values are known during *compilation*.
• **constexpr** objects and functions may be used in a wider range of contexts
than **non-constexpr** objects and functions.
• **constexpr** is part of an object’s or function’s interface.
