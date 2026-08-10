---
Created Date: 2026-08-03
tags:
  - software_engineering
---


---

# Module 1 — Algorithms & Performance Engineering

```text
✓ Complexity Analysis
✓ Memory Hierarchy
✓ Arrays
✓ Dynamic Arrays
✓ Binary Search
✓ Sorting Fundamentals
✓ Merge Sort

▶ Lesson 1.6.3 — Quick Sort: From Textbook to PDQSort
```

---

# Learning Objectives

By the end of this lesson you will understand:

- Divide and Conquer revisited
- Partitioning
- Lomuto Partition
- Hoare Partition
- Pivot selection
- Worst-case behavior
- Randomized Quick Sort
- Median-of-three
- Tail recursion elimination
- Cache behavior
- Why Quick Sort beats Merge Sort in practice
- How Introsort works
- How PDQSort improves Quick Sort

---

# Chapter 1 — The Core Idea

Merge Sort:

```text
Divide

↓

Sort

↓

Merge
```

Quick Sort:

```text
Choose Pivot

↓

Partition

↓

Sort Left

↓

Sort Right
```

Unlike Merge Sort,

Quick Sort never merges.

Instead,

it moves elements to the correct side of a pivot.

---

# Example

Array

```text
9 4 8 3 1 2 5
```

Choose pivot

```text
5
```

Partition

```text
4 3 1 2

5

9 8
```

Notice

Everything left of the pivot

```text
<
```

Everything right

```text
>
```

The pivot is now in its **final sorted position**.

That is the key property of Quick Sort.

---

# Chapter 2 — Partitioning

Partitioning is the heart of Quick Sort.

Everything else is recursion.

There are two famous partition algorithms:

- Lomuto
- Hoare

Understanding their trade-offs is far more important than memorizing code.

---

# Lomuto Partition

Algorithm

```text
Pivot = last element

Scan left to right

Move smaller values forward

Finally place pivot
```

Example

```text
7 3 8 4 2 5
```

Pivot

```text
5
```

Result

```text
3 4 2 5 8 7
```

Simple.

Easy to implement.

Popular in textbooks.

---

## Advantages

- Easy to understand
- Easy to verify
- Good for teaching

---

## Disadvantages

Lots of swaps.
Even when unnecessary.
That increases memory writes.

---

# Hoare Partition

Invented by Tony Hoare.

Algorithm

Two pointers

```text
←

→
```

Move inward.

Swap only when necessary.

---

Example

```text
9 3 8 2 5 7
```

Pivot

```text
5
```

Pointers move until they find misplaced elements.

Swap.

Repeat.

---

Advantages

- Fewer swaps
- Faster
- Better cache behavior
- Used in many production implementations

---

Disadvantages

Harder to reason about.

Many beginners introduce subtle bugs.

---

# Chapter 3 — Choosing the Pivot

Suppose the pivot is always the last element.

Already sorted input

```text
1 2 3 4 5 6
```

Pivot

```text
6
```

Partition

```text
1 2 3 4 5

6
```

Left side

```text
5 elements
```

Right side

```text
0
```

Repeat.

Recursion tree

```text
n

↓

n-1

↓

n-2

↓

...
```

Complexity

```text
O(n²)
```

---

# Better Pivot Strategies

## Random Pivot

Choose a random element.

Probability of worst-case becomes extremely small.

---

## Median of Three

Choose

```text
First

Middle

Last
```

Take their median.

Example

```text
2

50

100
```

Pivot

```text
50
```

Produces more balanced partitions.

Most real implementations use something similar.

---

# Chapter 4 — Complexity

Average

```text
O(n log n)
```

Worst

```text
O(n²)
```

Space

```text
O(log n)
```

(recursion stack)

---

# Why Quick Sort Is Usually Faster Than Merge Sort

Interesting question.

Merge Sort

```text
Allocate buffer

↓

Copy

↓

Merge
```

Quick Sort

```text
Partition in-place
```

Less memory traffic.

Better cache locality.

Fewer allocations.

Modern CPUs reward these characteristics.

That's why Quick Sort often wins despite the worse theoretical worst case.

---

# Chapter 5 — Tail Recursion Elimination

Naive Quick Sort

```go
quick(left)
quick(right)
```

Maximum recursion

```text
O(n)
```

Stack overflow possible.

Optimization

Always recurse into the smaller partition.

Loop over the larger one.

Maximum recursion

```text
O(log n)
```

This is used in production libraries.

---

# Chapter 6 — Cache Behavior

Partition scans memory sequentially.

```text
0

1

2

3

4

5
```

Sequential memory

↓

Excellent cache locality

↓

Hardware prefetching

↓

High throughput

Quick Sort's cache behavior is one reason it performs so well.

---

# Chapter 7 — Why C++ Doesn't Use Plain Quick Sort

Imagine malicious input.

Always worst-case.

```text
O(n²)
```

Unacceptable.

C++ uses

## Introsort

