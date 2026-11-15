---
Created Date: 2026-03-06
tags:
  - cpp
  - programming
Related: "[[SFINAE]]"
---
---
## What is `std::declval`?

#### `std::declval<T>()` is a function that:
1. Return reference of object of  type`T`.
2. **Crucially, it does _not_ actually construct or return an object of type `T`**. The object is purely hypothetical.
3. It is designed to be used in contexts where you want to **evaluate an expression involving a type `T` without needing an actual object of type `T` to exist**.

## What is used?
If we want to write template that checks if a type `T` has specific member function.
```cpp
template<typename T>
void check_foo(T t) {
// How can I check if obj.foo() is valid without actually calling it here? 
// If obj.foo() is *not* valid, the compiler will error out immediately. 
// I need a way to *test* the validity of obj.foo() as an expression.
}
```


## How `std::declval` Works in Practice (The SFINAE Connection)

`std::declval<T>()` is most commonly used within `decltype`. `decltype(expression)` gives you the type of an expression.

```cpp
#include <utility> // For std::declval
#include <type_traits> // For std::true_type, std::false_type

// Helper to check if T has a member function foo()
template <typename T>
struct has_foo {
private:
    // 1. std::declval<T>() creates a hypothetical T object.
    // 2. std::declval<T>().foo() creates a hypothetical call to foo().
    // 3. decltype(...) gets the type of that hypothetical expression.
    // 4. The comma operator ensures the expression is evaluated and then returns true_type.
    //    This whole part is within the return type of 'test', a deduced context.
    template <typename U>
    static auto test(U*) -> decltype(std::declval<U>().foo(), std::true_type{});

    // Fallback overload for types that don't have foo()
    template <typename>
    static std::false_type test(...);

public:
    // static constexpr bool value = ...; // (This part is outside the core explanation of declval)
};

// Example usage within a function template:
template <typename T>
auto process(T t) -> std::enable_if_t<has_foo<T>::value> {
    // This function will only be considered if T has a foo() member
    std::cout << "Processing type with foo()\n";
    t.foo(); // We can now safely call foo() because SFINAE guaranteed it exists.
}

```


**In this example:**

1. `std::declval<U>()` is called. It doesn’t need a real `U` object. It just _pretends_ to have one so that `foo()` can be applied to it.
2. The expression `std::declval<U>().foo()` is formed. The compiler checks if this expression is _valid_.
3. This check happens within `decltype(...)`, which is inside the return type of `template <typename U> static auto test(U*)`, which _is_ a **deduced context**.
4. If `std::declval<U>().foo()` is a valid expression, `decltype` succeeds, the comma operator proceeds, and `std::true_type{}` is returned. The `test` overload taking `U*` is a candidate.
5. If `std::declval<U>().foo()` is _invalid_ (e.g., `T` has no `foo()` member), `decltype` fails. This substitution failure within the deduced context causes the `test(U*)` template to be discarded (SFINAE). The compiler then tries the `test(...)` fallback, which always succeeds, returning `std::false_type{}`.


# Key Benefits of `std::declval`

1. **Enables Expression SFINAE:** Allows checking the validity of arbitrary expressions (member access, function calls, operator usage, etc.) without needing actual objects.
2. **Type Safety:** Guarantees that no actual object construction or side effects occur. The “object” is purely conceptual.
3. **Metaprogramming Power:** It’s a cornerstone for writing type traits and policies that inspect and react to type capabilities.

# When _Not_ to Use `std::declval`

- **When you have an actual object:** If you already have a variable or object of type `T`, you can just use that object directly. `std::declval` is for when you _don’t_ have one and need to test a type’s properties in isolation.
- **For simple type checks:** For basic checks like “is it an integer?”, `std::is_integral_v<T>` is sufficient and doesn’t require `decltype` or `declval`.

In essence, `std::declval` is a clever tool that helps C++ metaprogramming query the capabilities of types in a safe and non-intrusive way, particularly when combined with `decltype` and SFINAE.