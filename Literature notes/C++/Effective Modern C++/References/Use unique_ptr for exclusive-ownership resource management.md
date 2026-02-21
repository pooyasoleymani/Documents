---
Created Date: 2026-02-17
tags:
  - cpp
  - programming
Next: "[[Use shared_ptr for shared-ownership resource management]]"
---
---
## What is unique_ptr ?
- *unique_ptr* is a *smart pointer* that have same size as *raw pointer* .
- It *small* enough and *fast* enough for use.
- It have own *resource management (RII)* .
- *std::unique_ptr* embodies *exclusive ownership semantics*. A *non-null* *std:: unique_ptr* always owns what it points to. Moving a *std::unique_ptr* transfers ownership from the source pointer to the destination pointer.
##### **std::unique_ptr** is thus a *move-only* type.

- **unique_ptr**  use *delete* for destroy object but we can configure *custom deleters*  : arbitrary functions (function object, lambda function) 

## Exceptions:

- If **exception** propagates out of the *thread*'s primary function.
- If a **noexcept** specification is violated.
- If *std::abort* , *std::Exite*, *std::exit*, *std::quick_exit* is called.

## Use Case
A common use for *std::unique_ptr* is as a *factory function* _return type_ for objects in a *hierarchy*:

```cpp
class Investmenty {...};

class Stock: public Investmnet {...};
class Bond: public Investmnet {...};
class RealEstate: public Investmnet {...};
```

```mermid

```
