---
Home: "[[Effective Modern C++17]]"
Up: "[[Understand template type deduction]]"
Next: "[[Understand decltype]]"
Created Date: 2026-01-05
tags:
  - cpp
  - programming
---
---

## Understand auto type deduction

with only one curious exception, auto type deduction is template type deduction.
the type specifier takes the place of ParamType, so there
are three cases for that, too:

-  *Case 1*: **The type specifier is a pointer or reference, but not a universal reference.**
-  *Case 2*: **The type specifier is a universal reference.**
-  *Case 3*: **The type specifier is neither a pointer nor a reference.**

```c++
// ----------------------------  Case 1 & 3 ----------------------------
auto x = 27; // case 3 (x is neither ptr nor reference)
const auto cx = x; // case 3 (cx isn't either)
const auto& rx = x; // case 1 (rx is a non-universal ref.)

// ----------------------------  Case 2 --------------------------------
auto&& uref1 = x; // x is int and lvalue, so uref1's type is int&
auto&& uref2 = cx; // cx is const int and lvalue, so uref2's type is const int&
auto&& uref3 = 27; // 27 is int and rvalue, so uref3's type is int&&

// -------------------------  Array & Function -------------------------
const char name[] = "R. N. Briggs" // name's type is const char[13];
auto arr1 = name; // arr1's type is const char*
auto& arr2 = name; // arr2's type is const char (&)[13]

void someFunc(int, double); // someFunc is a function; type is void(int, double)
auto func1 = someFunc; // func1's type is void (*)(int, double)
auto& func2 = someFunc; // func2's type is void (&)(int, double)
```


---
## auto vs template deduction

This is due to a special type deduction rule for auto. When the initializer for an
auto-declared variable is enclosed in braces, the deduced type is a **std::initializer_list**.

```c++
auto x1 = 27; // type is int, value is 27
auto x2(27); // ditto
auto x3 = { 27 }; // type is std::initializer_list<int>, value is { 27 }
auto x4{ 27 }; // ditto

auto x5 = { 1, 2, 3.0 }; // error! can't deduce T for std::initializer_list<T>
auto x = { 11, 23, 9 }; // x's type is std::initializer_list<int>
```


> [!IMPORTANT] 
> So the only real difference between auto and template type deduction is that auto
assumes that a braced initializer represents a **std::initializer_list**, but template
type deduction doesn’t.



```c++
template<typename T> // template with parameter
void f(T param); // declaration equivalent to x's declaration
f({ 11, 23, 9 }); // error! can't deduce type for T

template<typename T>
void f(std::initializer_list<T> initList);
f({ 11, 23, 9 }); // T deduced as int, and initList's type is std::initializer_list<int>
```


function with an **auto** return type that returns a **braced initializer** won’t compile:

```c++
auto createInitList()
{
return { 1, 2, 3 }; // error: can't deduce type for { 1, 2, 3 }
} 
```


The same is true when **auto** is used in a parameter type specification in a **C++14** lambda:

```c++
std::vector<int> v;
auto resetV = [&v](const auto& newValue) { v = newValue; }; // C++14

resetV({ 1, 2, 3 }); // error! can't deduce type for { 1, 2, 3 }
```


> [!IMPORTANT] **Things to Remember**
> - auto type deduction is usually the same as template type deduction, but auto
type deduction assumes that a braced initializer represents a **std::initializer_list**, and template type deduction doesn’t.
>-  auto in a function return type or a **lambda** parameter implies template type
deduction, not **auto** type deduction.