Algorithm

```text
Quick Sort

↓

Too deep?

↓

Heap Sort
```

The recursion depth is monitored.

If it exceeds a threshold (typically proportional to `2*log₂(n)`), the algorithm switches to Heap Sort, guaranteeing **O(n log n)** worst-case performance while preserving Quick Sort's excellent average-case speed.

---

# Chapter 8 — Why Go Uses PDQSort

PDQ

```text
Pattern Defeating Quick Sort
```

Improves Quick Sort by detecting bad partition patterns.

Features

- Better pivot selection
- Handles duplicates efficiently
- Detects nearly sorted input
- Reduces branch mispredictions
- Avoids common Quick Sort worst cases

Result

Very fast on real workloads.

---

# Chapter 9 — Stability

Quick Sort

```text
NOT Stable
```

During partitioning,

equal elements may move relative to each other.

Example

```text
Alice 5000

Bob 5000
```

After Quick Sort

```text
Bob 5000

Alice 5000
```

Still sorted.

Not stable.

---

# Complexity Summary

| Property       | Quick Sort |
| -------------- | ---------- |
| Best           | O(n log n) |
| Average        | O(n log n) |
| Worst          | O(n²)      |
| Stable         | ❌          |
| In-place       | ✅          |
| Cache Friendly | Excellent  |
| Extra Memory   | O(log n)   |
| Parallelizable | Good       |

---

# Merge Sort vs Quick Sort

| Feature          | Merge Sort | Quick Sort            |
| ---------------- | ---------- | --------------------- |
| Stable           | ✅          | ❌                     |
| Extra Memory     | O(n)       | O(log n) stack        |
| Worst Case       | O(n log n) | O(n²)                 |
| Average Speed    | Very Good  | Excellent             |
| Cache Locality   | Good       | Excellent             |
| External Sorting | Excellent  | Poor                  |
| Default in Go    | ❌          | Foundation of PDQSort |

---

# Real-World Applications

Quick Sort (or its descendants) is used in:

- Go runtime (`slices.Sort`)
- Rust standard library
- C++ `std::sort` (via Introsort)
- Java primitive sorting (dual-pivot Quick Sort)
- Many embedded systems

---

# Common Production Bugs

Avoid these pitfalls:

1. Poor pivot selection leading to O(n²).
2. Infinite recursion when partition boundaries are wrong.
3. Stack overflow from deep recursion.
4. Mishandling duplicate values.
5. Assuming Quick Sort is stable.
6. Forgetting to optimize for small partitions (many runtimes switch to Insertion Sort).

---

# Exercises

## Theory

Answer these:

1. Why is partitioning the core operation of Quick Sort?
2. Compare Lomuto and Hoare partition schemes. What are the trade-offs?
3. Why does choosing the last element as pivot degrade performance on sorted input?
4. Why does randomized pivot selection reduce the chance of worst-case behavior?
5. Why is Quick Sort generally faster than Merge Sort on modern CPUs?
6. Why is Quick Sort not stable?
7. What problem does Introsort solve?
8. What improvements does PDQSort add over classic Quick Sort?

---

## Go

Implement:

```go
func QuickSort[T cmp.Ordered](arr []T)
```

Requirements:

- Start with Lomuto partition.
- Then implement Hoare partition.
- Benchmark both.
- Compare against:
    - Merge Sort
    - `slices.Sort`
- Run:

```bash
go test -bench=. -benchmem
```

Record:

- ns/op
- B/op
- allocs/op

---

## Python

Implement Quick Sort using:

- Lomuto partition
- Hoare partition

Compare both with:

```python
sorted(...)
```

Observe:

- runtime
- recursion depth
- behavior on already sorted input

---

## C++

Implement:

```cpp
template<typename T>
void QuickSort(std::vector<T>& arr);
```

Implement both partition strategies and compare them with:

```cpp
std::sort(...)
```

Analyze differences in performance and behavior.

---

# Reading Assignment

Study:

1. Go's `slices.Sort` documentation.
2. The PDQSort paper (high-level overview is sufficient for now).
3. C++ `std::sort` complexity guarantees.
4. Tony Hoare's original partition algorithm.

Focus on **why** runtime libraries evolved beyond textbook Quick Sort.

---

# Senior Engineer Challenge

You're building a log-processing service that sorts **100 million log entries** in memory.

Characteristics:

- 95% of the data is already sorted.
- Many entries have identical timestamps.
- Low memory overhead is required.
- Throughput is more important than latency.

Questions:

1. Would you choose classic Quick Sort? Why or why not?
2. How could many duplicate keys hurt a naïve Quick Sort implementation?
3. Why would PDQSort likely outperform textbook Quick Sort on this workload?
4. Would a stable sort provide any benefit here? Explain your reasoning.
5. If the dataset grows beyond RAM, how would your sorting strategy change?

This scenario reflects the kinds of trade-offs engineers make when designing high-performance backend and data-processing systems.