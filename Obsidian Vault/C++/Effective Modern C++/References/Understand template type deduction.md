
We can think of a function template as looking like this:

```c++
template<typename T>
void f(ParamType param);

f(expr); // call f with some expression
```


During compilation, compilers use expr to deduce two types: one for **T** and one for **ParamType**.
ParamType often contains adornments, e.g., **const** or reference qualifiers. For example:

```c++
template<typename T>
void f(const T& param); // ParamType is const T&

int x = 0;
f(x); // call f with an int
```


The type deduced for T is dependent not just on the type of expr, but also on the form of ParamType. There are three cases:

• *ParamType* is a pointer or reference type, but not a universal reference. (**Universal references** are described in *Item 24* [[Distinguish universal references from rvalue references.]]. At this point, all you need to know is that they exist and that they’re not the same as **lvalue** references or **rvalue** references.)
• *ParamType* is a universal reference.
• *ParamType* is neither a pointer nor a reference.

## Case 1: ParamType is a Reference or Pointer, but not a Universal Reference

The simplest situation is when ParamType is a reference type or a pointer type, but
not a universal reference. In that case, type deduction works like this:

1. If expr’s type is a reference, ignore the reference part.
2. Then pattern-match expr’s type against ParamType to determine T.

```c++
template<typename T>
void f(T& param); // param is a reference

// variable declarations.
int x = 27; // x is an int
const int cx = x; // cx is a const int
const int& rx = x; // rx is a reference to x as a const int
```

The deduced types for **param** and **T** in various calls are as follows:

```cpp

f(x); // T is int, param's type is int&

f(cx); // T is const int, param's type is const int&

f(rx); // T is const int, param's type is const int&

```


 In the second and third calls, notice that because **cx** and **rx** designate **const** values, **T** is deduced to be **const int**, thus yielding a parameter type of **const int&**.
