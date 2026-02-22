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



- *Moving* **std::shared_ptr** is faster than *copy* because in *move constructor* no *reference count* manipulation but set source pointer to *null*.


- **std::shared_ptr** support custom deleters.
```cpp
auto loggingDel = [](Widget* pw) 
{
	makeLogEnrty(pw);
	delete pw;
};

std::unique_ptr<Widget, decltype(loggingDle)> 
upw(new Widget, loggingDel); // deleters is part of type

std::shared_ptr<Widget> spw(new Widget, loggingDel);
// deleters is not part of type
```


- **std::shared_ptr** with same type can have different deleters:
```cpp
auto customDel1 = [](Widget* pw) {...};
auto customDel2 = [](Widget* pw) {...};

std::shared_ptr<Widget> pw1(new Widget, customDel1);
std::shared_ptr<Widget> pw2(new Widget, customDel2);

// they can be placed in a container of objects of that type:
std::vector<std::shared_ptr<Widget>> vpw{ pw1, pw2 };
```


## Key Concepts

### Control Block
*larger data structure* known as the **control block** contain:
1. *reference count*
2. a copy of the *custom deleter*, if one has been specified.
3. If a *custom allocator* was specified, the control block contains a copy of that, too.
4. A secondary reference count known as the *weak count*(Weak reference).


### std::make_shared
**std::make_shared** always create a *control block* if that object was new.


### unique_ptr -> shared_ptr
A *control block* is created when a *std::shared_ptr* is constructed from a *unique-ownership pointer* (i.e., a *std::unique_ptr* or *std::auto_ptr*).


### std::shared_ptr construct with raw pointer
When a **std::shared_ptr** constructor is called with a *raw pointer*, it creates a *control block*. If you wanted to create a **std::shared_ptr** from an object that already had a *control block*, you’d presumably pass a **std::shared_ptr** or a *std::weak_ptr* (see Item 20) as a constructor argument, not a *raw pointer*.
```cpp
auto pw = new Widget;

std::shared_ptr<Widget> spw1(pw, loggingDel1); // create control blcok
std::shread_ptr<Widget> spw2(pw, loggoingDle2); // create 2nd cntrol block
```

- Direct use of *new* and use *spw1* with copy construct:
```cpp
std::shared_ptr<Widget> spw1(new Widget, loggingDel);
std::shared_ptr<Widget> spw2(spw1); // use same control block
```

- using *raw pointer* variables as **std::shared_ptr** constructor arguments can lead to multiple *control blocks* involves the *this* pointer

```cpp
std::vector<std::shared_ptr<Widget>> processedWidgets;

class Widget {
	public:
	void process();
};

/*
**This code will compile, but it’s passing a raw
** pointer (this) to a container of std::shared_ptrs
** create a new control block for the pointed-to Widget (*this).
*/
void Widget::process() {
 ...
 processedWidgets.emplace_back(this);
};
```

```cpp
// Widget would inherit from std::enable_shared_from_this as follows:

class Widget: public std::enable_shared_from_this<Widget> 
{
 void process();
};


void Widget::process()
{
// as before, process the Widget
// add std::shared_ptr to current object to processedWidgets
processedWidgets.emplace_back(shared_from_this());
}
```
- **std::enable_shared_from_this** is *Base class* and type parameter is *Driven class* the name of this pattern is The [[ Curiously Recurring Template Pattern (CRTP)]]


#### ⚠️Critical Requirement:
The object **must already be owned by a `shared_ptr`** before calling `shared_from_this()`. If not, behavior is undefined (typically throws `std::bad_weak_ptr`).

##### 🔒 Enforcing Safety: Factory Pattern
To prevent misuse (calling `shared_from_this()` before a `shared_ptr` owns the object), enforce creation _only_ through `shared_ptr`:

```cpp
class Widget : public std::enable_shared_from_this<Widget> {
public:
    // Factory function returns shared_ptr
    template<typename... Ts>
    static std::shared_ptr<Widget> create(Ts&&... params) {
        return std::make_shared<Widget>(std::forward<Ts>(params)...);
    }

    void process() { /* ... shared_from_this() safe here ... */ }

private:
    Widget(/* params */) { /* ... */ } // Private constructor
};


// Usage:
auto w = Widget::create(); // Only way to create Widget
w->process();
```

---
### Understanding the Costs and Limitations of `std::shared_ptr`
|                         |                                 |                                                                                                            |
| ----------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Control block size**  | ~3 words (24 bytes on 64-bit)   | With default deleter/allocator and `std::make_shared`                                                      |
| **Allocation overhead** | Often _free_                    | `make_shared` allocates object + control block in one memory block (see Item 21 in _Effective Modern C++_) |
| **Dereferencing**       | Same as raw pointer             | No overhead for `*ptr` or `ptr->member`                                                                    |
| **Reference counting**  | 1–2 atomic ops per copy/destroy | Maps to single CPU instructions (e.g., `LOCK XADD`); cheap but not free                                    |
| **Virtual function**    | One-time cost at destruction    | Used internally to invoke correct deleter; negligible in practice                                          |


#### ⚠️ Critical Limitations of `std::shared_ptr`
1. **No native array support**  
	Unlike `std::unique_ptr<T[]>`, there is **no** `std::shared_ptr<T[]>`. Attempts to work around this are dangerous
	
	
2. **Irreversible ownership**
	Once an object is managed by shared_ptr, you cannot reclaim exclusive ownership—even if `use_count() == 1`



#### ✅ Practical Recommendations
1. **Prefer `std::make_shared`**
```cpp
auto w = std::make_shared<Widget>(args...); // ✅ one allocation
auto w = std::shared_ptr<Widget>(new Widget(args...)); // ❌ Two allocations
```

2. **Use factory functions with `enable_shared_from_this`**  
    Ensures objects are _always_ created via `shared_ptr`, preventing `shared_from_this()` misuse.

3. **Default to `unique_ptr`**  
    Start with exclusive ownership; upgrade to `shared_ptr` only when truly needed.
4. **Avoid `shared_ptr` for arrays**  
    Use `std::vector` instead. If you must manage raw arrays, `unique_ptr<T[]>` is safer and more ergonomic.


---

>[!IMPORTANT] **Things to Remember**
>- **std::shared_ptrs** offer convenience approaching that of *garbage collection* for the shared lifetime management of arbitrary resources.
>-  Compared to **std::unique_ptr**, **std::shared_ptr** objects are typically twice as big, incur overhead for *control blocks*, and require *atomic* reference count manipulations.
>- Default resource destruction is via delete, but *custom deleters* are supported. The type of the deleter has no effect on the type of the **std::shared_ptr**. 
>-  Avoid creating **std::shared_ptrs** from variables of *raw pointer* type.

