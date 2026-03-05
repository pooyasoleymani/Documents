---
Created Date: 2026-01-28
tags:
  - cpp
  - programming
Next: "[[Declare functions noexcept if they won’t emit exceptions]]"
---
---

- **const_iterators** are the *STL equivalent* of *pointers-to-const*.

```cpp
std::vector<int> values;

std::vector<int>::iterator it = std::find(values.begin(), values.end(), 1998);
values.insert(it, 1998);

// But iterators aren’t really the proper choice here, because this code never modifies what an iterator points to.

typedef std::vector<int>::iterator IterT;
typedef std::vector<int>::const_iterator ConstIterT;

std::vector<int> values;
ConstIterT ci = std::find(static_cast<ConstIterT>(values.begin()), static_cast<ConstIterT>(values.end()), 1998);

values.insert(static_cast<IterT>(ci), 1998); // may not compile
```



>[!NOTE]
>there’s no portable conversion from a **const_iterator** to an **iterator**, not even with a
**static_cast**. Even the semantic sledgehammer known as **reinterpret_cast** can’t do the job.



- The container member functions **cbegin** and **cend** produce **const_iterators**, even for non-const containers, and STL member functions that use *iterators* to identify positions.

```cpp
std::vector<int> values; // as before

auto it = std::find(values.cbegin(),values.cend(), 1983); // use cbegin
values.insert(it, 1998);

// we could generalize the code we’ve been working with into a findAnd Insert template as follows:

template<typename C, typename V>
void findAndInsert(C& container, // in container, find
const V& targetVal, // first occurrence
const V& insertVal) // of targetVal, then
{ // insert insertVal

using std::cbegin; // there
using std::cend;

auto it = std::find(cbegin(container),cend(container),targetVal); 
// non-member cend and cbegin
container.insert(it, insertVal);
}
```



- implementation of *non-member* **cbegin**:
```cpp
template <class C>
auto cbegin(const C& container) -> decltype(std::begin(container))
{
	return std::begin(container);
}
```

---


>[!IMPORTANT] **Things to Remember**
>• Prefer *const_iterators* to *iterators*.
• In maximally generic code, prefer non-member versions of *begin*, end, *rbegin*, etc., over their member function counterparts.



---
Reff: [[Iterator vs Pointer]], [[Random Access Iterator]], [[Forward Iterator]],[[Concepts and Generic Programming]]