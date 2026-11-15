---
Created Date: 2026-02-17
tags:
  - cpp
  - programming
Next: "[[Smart Pointers]]"
---
---

- Generated *special member functions* are implicitly public and **inline**, and they’re nonvirtual unless the function in question is a *destructor* in a derived class inheriting from a base class with a *virtual destructor*.

## What are "Special Member Functions"?
- **C++98 had 4:**
    1. Default Constructor
    2. Destructor
    3. Copy Constructor
    4. Copy Assignment Operator
- **C++11 added 2 more:**
    5. Move Constructor
    6. Move Assignment Operator


## The Core Rule: "If you touch one, you affect the others"
In *C++98*, the rules were simple. In *C++11*, the rules became stricter to prevent bugs and performance issues. The generation of these functions depends on what **you** declare.
1. You declare **no** copy operations.
2. You declare **no** move operations.
3. You declare **no** destructor.

**Why?**

- **Move vs. Copy:** If you write a custom Copy Operation, the compiler assumes the default "memberwise copy" isn't good enough. Therefore, it assumes the default "memberwise move" probably isn't good enough either, so it won't generate moves.
- **Move vs. Move:** If you write a Move Constructor, the compiler assumes you know something special about moving this class. It won't generate a Move Assignment Operator because it assumes your special logic applies there too.
- **Destructor Impact:** If you write a Destructor, the compiler assumes you are managing resources (like memory). In C++98, this didn't stop copy operations. In C++11, writing a destructor **prevents the compiler from generating Move Operations.**

### 3. The "Rule of Three" Evolution

- **C++98 Rule of Three:** If you need to write a Destructor, Copy Constructor, or Copy Assignment, you should write all three. This is usually because you are managing resources (like dynamic memory).
- **C++11 Reality:** Because writing a Destructor now suppresses Move Operations, the "Rule of Three" effectively becomes the **"Rule of Five"** (Destructor + 2 Copy + 2 Move).

### 4. The Dangerous Pitfall (The `StringTable` Example)

The text highlights a specific performance trap.

1. **Scenario:** You have a class with a `std::map` inside. You don't write any special functions.
    - _Result:_ Compiler generates Move Operations. Moving a `std::map` is very fast.
2. **Change:** You decide to add logging. To log when the object dies, you add a **Destructor**.
    - _Result:_ Because you declared a Destructor, the compiler **stops generating Move Operations**.
3. **The Bug:** Your code still compiles. When you try to "move" the object, the compiler falls back to **Copying** it (because copy operations are still generated).
    - _Consequence:_ Copying a large `std::map` is orders of magnitude slower than moving it. You introduced a massive performance regression just by adding a log line in the destructor.

### 5. The Solution: `= default`

To fix the pitfall above, you should explicitly tell the compiler to generate the functions even if you wrote a destructor.

```cpp
class Base {
public:
    virtual ~Base() = default; // You declare the dtor (needed for polymorphism)
    
    // But you explicitly ask the compiler to generate the rest:
    Base(Base&&) = default; 
    Base& operator=(Base&&) = default;
    Base(const Base&) = default;
    Base& operator=(const Base&) = default;
};
```

Using `= default` makes your intentions clear and ensures you don't accidentally lose move semantics when you add a destructor.

### 6. A Note on Templates

If you write a **function template** that _looks_ like a copy constructor (e.g., `template<typename T> Widget(const T& rhs)`), the compiler **will still generate** the real special member functions. Templates do not count as user-declared special member functions.

### Summary Checklist (Things to Remember)

- **Special Member Functions:** Default Ctor, Dtor, Copy Ctor, Copy Assign, Move Ctor, Move Assign.
- **Move Generation:** Moves are **not** generated if you declare a Copy Operation, a Move Operation, or a Destructor.
- **Copy Generation:** Copies are **deleted** if you declare a Move Operation.
- **Deprecation:** Relying on the compiler to generate Copy Operations when you have declared a Destructor is deprecated (it still works, but don't do it).
- **Best Practice:** If you need a Destructor (e.g., for a virtual interface), use `= default` for the Copy and Move operations to ensure your class remains efficient and copyable/movable.
- **Templates:** Member function templates do not suppress the generation of special member functions.

### In Plain English

The compiler tries to be helpful by writing boilerplate code for you. However, in C++11, if you touch the engine (by writing a destructor or copy function), the compiler assumes you know what you're doing and stops helping with the **Move** functions. If you aren't careful, your program will silently switch from "fast moving" to "slow copying," hurting performance. Explicitly using `= default` tells the compiler: "I know I wrote a destructor, but please keep generating the fast move functions for me."


---
>[!IMPORTANT] **Things to Remember**
>- The special member functions are those compilers may generate on their own: **default constructor**, **destructor**, **copy operations**, and **move operations**.
>- **Move operations** are generated only for classes lacking explicitly declared **move operations**, **copy operations**, and a **destructor**.
>- The **copy constructor** is generated only for classes lacking an explicitly declared **copy constructor**, and it’s *deleted* if a **move operation** is declared. The **copy assignment** operator is generated only for classes lacking an explicitly declared **copy assignment** operator, and it’s deleted if a **move operation** is declared. Generation of the **copy operations** in classes with an explicitly declared **destructor** is deprecated.
>- Member function **templates** never suppress generation of special member functions.
