---
Created Date: 2026-03-06
tags:
  - cpp
  - programming
Related: "[[Template]]"
---
---
در دنیای TMP، هر عملیات در سطح type انجام می‌شود و معمولاً با `struct` پیاده‌سازی می‌گردد که شامل `::type` یا `::value` است.

```cpp
template<int A, int B>
struct Add {
	static constexpr int value = A + B;
};

constexpr int result = Add<Add<1, 2>::value, 3>::value; // 6
```

