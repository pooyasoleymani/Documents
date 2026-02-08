---
Created Date: 2026-01-11
tags:
  - cpp
  - programming
Up: "[[auto]]"
Next: "[[Use the explicitly typed initializer idiom when auto deduces undesired types]]"
---
---

Let’s move on to the simple joy of declaring a **local variable** to be **initialized** by dereferencing an **iterator**:

```c++

template<typename It> // algorithm to dwim ("do what I mean")
void dwim(It b, It e) // for all elements in range from // b to e
{ 
while (b != e) {
typename std::iterator_traits<It>::value_type currValue = *b;
	}
}
```

That means you can wave goodbye to a host of **uninitialized** **variable** problems as you speed by on the modern C++ superhighway:

```c++
int x1; // potentially uninitialized
auto x2; // error! initializer required
auto x3 = 0; // fine, x's value is well-defined
```

Said highway lacks the potholes associated with declaring a **local variable** whose value is that of a **dereferenced** **iterator**:

```c++

template<typename It> // as before
void dwim(It b, It e)
{
while (b != e) {
auto currValue = *b;
	}
}

// ---------------------------------------------------------------------

auto derefUPLess = // comparison func.
[](const std::unique_ptr<Widget>& p1, // for Widgets
const std::unique_ptr<Widget>& p2) // pointed to by
{ return *p1 < *p2; }; // std::unique_ptrs

// ---------------------------------------------------------------------
// In C++14, the temperature drops further, because parameters to lambda  expressions may involve auto:
// ---------------------------------------------------------------------

auto derefLess = [](const auto& p1, const auto& p2) // C++14 comparison function for values pointed
{ return *p1 < *p2; }; // to by anything pointer-like

```



---
> [!NOTE] **What is std::function?**
>**std::function** is a template in the C++11 Standard Library that generalizes the idea
>of a **function pointer**. Whereas **function pointers** can point only to functions, however,
>**std::function** objects can refer to any **callable** object, i.e., to anything that can
>be **invoked** like a function.


 It’s important to recognize that even setting aside the syntactic verbosity and need to repeat the parameter types, using **std::function** is not the same as using **auto**. An auto-declared variable holding a closure has the same type as the **closure**, and as such it uses only as much memory as the **closure** requires.
 The type of a **std::function** declared variable holding a closure is an instantiation of the **std::function** template, and that has a fixed size for any given signature.
 This size may not be adequate for the closure it’s asked to store, and when that’s the case, the **std::function** **constructor** will allocate **heap memory** to store the **closure**.
 

```c++
// C++11 signature for std::unique_ptr<Widget> comparison function
bool(const std::unique_ptr<Widget>&, const std::unique_ptr<Widget>&)


std::function<bool(const std::unique_ptr<Widget>&, const std::unique_ptr<Widget>&)> func;

// -------------------------------------------------------------------------------
// Because lambda expressions yield callable objects, closures can be stored in std::function objects.
// -------------------------------------------------------------------------------

std::function<bool(const std::unique_ptr<Widget>&, const std::unique_ptr<Widget>&)> DifferUpLess = [](const std::unique_ptr<Widget>& p1, const std::unique_ptr<Widget>& p2) { return *p1 > *p2; };

```


> [!IMPORTANT]
> **std::function** object typically uses more memory than the **auto-declared** object.
> In other words, the **std::function** approach is generally bigger and slower than the **auto** approach, and it may yield **out-of-memory exceptions**, too.


Here’s something you’ve probably seen—possibly even written:

```c++

std::vector<int> v;
unsigned sz = v.size(); // This means that code that works under 32-bit Windows may behave incorrectly under 64-bit Windows

auto sz = v.size(); // sz's type is std::vector<int>::size_type
```


---

>[!IMPORTANT]  **Things to Remember**
> - **auto** variables must be initialized, are generally immune to type mismatches
that can lead to portability or efficiency problems, can ease the process of refactoring, and typically require less typing than variables with explicitly specified types.
 >- **auto-typed** variables are subject to the pitfalls described in Items 2 and 6.
 