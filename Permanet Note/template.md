---
Created Date: 2026-02-26
tags:
  - inbox
  - cpp
---
---
## What is Template?
**Template** class or function is [[compile-time]] mechanism for parameterized with set of types or values.

```cpp
template<typename T>
class Vector {
	private:
		T* elemnet;
		int size;
	public:
		explicit Vector(int s);
		~Vector() {delete[] element;}
	
		const T* operator[](int s) const;
}

// older version 
template<class T>
class Vector {
	...
}
```


> **Template** is [[compile-time]] mechanism so use incurs no [[run-time]] overhead compared to hand-craft code.



#### A **template** plus a set of **template arguments** is called an [[instantiation]] or a specialization. Late in the *compilation* process, at [[instantiation time]], code is generated for each instantiation used in a program .


>[!NOTE]
>a Template arguments is called an instantiation or a specialization. 
>Late in the compilation process ,at [[instantiation time]], code is generated for each instantiation used in a program .
>The code generated is **type checked** so that the generated code is as **type safe** as handwritten code .
>Type check often occurs late in the [[compilation process]], at [[instantiation time]]. 



### Value Template Arguments
In addition to type arguments, a template can take value arguments.

```cpp
template<typename T, int N>
struct Buffer {
	using value_type = T;
	constexpr int size() {return N;}
	T[N];
	// ... 
}
```
 

>[!IMPORTANT]
>The alias **value_type** and **constexpr** function are provided to allow users *read-only* access to the template arguments
>*Template value argument* must be a **constant expression**.




### Template Argument Deduction
[[Understand template type deduction]]

```cpp
auto p = make_pair(1.2, 5); // p is pair<double, int> 
std::pair p = {1.2, 5} //  p is pair<double, int>


template<typename T>
class Vector {
	public:
		Vector(int);
		Vector(initializ er_list<T>); // initializer-list constructor
// ...
};

Vector v1 {1,2,3}; // deduce v1’s element type from the initializer element type
Vector v2 = v1; // deduce v2’s element type from v1’s element type
auto p = new Vector{1,2,3}; // p points to a Vector<int>
Vector<int> v3(1); // here we need to be explicit about the element type (no element type is mentioned)
``` 




##### However, it is not a panacea. *Deduction can cause surprises* (both for make_ functions and constructors). Consider:

```cpp
Vector vs {"Hello", "World"}; // deduces to Vector<const char*>
```

##### deduction guide:
When compiler can't deducting type we can providing deducting guide

```cpp
template<typename T>
class Vector {
	public:
		using value_type = T;
		
		template<typename It>
		Vector(It b, It e);
}

template<typename It>
Vector(It b, It e) -> Vector<typename It::value_type>;
```



### Parameterized Operation

There are 3 way of expressing operation parameterized type or values:
1. A **Function template**
2. A **Function object**: an object that can carry data and be called like a function
3. A **Lambda expression**: a shorthand notation for a function object


#### 1. Function Template

```cpp

Value sum(const Sequence& s, Value v)
{
	for(auto x: s)
		v+=x;
	return v;
}
```


>[!IMPORTANT]
>A function template can be a member function, but not a **virtual member**.
>The compiler would not know all instantiations of such a template in a program, so it not generate a **vtbl**.



#### 2. Function Objects

The **Function object (functor)** use for defined objects that can be called like function.
and this object can carry data ans state: 

```cpp
template<typename T>
class LessThan {
	public:
		LessThan(const T& v): val{v} {}
		bool operator()(const T& x) const {return x < val;}
		
};
```


The function called **operator()** implements the *‘‘function call,’’* *‘‘call,’’* or *‘‘application’’* **operator ().** We can define named variables of type *Less_than* for some argument type:

```cpp
LessThan Iti{42}; // compare i with 42
LessThan Its {"Backus"s}; // compare i with Backus
```


#### 3. Lambda Expressions

The notation` [&](int a){ return a<x; } `is called a **lambda expression**. It generates a *function object*  exactly like `Less_than<int>{x}`.  The `[&]` is a capture list specifying that all local names used in the *lambda* body (such as x) will be accessed through references. Had we wanted to ‘‘capture’’ only x, we could have said so: `[&x]`. Had we wanted to give the generated object a copy of x, we could have said so: `[=x]`. Capture nothing is `[ ]`, capture all local names used by reference is `[&]`, and capture all local names used by value is `[=]`.
Using lambdas can be convenient and terse, but also obscure. For nontrivial actions (say, more
than a simple expression), I prefer to name the operation so as to more clearly state its purpose and
to make it available for use in several places in a program.

```cpp
void User2() {
	vector<std::unique_ptr<Shape>> v;
	while(cin)
		v.push_back(read_shape(cin));
	for_all(v, [](std::unique_ptr<Shape>& ps){ps->draw();});
	for_all(v, [](std::unique_ptr<Shape>& ps){ps->rotate(45);});
}


// Like a function, a lambda can be generic. For example:

template<class S>
void rotate_and_draw(vector<S>& v, int r)
{
	for_all(v,[](auto& s){ s−>rotate(r); s−>draw(); });
}
```


>[!NOTE]
>**Lambda** with *auto* parameter a template , is **a generic lambda**.
>



### Template Mechanisms
To define good templates, we need some supporting language facilities:

- Values dependent on a type: *variable templates* .
- Aliases for types and templates: *alias templates* .
- A compile-time selection mechanism: *if constexpr* .
- A *compile-time* mechanism to inquire about properties of types and expressions: *requires expressions* (§7.2.3).
- In addition, *constexpr functions* and *static_asserts*  often take part in template design and use.
These basic mechanisms are primarily tools for building general, foundational abstractions.


#### Variable Template 
We can define constant or variables of type **T** and other types depending on **T**.

```cpp
template<class T>
	constexpr T viscosity = 0.4;

template<class T> 
	constexpr scpace_vector<T> exteranl_acceleration = {T{}, T{-9.8}, T{}};

auto vis2 = 2 * viscosity<double>;

template<typename T, typename T2>
	constexpr Assignable = is_assignable<T&, T2>::value;

template<typename T> 
	void test()
	{
		static_assert(Assignable<T&, double>, "can't assign a double");
		static_assert(Assignble<T&, string>, "can't assign a string");
	}

```

#### Alias Template
Modern use of *typedef* in C++11 and later.
With type alias we can write portable codes.
*Example*: **value_type** in STD 

```cpp
template<typename T>
	using Value_type = typename T::value_type;
	
template<typename Container>
void algo(Container& c)
{
	Vector<Value_type<Container>> vec;
}
```

#### Compile-Time **if**

```cpp
template<typename T>
void Update(T& target)
{
	// ...
	if constexpr(is_pod<T>::value)
		simple_and_fast(target);
	else
		slow_and_safe(target);
	// ...
}
```



>[!IMPORTANT]
>Importantly, an **if constexpr** is not a **text-manipulation** mechanism and *cannot* be used to break the usual rules of grammar, type, and scope.
>```cpp
>template<typename T>
>void bad(T arg)
>{
> 	// ...
> 	if constexpr(Something<T>::value)
> 		try {
> 		// ...	
> 		}
> 		catch(...) {/* ... */}
> } // syntax error
> ```






