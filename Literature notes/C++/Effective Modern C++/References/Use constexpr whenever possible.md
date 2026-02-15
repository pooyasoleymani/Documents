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
```

