---
Created Date: 2026-01-11
tags:
  - cpp
  - programming
Next: "[[Prefer nullptr to 0 and NULL]]"
---
---

- Depending on your perspective, syntax choices for object initialization in C++11 embody either an embarrassment of riches or a confusing mess. As a general rule, initialization values may be specified with **parentheses**, an equals sign, or **braces**:

```c++
int x(0); // initializer is in parentheses
int y = 0; // initializer follows "="
int z{ 0 }; // initializer is in braces

int z = { 0 }; // initializer uses "=" and braces
```




- it’s important to distinguish **initialization** from assignment, because different function calls are involved:

```c++
Widget w1; // call default constructor
Widget w2 = w1; // not an assignment; calls copy ctor
w1 = w2; // an assignment; calls copy operator=
```




- Using **braces**, specifying the **initial** contents of a container is easy:

```c++
std::vector<int> v{ 1, 3, 5 }; // v's initial content is 1, 3, 5
```



- **Braces** can also be used to specify default **initialization** values for **non-static** data members This capability—new to C++11—is shared with the **“=”** **initialization** syntax, but not with **parentheses**:

```c++
class Widget {
…
private:
	int x{ 0 }; // fine, x's default value is 0
	int y = 0; // also fine
	int z(0); // error!
};
```




- On the other hand, **uncopyable** objects (e.g., **std::atomics**—see Item 40) may be **initialized** using **braces** or **parentheses**, but not using **“=”**:

```c++
std::atomic<int> ai1{ 0 }; // fine
std::atomic<int> ai2(0); // fine
std::atomic<int> ai3 = 0; // error!
```



- A **novel** feature of **braced** **initialization** is that it prohibits **implicit** *narrowing conversions among* **built-in** types. If the value of an expression in a **braced** **initializer** isn’t guaranteed to be expressible by the type of the object being **initialized**, the code won’t compile:

```c++
double x, y, z;
int sum1{ x + y + z }; // error! sum of doubles may not be expressible as int
```




- **Initialization** using **parentheses** and **“=”** doesn’t **check** for *narrowing conversions*, because that could break too much *legacy code*:

```c++
int sum2(x + y + z); // okay (value of expression truncated to an int)
int sum3 = x + y + z; // ditto
```





-  Another noteworthy characteristic of **braced** **initialization** is its immunity to C++’s most ***vexing parse***. The root of the problem is that if you want to call a **constructor** with an argument, you can do it like this:
```c++
Widget w1(10); // call Widget ctor with argument 10

Widget w2(); // most vexing parse! declares a function named w2 that returns a Widget!

Widget w3{}; // calls Widget ctor with no args
```




- In constructor calls, **parentheses** and **braces** have the same meaning as long as **std::initializer_list** parameters are *not* *involved*:

```c++
class Widget {
public:
	Widget(int i, bool b); // ctors not declaring
	Widget(int i, double d); // std::initializer_list params
…
};

Widget w1(10, true); // calls first ctor
Widget w2{10, true}; // also calls first ctor
Widget w3(10, 5.0); // calls second ctor
Widget w4{10, 5.0}; // also calls second ctor

// -----------------------------------------------------------------
// If the Widget class above is augmented with a constructor taking a // std::initializer_list<long double>, for example:

class Widget {
public:
	Widget(int i, bool b); // as before
	Widget(int i, double d); // as before
	Widget(std::initializer_list<long double> il); // added
…
};

Widget w1(10, true); // uses parens and, as before, calls first ctor

Widget w2{10, true}; // uses braces, but now calls std::initializer_list ctor (10 and true convert to long double)

Widget w3(10, 5.0); // uses parens and, as before, calls second ctor

Widget w4{10, 5.0}; // uses braces, but now calls std::initializer_list ctor (10 and 5.0 convert to long double)
```




- Even what would normally be **copy** and **move** construction can be *hijacked* by **std::initializer_list** constructors:

