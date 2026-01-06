---
Up: "[[Effective Modern C++17]]"
Related: "[[Understand template type deduction]]"
Created Date: 2026-01-05
tags:
  - cpp
  - programming
---
---

C++98 had a single set of rules for type deduction: the one for **function templates**.
C++11 modifies that ruleset a bit and adds two more, one for **auto** and one for **decltype**.
C++14 then extends the usage contexts in which auto and **decltype** may be employed.

##### Why it is important?
It makes C++ software more adaptable, because changing a type at one point in the source code automatically propagates through type deduction to other locations.
However, it can render code more difficult to reason about, because the types deduced by compilers may not be as apparent as you’d like.


> [!NOTE] 
> There are just too many contexts where type deduction takes place: in calls to function templates, in most situations where **auto** appears, in **decltype** expressions, and, as of C++14, where the enigmatic **decltype(auto)** construct is employed
