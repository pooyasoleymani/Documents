---
Created Date: 2026-01-11
tags:
  - cpp
  - programming
Up: "[[Prefer auto to explicit type declarations]]"
Next: "[[Distinguish between () and {} when creating objects]]"
---
---

## auto problems

suppose I have a function that takes a **Widget** and returns a `std::vector<bool>`, where each **bool** indicates whether the **Widget** offers a particular feature:

```c++
std::vector<bool> features(const Widget& w);
```

Further suppose that **bit 5** indicates whether the Widget has **high priority**. We can
thus write code like this:

```c++
Widget w;
bool highPriority = features(w)[5]; // is w high priority?
processWidget(w, highPriority); // process w in accord with its priority
```

If replacing the explicit type for **highPriority** with **auto**:

```c++

auto highPriority = features(w)[5]; 
/* 
// is w high priority? 
// All the code will continue to compile, but its behavior is 
// no longer predictable:
*/
processWidget(w, highPriority); // undefined behavior!****
```


>[!NOTE]
Though` std::vector<bool>` conceptually holds bools, `operator[]` for `std::vector<bool>` *doesn’t return a reference* to an element of the container (which is what `std::vector::operator[] `returns for every type except **bool**). Instead, it returns an object of type `std::vector<bool>::reference` (a class nested inside `std::vector<bool>`).
`std::vector<bool>::reference` exists because `std::vector<bool>` is specified to represent its **bools** in packed form, one bit per bool. That creates a problem for `std::vector<bool>`’s `operator[]`, because `operator[]` for` std::vector<T>` is supposed to return a `T&`, but C++ *forbids references* to **bits**.


---
## Proxy Class

`std::vector<bool>::reference` is an example of a **proxy class**: a class that exists
for the purpose of emulating and augmenting the behavior of some other type. 
**Proxy classes** are employed for a variety of purposes. `std::vector<bool>::reference` exists to offer the *illusion* that `operator[]` for `std::vector<bool>` returns a reference to a bit.

**smart pointe**r types (see Chapter4)are **proxy classes** that graft resource management onto **raw pointers**.


*Some proxy classes are designed to be apparent to clients.*
`std::vector<bool>::reference` is an example of such “**invisible**” proxies, as is its **std::bitset** compatriot, **std::bitset::reference**.


---

Also in that camp are some classes in C++ libraries employing a technique known as
**expression templates**. Such libraries were originally developed to **improve the efficiency**
of numeric code.
can be computed much more efficiently if operator+ for Matrix objects returns a
proxy for the result instead of the result itself.
It’s rarely possible for source code to fully cloak **proxy objects**.  They’re typically returned from functions that clients are expected to call, so function signatures usually reflect their existence.
Here’s the spec for `std::vector<bool>::operator[]`, for example

```c++
namespace std { // from C++ Standards

template <class Allocator>
class vector<bool, Allocator> {
public:
…
class reference { … };
reference operator[](size_type n);
…
	};
}
```


 #### The problem is that **auto** isn’t deducing the type you want it to deduce. The solution is to force a different type deduction. The way you do that is what I call the **explicitly typed** **initializer** **idiom**.
#### The **explicitly typed initializer idiom** involves declaring a variable with **auto** but casting the initialization expression to the type you want auto to deduce.

```c++
auto highPriority = static_cast<bool>(features(w)[5]);
```


---


>[!IMPORTANT] 
> - **“Invisible”** **proxy** types can cause **auto** to deduce the *“wrong”* type for an initializing expression.
>-  The explicitly typed initializer idiom forces **auto** to deduce the type you want it to have.
