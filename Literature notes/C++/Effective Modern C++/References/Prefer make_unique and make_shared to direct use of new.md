---
Created Date: 2026-02-22
tags:
  - cpp
  - programming
Next: "[[When using the Pimpl Idiom, define special member functions in the implementation file]]"
---
---

**Stop writing `new` when creating smart pointers. Use the factory functions instead.**



### 1. Exception Safety (The Most Important Reason)

The primary technical reason for this rule is to prevent memory leaks in the event of an exception.

#### The Problem with `new`

Consider a function call where you create a smart pointer directly using `new` as an argument:

```cpp
// DANGEROUS CODE
processWidget(std::shared_ptr<Widget>(new Widget), priority());
```

In C++, the order in which function arguments are evaluated is **unspecified**. The compiler might do this:

1. Execute `new Widget` (Memory is allocated).
2. Execute `priority()` (This function throws an exception!).
3. Construct the `std::shared_ptr` (Never happens because of the exception).

**Result:** The memory allocated by `new Widget` is lost because the `shared_ptr` that was supposed to manage it was never created. This is a **memory leak**.


#### The Solution with `make_shared`
```cpp
// SAFE CODE
processWidget(std::make_shared<Widget>(), priority());
```

`std::make_shared` creates the object _and_ the smart pointer control block in a single expression.

1. `std::make_shared<Widget>()` is fully evaluated (object created, pointer created).
2. `priority()` is evaluated.

If `priority()` throws, the temporary `shared_ptr` created in step 1 goes out of scope and its destructor automatically frees the memory. **No leak.**


### 2. Code Clarity and Conciseness

Using `make_` functions reduces verbosity and eliminates type duplication.

**Direct `new`:**
```cpp
std::unique_ptr<Widget> upw(new Widget);
std::shared_ptr<Widget> spw(new Widget);
```

- You have to type the type (`Widget`) twice.
- You have to mix `new` syntax with smart pointer syntax.

**Using `make_`:**
```cpp
auto upw = std::make_unique<Widget>();
auto spw = std::make_shared<Widget>();
```
- You use `auto`, so the type is written once (in the template argument).
- It is immediately obvious that you are creating a managed object.


### 3. Performance (`std::make_shared` specific)

`std::make_shared` offers a performance optimization over direct `new` with `shared_ptr`.

- **Direct `new`:** Requires **two** memory allocations.
    1. One for the object (`Widget`).
    2. One for the control block (reference counts, weak counts, etc.).
- **`std::make_shared`:** Requires **one** memory allocation.
    1. It allocates a single chunk of memory that holds both the `Widget` and the control block.

**Benefits:**

- Faster allocation (one call to the allocator instead of two).
- Better cache locality (the object and its reference counts are next to each other in memory).

_(Note: `std::make_unique` does not offer this specific allocation optimization, but it still provides exception safety and clarity.)_



---

### 4. When NOT to use them (The Caveats)

While you should prefer `make_` functions 95% of the time, there are three specific scenarios where you must use direct `new` with the smart pointer constructor:

#### A. You need a Custom Deleter

`std::make_shared` and `std::make_unique` do not support custom deleters.
```cpp
// You cannot do this with make_shared
auto sp = std::shared_ptr<Widget>(new Widget, getDeleter()); 
```


#### B. You want to use Brace Initialization (`{}`)
Sometimes template argument deduction with `make_` functions conflicts with brace initialization.

```cpp
// Ambiguous: Is {1, 2, 3} for the vector or for make_shared?
auto sp = std::make_shared<std::vector<int>>({1, 2, 3}); // Might fail to compile

// This works clearly
auto sp = std::shared_ptr<std::vector<int>>(new std::vector<int>{1, 2, 3});
```


#### C. You are using `weak_ptr` and care about memory lifetime
This is an advanced edge case.

- With `make_shared`, the object and the control block are in the same memory allocation.
- The memory cannot be freed until **both** the `shared_ptr` count AND the `weak_ptr` count go to zero.
- If you have long-lived `weak_ptr`s, the object's memory will stay allocated even after the object is "destroyed" (shared count = 0).

If you need the object's memory to be freed immediately when the last `shared_ptr` dies (regardless of `weak_ptr`s), you must use direct `new`. This separates the object's memory from the control block's memory.


---
**Bottom Line:** Unless you have a specific need for a custom deleter, brace initialization issues, or specific `weak_ptr` memory management, **always use `std::make_unique` and `std::make_shared`.**



---
