---
Created Date: 2026-03-03
tags:
  - cpp
  - programming
---
---
A **Random Access Iterator** is the most powerful category of iterators. It supports all operations of a Bidirectional Iterator (which includes Forward Iterator) and adds much more flexible arithmetic operations.

#### **Key Characteristics (All of Forward Iterator’s +):**

- **Arithmetic Operations:**
- **Addition:** You can advance an iterator by an arbitrary number of positions: `it + n`. This results in an iterator pointing `n` positions _after_ the original `it`.
- **Subtraction:** You can move an iterator backward by an arbitrary number of positions: `it - n`. This results in an iterator pointing `n` positions _before_ the original `it`.
- **Difference:** You can calculate the distance between two random access iterators: `it1 - it2`. This gives you the number of elements between them.
- **Offset Dereferencing:** You can access an element at a specific offset from the iterator: `it[n]`. This is equivalent to `*(it + n)`.
- **Comparison:** You can compare two random access iterators not only for equality but also for ordering:
- `it1 < it2`
- `it1 > it2`
- `it1 <= it2`
- `it1 >= it2`

**Analogy:** Think of an array or a memory address. You can jump directly to any element using its index. You can also calculate how far apart any two elements are.

**Example Containers/Ranges:**

- `std::vector`
- `std::deque`
- C-style arrays (`int arr[10];`)
- `std::string`
- `std::array`

#### **Typical Use Cases:**

- Algorithms that need to jump around in a sequence efficiently, like `std::sort`, `std::binary_search`, `std::copy`, `std::fill`.
- Any operation where you need to know the exact distance between two points in a sequence or access elements by index.


---
Ref: [[Concepts and Generic Programming]], [[Iterator vs Pointer]]