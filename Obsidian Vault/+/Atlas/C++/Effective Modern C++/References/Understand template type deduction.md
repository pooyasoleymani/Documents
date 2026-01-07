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



> [!NOTE] 
> Even though **cx** and **rx** represent **const values**, param isn’t **const**. That
makes sense. param is an object that’s completely independent of **cx** and **rx**—a copy
of **cx** or **rx**. The fact that **cx** and **rx** can’t be modified says nothing about whether
param can be. That’s why expr’s **constness** (and **volatileness**, if any) is ignored
when deducing a type for param: just because expr can’t be modified doesn’t mean
that a copy of it can’t be.

> [!IMPORTANT] 
> It’s important to recognize that **const** (and **volatile**) is **ignored** only for *by-value* parameters.
The type deduced for T is dependent not just on the type of expr, but also on the form of ParamType. There are three cases:


case where expr is a const pointer to a const object, and expr is passed to a by value
param:

```c++
template<typename T>
void f(T param); // param is still passed by value
const char* const ptr = "Fun with pointers"; // ptr is const pointer to const object

f(ptr); // pass arg of type const char * const Here, the const to the right of the asterisk declares ptr to be const: ptr can’t
```

##### the **const** to the right of the asterisk declares **ptr** to be const: **ptr** can’t be made to point to a different location, nor can it be set to null.


> [!NOTE] 
> The constness of what ptr points to is preserved during type deduction, but the **constness** of **ptr** itself is ignored when copying it to *create the new pointer*, param.

---

## Array Arguments

A primary contributor to this illusion is that, in many contexts, an array decays into a pointer to its first element. This decay is what permits code like this to compile:

```c++
const char name[] = "J. P. Briggs"; // name's type is // const char[13]
const char * ptrToName = name; // array decays to pointer
```

>[!NOTE] 
> These types (**const char* and const char[13]**) are not the same, but because of the array-to-pointer decay rule, the code compiles.
****



```cpp
void myFunc(int param[]);
void myFunc(int* param); // same function as above

template<typename T>
void f(T param); // template with by-value parameter
f(name); // name is array, but T deduced as const char*

---------------------------------------------------------------
	/* Declare parameters that are references to arrays: */
---------------------------------------------------------------

template<typename T>
void f(T& param); // template with by-reference parameter
f(name); // pass array to f

---------------------------------------------------------------
/* 
	T is deduced to be const char [13], and the type of f’s
	parameter (a reference to this array) is const char (&)[13]. 
*/
---------------------------------------------------------------
```


Interestingly, the ability to declare references to arrays enables creation of a template
that deduces the number of elements that an array contains:

```cpp
// return size of an array as a compile-time constant. (The
// array parameter has no name, because we care only about
// the number of elements it contains.)
template<typename T, std::size_t N> 
constexpr std::size_t arraySize(T (&)[N]) noexcept 
// see info  below on constexpr and noexcept
{ 
	return N;
} 
// As Item 15 explains, declaring this function constexpr makes its result available during compilation

int keyVals[] = { 1, 3, 7, 9, 11, 22, 35 }; // keyVals has 7 elements

int mappedVals[arraySize(keyVals)]; // so does mappedVals

std::array<int, arraySize(keyVals)> mappedVals;

```


As for arraySize being declared noexcept, that’s to help compilers generate better
code. For details, see **Item 14 [[Declare functions noexcept if they won’t emit exceptions.]].**


---

## Function Arguments

arrays applies to type deduction for functions and their decay into function
pointers:

```cpp
void someFunc(int, double); // someFunc is a function; type is void(int, double)
template<typename T>
void f1(T param); // in f1, param passed by value
template<typename T>
void f2(T& param); // in f2, param passed by ref

f1(someFunc); // param deduced as ptr-to-func;  type is void (*)(int, double)
f2(someFunc); // param deduced as ref-to-func; type is void (&)(int, double)
```


---

> [!IMPORTANT] Things to Remember
>                     
> - During template type deduction, arguments that are references are treated as non-references, i.e., their reference-ness is ignored.
> - When deducing types for universal reference parameters, lvalue arguments get special treatment.
> -  When deducing types for by-value parameters, const and/or volatile arguments are treated as non-const and non-volatile.
> -  During template type deduction, arguments that are array or function names decay to pointers, unless they’re used to initialize references.
