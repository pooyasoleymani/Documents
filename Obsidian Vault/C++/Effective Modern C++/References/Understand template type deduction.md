---
Home: "[[Effective Modern C++17]]"
Up: "[[Deducing Type]]"
Related: "[[Understand auto type deduction]]"
Created Date: 2026-01-05
tags:
  - cpp
  - programming
---
---

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

• *ParamType* is a pointer or reference type, but not a universal reference. (**Universal references** are described in *Item 24* [[Distinguish universal references from rvalue references]]. At this point, all you need to know is that they exist and that they’re not the same as **lvalue** references or **rvalue** references.)
• *ParamType* is a universal reference.
• *ParamType* is neither a pointer nor a reference.

---

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
These examples all show **lvalue reference** parameters, but type deduction works exactly the same way for **rvalue reference** parameters.

  The **constness** of cx and rx continues to be respected, but because we’re now assuming that param is a reference-to-const, there’s no longer a need for const to be deduced as part of T:

```c++
template<typename T>
void f(const T& param); // param is now a ref-to-const

int x = 27; // as before
const int cx = x; // as before
const int& rx = x; // as before

f(x); // T is int, param's type is const int&
f(cx); // T is int, param's type is const int&
f(rx); // T is int, param's type is const int&
```


If *param* were a **pointer** (or a *pointer to* *const*) instead of a reference, things would work essentially the same way:

```c++

template<typename T>
void f(T* param); // param is now a pointer

int x = 27; // as before
const int *px = &x; // px is a ptr to x as a const int

f(&x); // T is int, param's type is int*
f(px); // T is const int, // param's type is const int*

```


> [!NOTE] 
> By now, you may find yourself yawning and nodding off, because C++’s type deduction rules work so naturally for reference and pointer parameters, seeing them in written form is really dull.


## Case 2: ParamType is a Universal Reference
Such parameters are declared like **rvalue references** (i.e., in a function template taking a type parameter *T*, a **universal reference’s** declared type is *T&&*), but they behave differently when **lvalue arguments** are passed in.
The complete story is told in **Item 24**, but here’s the headline version:

-  If expr is an **lvalue**, both **T** and **ParamType** are deduced to be **lvalue references**. Second, although ParamType is declared using the syntax for an **rvalue** **reference**, its deduced type is an **lvalue reference**.
-  If expr is an **rvalue**, the “normal” (i.e., Case 1) rules apply. 
For example:

```c++
template<typename T>
void f(T&& param); // param is now a universal reference

int x = 27; // as before
const int cx = x; // as before
const int& rx = x; // as before

f(x); // x is lvalue, so T is int&, // param's type is also int&
f(cx); // cx is lvalue, so T is const int&, // param's type is also const int&
f(rx); // rx is lvalue, so T is const int&, // param's type is also const int&
f(27); // 27 is rvalue, so T is int, // param's type is therefore int&&
```


## Case 3: ParamType is Neither a Pointer nor a Reference

When ParamType is neither a pointer nor a reference, we’re dealing with pass-by value:

```c++
template<typename T>
void f(T param); // param is now passed by value
```

*That means that param will be a copy of whatever is passed in a completely new object.*

1. As before, if expr’s type is a reference, ignore the reference part.
2. If, after ignoring expr’s reference-ness, expr is const, ignore that, too. If it’s volatile, also ignore that. (volatile objects are uncommon. They’re generally used only for implementing device drivers. For details, see **Item 40**.)

```c++
int x = 27; // as before
const int cx = x; // as before
const int& rx = x; // as before

f(x); // T's and param's types are both int
f(cx); // T's and param's types are again both int
f(rx); // T's and param's types are still both int
```

