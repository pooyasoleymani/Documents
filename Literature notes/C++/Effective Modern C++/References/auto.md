---
Created Date: 2026-01-11
tags:
  - cpp
  - programming
Next: "[[Prefer auto to explicit type declarations]]"
---
---
In concept, **auto** is as simple as simple can be, but it’s more subtle than it looks. 
Using it saves typing, sure, but it also prevents correctness and performance issues that can bedevil manual type declarations. Furthermore, some of **auto**’s type deduction results, while dutifully conforming to the prescribed algorithm, are, from the perspective of a programmer, just wrong. 
When that’s the case, it’s important to know how to guide auto to the right answer, because falling back on manual type *declarations* is an alternative that’s often best avoided.