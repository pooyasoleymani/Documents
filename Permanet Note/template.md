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