```c++
class Widget {
public:
	Widget(int i, bool b); // as before
	Widget(int i, double d); // as before
	Widget(std::initializer_list<long double> il); // as before
	operator float() const; // convert to float
};

Widget w5(w4); // uses parens, calls copy ctor
Widget w6{w4}; // uses braces, calls std::initializer_list ctor (w4 // converts to float, and float converts to long double)

Widget w7(std::move(w4)); // uses parens, calls move ctor
Widget w8{std::move(w4)}; // uses braces, calls 
// std::initializer_list ctor (for same reason as w6)
```



- **Compilers**’ determination to match **braced** **initializers** with constructors taking **std::initializer_list**s is so strong, it prevails even if the best-match  **std::initializer_list** constructor can’t be called. For example:

```c++
class Widget {
public:
	Widget(int i, bool b); // as before
	Widget(int i, double d); // as before
	Widget(std::initializer_list<bool> il); // element type is now        // bool no implicit conversion funcs
};

Widget w{10, 5.0}; // error! requires narrowing conversions
```




 #### Only if there’s no way to convert the types of the arguments in a **braced** **initializer** to the type in a `std::initializer_list` do compilers fall back on normal **overload resolution**. For example, if we replace the `std::initializer_list<bool>` constructor with one taking a `std::initializer_list<std::string>`, the non `std:: initializer_lis`t constructors become candidates again, because there is no way to convert **int**s and bools to `std::strings`:

```c++
class Widget {
public:
	Widget(int i, bool b); // as before
	Widget(int i, double d); // as before std::initializer_list element type is  //now std::string
Widget(std::initializer_list<std::string> il);
… // no implicit

}; // conversion funcs

Widget w1(10, true); // uses parens, still calls first ctor
Widget w2{10, true}; // uses braces, now calls first ctor
Widget w3(10, 5.0); // uses parens, still calls second ctor
Widget w4{10, 5.0}; // uses braces, now calls second ctor

// The rule is that you get default construction. Empty braces mean no arguments, // not an empty std::initializer_list:

Widget w1; // calls default ctor
Widget w2{}; // also calls default ctor
Widget w3(); // most vexing parse! declares a function!
```




- If you want to call a **std::initializer_list** constructor with an empty **std::initializer_list**, you do it by making the empty **braces** a constructor argument—by putting the empty braces inside the **parentheses** or braces demarcating what you’re passing:

```c++
Widget w4({}); // calls std::initializer_list ctor with empty list
Widget w5{{}}; // ditto
```



- **std::vector** has a **non-std::initializer_list** constructor that allows you to specify the initial size of the container and a value each of the initial elements should have, but it also has a constructor taking a **std::initializer_list** that permits you to specify the initial values in the container.
```cpp
// use non-std::initializer_list  ctor: create 10-element std::vector, all 
// elements have value of 20
std::vector<int> v1(10, 20);

// use std::initializer_list ctor: 
// create 2-element std::vector, element values are 10 and 20
std::vector<int> v2{10, 20};
```



- If you’re a **template** author, the tension between **parentheses** and **braces** for object creation can be especially frustrating, because, in general, it’s not possible to know which should be used. A **variadic template** makes this conceptually straightforward:
```c++
// type of object to create typename... Ts> 
// types of arguments to use

template<typename T, typename... params>
void DoSomting(T&&.. params)
{
// create local T object from params...
}

T localObject(std::forward<Ts>(params)...); // using parens
T localObject{std::forward<Ts>(params)...}; // using braces
```


---


>[!IMPORTANT] **Things to Remember**
>-  Braced initialization is the most widely usable initialization syntax, it prevents *narrowing conversions*, and it’s immune to C++’s most *vexing parse*.
>- During constructor overload resolution, braced initializers are matched to std::initializer_list parameters if at all possible, even if other constructors offer seemingly better matches.
 >-  An example of where the choice between **parentheses** and **braces** can make a significant difference is creating a `std::vector<numeric type>` with two arguments. 
 >- Choosing between **parentheses** and **braces** for object creation inside **templates** can be challenging

  


