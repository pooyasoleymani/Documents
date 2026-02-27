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

