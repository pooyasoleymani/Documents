---
Created Date: 2026-03-06
tags:
  - cpp
  - programming
Related: "[[Template]]"
---
---
### هدف: بررسی اینکه آیا همه نوع‌ها از یک نوع خاص هستند

مثلاً می‌خواهیم بدانیم آیا تمام نوع‌ها از `std::integral` هستند یا نه.

```cpp
#include <type_traits>

// Base case: Empty pack → true
template <typename... Ts>
struct AllIntegral : std::true_type {};

// Recursive case:
template <typename T, typename... Rest>
struct AllIntegral<T, Rest...>
    : std::conditional_t< std::is_integral_v<T>, AllIntegral<Rest...>, std::false_type> {};


static_assert(AllIntegral<int, long, short>::value, "همه عدد صحیحند");
static_assert(!AllIntegral<int, double>::value, "double عدد صحیح نیست");

```