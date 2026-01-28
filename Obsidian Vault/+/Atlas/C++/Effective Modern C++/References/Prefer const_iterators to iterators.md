---
Created Date: 2026-01-28
tags:
  - cpp
  - programming
Up: "[[Declare overriding functions override]]"
Next:
Home: "[[Effective Modern C++17]]"
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

