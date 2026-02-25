---
tags:
  - linux
---
---
### 1. The Basics: lvalues vs. rvalues

| Feature        | **lvalue** (locator value)                                                | **rvalue** (read value)<br>                                                          |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Definition** | An object that has a **persistent identity** (a memory address).          | A **temporary** value that does not have a persistent identity.                      |
| **Lifetime**   | Lives until it goes out of scope.                                         | Lives only until the end of the full expression (usually).                           |
| **Address**    | You **can** take its address (`&x`).                                      | You **cannot** take its address (`&5` is illegal).                                   |
| **Assignment** | Can appear on the **left** side of `=`.                                   | Can only appear on the **right** side of `=`.                                        |
| **Examples**   | Variables (`x`), dereferenced pointers (`*p`), function returning `int&`. | Literals (`5`, `"hello"`), temporaries (`x + 1`), function returning `int` by value. |


### 2. Lvalue References (`T&`)
- Syntax: **Type& t**
- **Bind to lvalue**
- **Exception**: A `const T&` can bind to an rvalue (this extends the temporary's lifetime).
- **Purpose:** Avoid copying large objects when passing to *functions*; allow functions to modify arguments.

```cpp
int x = 10;
int& ref = x;    // ✅ OK: ref binds to lvalue 'x'
ref = 20;        // ✅ OK: modifies 'x'

int& ref2 = 5;   // ❌ ERROR: Cannot bind non-const lvalue ref to rvalue (literal 5)
const int& ref3 = 5; // ✅ OK: const lvalue ref CAN bind to rvalue
```

### 3. Rvalue References (`T&&`)
- **Syntax:** `Type&& name`
- **Binds to:** **rvalues** (temporaries).
- **Purpose:** Enable **Move Semantics**. It tells the compiler: _"This object is a temporary. It's about to be destroyed. I am allowed to steal its resources instead of copying them."_
```cpp
int x = 10;
int&& ref = 10;   // ✅ OK: ref binds to rvalue (literal)
int&& ref2 = x;   // ❌ ERROR: Cannot bind rvalue ref to lvalue 'x'
```

To bind an rvalue reference to an lvalue (like `x` above), you must cast it using `std::move`. This tells the compiler: _"Treat `x` as if it were a temporary. I promise I won't use it again."_

```cpp
int&& ref3 = std::move(x); // ✅ OK: 'x' is now treated as an rvalue
```


### 4. Why do we need Rvalue References? (Move Semantics)
This is the most important part.
Imagine a class that manages a large resource, like a `std::vector` or a file handle.

#### The Problem: Copying is Expensive
When you copy an object (using lvalue references), you must *allocate new memory* and copy all the data.


#### The Solution: Moving is Cheap

