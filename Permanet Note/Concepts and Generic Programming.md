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


### Concept-based Overloading

we can *overload based* on their properties, much as we do for functions. Consider a slightly simplified *standard-library* function **advance()** that advances an *iterator*:

```cpp
template<Forward_Iterator Iter>
void advance(Iter it, int n)
{
	while(n--)
		++p; // forward iterator has ++, but not += or +
} 

template<Random_Access_Iterator Iter>
void advance(Iter it, int n)
{
	p += n;
}

void user(vector<int>::iterator vip, list<string>::iterator lsp)
{
	advance(vip, 10);
	advance(lsp, 10);
}

```

>[!IMPORTANT]
> Like other overloading , this is [[compile-time]] mechanism implying no [[run-time]] cost and where the compiler does not  find best choice it gives an **ambiguity error**.



#### Consider first a *single argument* for several *alternative functions*:

• If the *argument* doesn’t match the **concept**, that alternative cannot be chosen.
• If the *argument* matches the **concept** for just one alternative, that alternative is chosen.
• If *arguments* from two alternatives are equally good matches for a **concept**, we have an ambiguity.
• If *arguments* from two alternatives match a **concept** and one is stricter than the other (match all the *requirements* of the other and more), that alternative is chosen.

#### For an alternative to be chosen it has to be
• a match for all of its arguments, and
• at least an equally good match for all arguments as other alternatives, and
• a better match for at least one argument.
