---
Created Date: 2026-02-23
tags:
  - cpp
  - programming
---
---

## A declaration introduces its name into a scope:

- **Local scope:** A name declared in a function (§1.3) or lambda (§6.3.2) is called a local name. Its scope extends from its point of declaration to the end of the block in which its declaration occurs. A block is delimited by a { } pair. Function argument names are considered local names.

- **Class scope:** A name is called a member name (or a class member name) if it is defined in a class , outside any function (§1.3), lambda (§6.3.2), or enum class. Its scope extends from the opening { of its enclosing declaration to the end of that declaration.

- **Namespace scope:** A name is called a namespace member name if it is defined in a name space (§3.4) outside any function, lambda (§6.3.2), class (§2.2, §2.3, Chapter 4), or enum class (§2.5). Its scope extends from the point of declaration to the end of its namespace. A name not declared inside any other construct is called a global name and is said to be in the global namespace.