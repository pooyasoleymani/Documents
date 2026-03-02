---
Created Date: 2026-03-02
tags:
  - inbox
  - cpp
---
---

## Generic Programming
That means that algorithms can be designed to accept a wide variety of types(classes) as long as they meet the algorithm's requirements on its arguments.
- *Template* in C++ is main support for **generic programming** . 
- *Template* provide ([[compile-time]]) parametric polymorphic.


### Key Problems

Consider *sum()* in below:
```cpp
template<typename Seq, typename Num>
Num sun(Seq s, Num v)
{
	for(auto& x: s)
		v += s;
	return v;
}
```

1. we need data structure that support *begin()* and *end()* so support *for-loop* .
2. 