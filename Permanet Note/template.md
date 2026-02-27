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


