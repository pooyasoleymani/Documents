---
Created Date: 2026-02-25
tags:
  - cpp
  - programming
Next:
---
---
**`std::move` and `std::forward` do not move or forward anything. They are cast functions.**



### 1. `std::move`: The Unconditional Cast

**What it does:**
`std::move` takes an object (usually an lvalue) and **unconditionally casts it to an rvalue reference**.

**Why use it:**
To tell the compiler: _"I am done with this object. Treat it as a temporary so you can steal its resources (move) instead of copying them."_


**How it works:**
```cpp
template<typename T>
typename std::remove_reference<T>::type&& move(T&& param) {
	using ReturnType = typename std::remove_reference<T>::type&&;
	return static_cast<ReturnType>(param);
}

// C++14
template<typename T>
decltype(auto) move(T&& param) {
	using ReturnType = typename std::remove_reference<T>::type&&;
	return static_cast<ReturnType>(param);
} 

```

_(Simplified: It basically does `static_cast<T&&>(obj)`.)_


**When to use `std::move`:**

1. **Non-template code:** When you have a named rvalue reference parameter and want to pass it along as an rvalue.
2. **Explicitly triggering a move:** When you know an object is no longer needed and want to avoid a copy.



### 2. `std::forward`: The Conditional Cast
**What it does:**
`std::forward` casts an object to an rvalue reference **only if the original argument passed to the template was an rvalue**. If the original argument was an lvalue, it casts to an lvalue reference.

**Why use it:** 
For **Perfect Forwarding** in *templates*. It preserves the *"value category"* (lvalue vs. rvalue) of an argument as it passes through a function wrapper.

```cpp
template<typename T> 
T&& forward(typename std::remove_reference<T>::type& param) {
	return static_cast<T&&>(param);
}
```

_(Note: It requires a template type parameter `T` to know how to cast.)_


**Example:**
Imagine a wrapper function that logs arguments and passes them to another function.


```cpp
template<typename T> 
void wrapper(T&& param) {
	**std::cout << "Logging...\n";
    // If 'arg' was passed as an lvalue, forward returns T& (lvalue)
    // If 'arg' was passed as an rvalue, forward returns T&& (rvalue)
    process(std::forward<T>(arg));
}
```

If you used `std::move(arg)` here, you would **always** cast to an rvalue, even if the caller passed an lvalue. That would force a move (potentially invalidating the caller's variable) when they expected a copy. `std::forward` prevents this.


**When to use `std::forward`:**

1. **Template code:** Specifically when dealing with **Universal References** (`T&&` in a template).
2. **Forwarding arguments:** When passing parameters to another function inside a template.


### 3. Decision Matrix: Which one to use?
|Scenario|Function Type|Parameter Type|Goal|Use|
|---|---|---|---|---|
|**Non-Template**|Regular Function|`Widget&& w`|Pass `w` to another function as an rvalue|`std::move(w)`|
|**Template**|Template Function|`T&& t` (Universal Ref)|Pass `t` preserving its original category|`std::forward<T>(t)`|
|**Template**|Template Function|`T& t` or `const T& t`|Pass `t` (no moving intended)|Neither (pass `t`)|

**Meyers' Rule of Thumb:**

- Use **`std::move`** on **rvalue references** (in non-template code).
- Use **`std::forward`** on **universal references** (in template code).




### 4. Critical Pitfalls & Warnings

#### A. `std::move` on a `const` Object

If you apply `std::move` to a `const` object, you get a `const T&&`.
- Move constructors usually take `T&&` (non-const).
- Copy constructors take `const T&`.
- **Result:** A `const T&&` binds to the **Copy Constructor**, not the Move Constructor.
- **Lesson:** `std::move` a `const` object results in a **copy**, not a move.

```cpp
const std::string s = "Hi";
std::string s2 = std::move(s); // Copies! Cannot steal from const.
```

#### B. Using `std::move` Inside Templates (Instead of `forward`)

If you have a universal reference `T&& param` inside a template and you use `std::move(param)`:
- You force `param` to be treated as an rvalue.
- If the caller passed an lvalue, you just invalidated their variable unexpectedly.
- **Lesson:** Always use `std::forward<T>(param)` in templates.


#### C. Using an Object After `std::move`
As mentioned, the moved-from object is in a "valid but unspecified state."

```cpp
std::vector<int> v1 = {1, 2, 3};
std::vector<int> v2 = std::move(v1);
v1.push_back(4); // ⚠️ DANGER: v1 is empty/garbage. Behavior depends on implementation.
```


Only destroy `v1` or assign a new value to it after moving.


#### D. `std::move` Doesn't Actually Move
Remember: **`std::move` generates code that _permits_ moving.** The actual moving happens in the **Move Constructor** or **Move Assignment Operator** of the class. If a class doesn't have a move constructor, `std::move` will result in a copy (via the copy constructor).


### 5. Connection to Previous Items
- **Item 21 (`make_unique`):** Inside the implementation of `make_unique`, `std::forward` is used to perfectly forward arguments to the object's constructor.
- **Item 22 (Pimpl):** When you define the move constructor for your Pimpl class in the `.cpp` file, you will likely use `std::move` on the `pImpl` pointer to transfer ownership.

```cpp
// In widget.cpp
Widget::Widget(Widget&& other) noexcept 
    : pImpl(std::move(other.pImpl)) {} // Steal the unique_ptr
```


---

### Summary

1. **`std::move`**: Casts to *rvalue*. Use when you want to **steal** resources. (Non-templates).
2. **`std::forward`**: *Casts conditionally*. Use when you want to **pass through** arguments without changing their nature. (Templates).
3. **Neither** actually *moves memory*; they just enable the *move constructor* to be called.
4. **Never** use a variable after `std::move` unless you reassign it.
5. **Never** `std::move` a `const` variable (it forces a copy).
6. • **Neither** *std::move* nor *std::forward* do anything at runtime.

