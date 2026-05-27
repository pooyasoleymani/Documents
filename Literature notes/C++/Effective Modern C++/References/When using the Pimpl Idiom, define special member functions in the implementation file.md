---
Created Date: 2026-02-24
tags:
  - cpp
  - programming
Next: "[[Rvalue References, Move Semantics, and Perfect Forwarding]]"
---
---
 ##### If you use **std::unique_ptr** for your **Pimpl pointer**, you cannot let the *compiler* generate your class's *destructor* (and other *special members*) in the *header* file. You must define them in the *source* (.cpp) file.


### 1. The Context: What is the Pimpl Idiom?
The **Pimpl Idiom** is used to hide implementation details, reduce *compilation dependencies*, and maintain *binary compatibility*. It looks like this:

**widget.h**
```cpp
class Widget {
public:
	Widget();
	// other methods.
	
private:
	struct Impl;
	std::unique_ptr<Ipml> pImpl;
}
```


**widget.cpp**
```cpp

struct Impl {
	std::string name;
	int id;
};

Widget::Widget(): pImml(std::make_unique<Impl>())
```


### 2. The Problem: Incomplete Types and `unique_ptr`
The issue arises when the `Widget` object is destroyed.

1. When a `Widget` is destroyed, its member `pImpl` (the `std::unique_ptr`) must also be destroyed.
2. When `std::unique_ptr<Impl>` is destroyed, it calls `delete` on the raw `Impl*` pointer it holds.
3. **Crucial Rule:** To call `delete` on a pointer, the compiler **must know the complete definition** of the type (`Impl`) at that point. It needs to know the size of the object and which destructor to call.
4. **The Conflict:** In `widget.h`, `Impl` is only **forward-declared**. It is an **incomplete type**. The full definition exists only in `widget.cpp`.


#### The "Wrong" Way (Header-only Destructor)
If you let the *compiler* generate the *destructor* in the header (either implicitly or via `= default`):

```cpp
// widget.h
class Widget {
public:
    ~Widget() = default; // DANGER!
private:
    struct Impl;
    std::unique_ptr<Impl> pImpl;
};
```

**What happens:** The *compiler* tries to generate the code for `~Widget()` right there in the *header*. It sees `pImpl` needs to be *destroyed*. It tries to generate the code to `delete` the `Impl` *pointer*. But it doesn't know what `Impl` is yet (it's *incomplete*). 
**Result:** **Compilation Error.** (e.g., "invalid application of *'sizeof'* to *incomplete* type *Widget::Impl*").



### 3. The Solution: Define Special Members in the `.cpp`
To fix this, you must prevent the *compiler* from generating the *destructor* in the header. You do this by *declaring* the *destructor* in the header but **defining** it in the source file, where `Impl` is a complete type.

#### The "Right" Way

**widget.h**
```cpp
class Widget {
public:
    Widget();
    ~Widget(); // 1. Declare only (do NOT = default here)

    // Copy/Move operations also need care (see below)
    Widget(const Widget&); 
    Widget& operator=(const Widget&);
    Widget(Widget&&);
    Widget& operator=(Widget&&);

private:
    struct Impl;
    std::unique_ptr<Impl> pImpl;
};
```

**widget.cpp**
```cpp
struct Widget::Impl { /* ... */ };

Widget::Widget() : pImpl(std::make_unique<Impl>()) {}

// 2. Define the destructor here, where Impl is complete
Widget::~Widget() = default; 

// 3. Define Copy/Move here too
Widget::Widget(const Widget& rhs) 
    : pImpl(std::make_unique<Impl>(*rhs.pImpl)) {} // Deep copy

Widget& Widget::operator=(const Widget& rhs) {
    *pImpl = *rhs.pImpl; 
    return *this;
}

// Move operations can be defaulted here
Widget::Widget(Widget&&) = default;
Widget& Widget::operator=(Widget&&) = default;
```


**Why this works:** When the compiler compiles `widget.cpp`, it sees the full definition of `struct Widget::Impl`. Therefore, when it compiles `Widget::~Widget()`, it knows exactly how to delete the `Impl` object managed by `pImpl`.

### 4. Handling Copy and Move Operations

Because `std::unique_ptr` is move-only, the compiler-generated copy constructor and copy assignment operator would try to copy the `unique_ptr`, which is deleted. This causes a compilation error even if the type was complete.

- **If `Widget` should be copyable:** You must manually implement the copy constructor and assignment operator in the `.cpp` file to perform a **deep copy** of the `Impl` object (as shown in the code above).
- **If `Widget` should be movable:** You can default the move operations, but you **must still define them in the `.cpp` file**. If you default them in the header, the compiler tries to generate them immediately, encounters the incomplete `Impl` type inside the `unique_ptr` logic, and fails.



### 5. Exception: `std::shared_ptr`
If you use `std::shared_ptr` for your Pimpl pointer instead of `std::unique_ptr`, **this rule does not apply.**

```cpp
// This IS safe in the header
std::shared_ptr<Impl> pImpl; 
~Widget() = default; 
```

**Why?** `std::shared_ptr` stores its deleter (the code that knows how to delete `Impl`) inside the control block at the time the `shared_ptr` is created (usually in the constructor). By the time the `shared_ptr` destructor runs, it already has the function pointer needed to delete the object. It does not need the complete type of `Impl` at the point where the `Widget` destructor is defined.

However, using `unique_ptr` is generally preferred for Pimpl because it implies exclusive ownership and has slightly less overhead.


---

### Summary Checklist

When using Pimpl with `std::unique_ptr`:

1. **Forward declare** the Impl struct in the header.
2. **Declare** the destructor, copy constructor, copy assignment, move constructor, and move assignment in the header (do not `= default` them there).
3. **Define** all of these special member functions in the `.cpp` file.
4. In the `.cpp` file, you can `= default` the destructor and move operations, but you must manually implement copy operations if copyability is desired.

**Mnemonic:** "Pimpl with `unique_ptr` needs the full picture to clean up. Give it the picture in the `.cpp`."
