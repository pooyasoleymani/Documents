---
Created Date: 2026-02-17
tags:
  - cpp
  - programming
Next: "[[Use weak_ptr for std::shared_ptr like pointers that can dangle]]"
---
---
## What is std::shared_ptr ?

- **std::shared_ptr** in C++11 way to binding *Garbage collection* with *manual resource management* .
- An object accessed via **std::shared_ptrs** has its lifetime managed by those pointers through *shared ownership*.
- A **std::shared_ptr** can tell whether it’s the *last one pointing* to a resource by consulting the resource’s *reference count* ,a value associated with the *resource* that *keeps track* of how many **std::shared_ptrs** point to it.
- **std::shared_ptr** *constructors* increment this *reference count*.
- **std::shared_ptr** *destructor* decrement this *reference count*.
- **std::shared_ptr** *copy-constructor* do both:
```cpp
std::shared_ptr<Type> sp1; // point to one object 1
std::shared_ptr<Type> sp2; // point to one object 2

sp1 = sp2; // copy constructor 
// sp1 reference count -1
// sp2 reference count +1
```

- **std::shared_ptrs** are *twice* the size of a *raw pointer*, because they internally contain a *raw pointer* to the resource as well as a raw pointer to the *resource’s reference count*.
- *Memory* for the *reference count* must be *dynamically allocated*: explains that the cost of the dynamic allocation is avoided when the **std::shared_ptr** is created by **std::make_shared**, but there are situations where **std::make_shared** can’t be used. Either way, the reference count is stored as dynamically allocated data.
- *Increments* and *decrements* of the *reference count* must be **atomic**, because there can be simultaneous readers and writers in different *threads*.

>[[ Atomic operations]] are typically slower than [[non-atomic operations]]


