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
2. need types can add to value *(+=)*.

> *typename* is last constraining , requiring only that the argument be a type.


```cpp
template<Sequence Seq, Value V>
requiers Arithmetic<value_type<Seq>, V>
Value sum(Seq s, V v);
```

- `Arithmetic<value_type<Seq>, V>` is called *requirements-clause*  


We can write code like this:
```cpp
template<typename Sequence, typename Number>
requires Arithmetic<Value_type<Sequence>,Number>
Number sum(Sequence s, Number n);
```




>[!NOTE]
>In C++ concepts, `std::ranges::forward_range` requires iterators that meet the Forward Iterator requirements, while `std::ranges::random_access_range` requires iterators that meet the Random Access Iterator requirements. The concept `std::sortable` specifically requires Random Access Iterators because sorting algorithms often need to perform random access.


### Version:0.9 StartHTML:0000000105 EndHTML:0000000320 StartFragment:0000000141 EndFragment:0000000280

Concept-based Overloading
