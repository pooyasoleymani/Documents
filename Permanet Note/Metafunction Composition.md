---
Created Date: 2026-03-06
tags:
  - cpp
  - programming
Related: "[[Template]]"
---
---
در TMP، مثل Functional Programming، می‌توان چند متا‌تابع را زنجیره کرد.

```cpp
template <int X>
struct Square {
    static constexpr int value = X * X;
};

template <int A, int B>
struct SquareSum {
    static constexpr int value = Square< Add<A,B>::value >::value;
};

```

اینجا `SquareSum<2,3>::value` معادل `(2+3)^2 = 25` است و هیچ runtime cost ندارد.