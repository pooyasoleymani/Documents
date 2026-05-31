---
Created Date: 2026-02-24
tags:
  - cpp
  - programming
Next: "[[Distinguish universal references from rvalue references]]"
---
---
## Key Concepts

-  **Move semantics** makes it possible for compilers to replace *expensive copying* operations with less expensive *moves*. In the same way that copy constructors and copy assignment operators give you control over what it means to copy objects, move constructors and move assignment operators offer control over the semantics of moving. Move semantics also enables the creation of *move-only types*, such as *std::unique_ptr*, *std::future*, and *std::thread*.

-  **Perfect forwarding** makes it possible to write *function templates* that take arbitrary arguments and forward them to other functions such that the target functions receive exactly the same arguments as were passed to the forwarding functions.


