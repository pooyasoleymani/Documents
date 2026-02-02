---
Created Date: 2026-01-05
tags:
  - cpp
  - programming
Up: "[[Understand auto type deduction]]"
Next: "[[Know how to view deduced types]]"
---
---

## Understand decltype

**decltype** typically parrots back the exact type of the name or expression you give it:

```c++
const int i = 0; // decltype(i) is const int
bool f(const Widget& w); // decltype(w) is const Widget& decltype(f) is bool(const Widget&)
struct Point {
int x, y; // decltype(Point::x) is int
}; // decltype(Point::y) is int

Widget w; // decltype(w) is Widget
if (f(w)) … // decltype(f(w)) is bool

template<typename T> // simplified version of std::vector
class vector {
public:
T& operator[](std::size_t index);
};
vector<int> v; // decltype(v) is vector<int>

if (v[0] == 0) // decltype(v[0]) is int&
```


**operator[]** on a container of objects of type T typically returns a **T&**. This is the case
for *std::deque*, for example, and it’s almost always the case for **std::vector** for **bool** . 
For **std::vector** , however, **operator[]** does not return a **bool&** .
Instead, it returns a brand **new object**.

**decltype** makes it easy to express that. Here’s a first cut at the template we’d like to write, showing the use of **decltype** to compute the **return type**


```c++
template<typename Container, typename Index> // works, but requires refinement
auto authAndAccess(Container& c, Index i) -> decltype(c[i]) 
{
authenticateUser();
return c[i];
}

// C++14 we can omit the trailing

template<typename Container, typename Index> // C++14 ;not quite correct
auto authAndAccess(Container& c, Index i) 
{ 
authenticateUser();
return c[i]; // return type deduced from c[i] 
}
```


> [!NOTE]
> template type deduction, the **reference-ness** of an initializing expression is ignored.
> 
> ```c++
> std::deque<int> d;
> authAndAccess(d, 5) = 10; // authenticate user, return d[5],then assign 10 to it;
> ```
> 
> Here, **d[5]** returns an **int&**, but auto return type deduction for authAndAccess will
> *strip off the reference*, thus yielding a return type of **int**.
> That int, being the return value of a function, is an **rvalue**, and the code above thus attempts to assign 10 to an **rvalue** **int**.


The use of **decltype(auto)** is not limited to function return types.

```cpp
Widget w;
const Widget& cw = w;
auto myWidget1 = cw; // auto type deduction: myWidget1's type is Widget
decltype(auto) myWidget2 = cw; // decltype type deduction: myWidget2's type is
// const Widget&
```


---

##### To avoid **overloading** for **lvalue** and **rvalue** use **universal references**:


```c++

template<typename Container, typename Index>
decltype(auto) authAndAccess(Container&& c, Index i);


// ------------------- C++14 final version ------------------- 

template<typename Container, typename Index> 
decltype(auto) authAndAccess(Container&& c, Index i)
{
	authenticateUser();
	return std::forward<Container>(c)[i];
}


// ------------------- C++11 final version ------------------- 

template<typename Container, typename Index> 
auto authAndAccess(Container&& c, Index i) -> decltype(std::forward<Container>(c)[i])
{
	authenticateUser();
	return std::forward<Container>(c)[i];
}
```


> [!NOTE] **decltype for expressions**
> That is, if an lvalue expression other than a name has type **T**, **decltype** reports that type as **T&**.
>  ```
> decltype(auto) f1()
>  {
> int x = 0;
> return x;          // decltype(x) is int, so f1 returns int
> }
> 
> decltype(auto) f2()
>{
>int x = 0;
>return (x);        // decltype((x)) is int&, so f2 returns int&
>}
>```
>
>Note that not only does f2 have a different return type from f1, it’s also returning a
reference to a local variable!


---

>[!IMPORTANT] **Things to Remember**
> - **decltype** almost always yields the type of a variable or expression *without any modifications*.
>-  For lvalue expressions of type **T** other than names, decltype always reports a
>type of **T&**.
>- *C++14* supports **decltype(auto)**, which, like auto, deduces a type from its initializer, but it performs the type deduction using the **decltype rules**.
