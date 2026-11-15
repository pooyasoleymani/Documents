---
Created Date: 2026-07-26
tags:
  - software_engineering
---
---

# Module 1 — Algorithms & Performance Engineering

```text
✓ Lesson 1.1 Complexity Analysis
✓ Lesson 1.2 Memory Hierarchy
✓ Lesson 1.3 Arrays
✓ Lesson 1.4 Dynamic Arrays
✓ Lesson 1.5 Binary Search

▶ Lesson 1.6 Sorting: Why Languages Use Different Algorithms
```

This lesson is much bigger than binary search and will span several sub-lessons.

```
Lesson 1.6.1 Fundamentals of Sorting
Lesson 1.6.2 Merge Sort
Lesson 1.6.3 Quick Sort
Lesson 1.6.4 Heap Sort
Lesson 1.6.5 Introsort
Lesson 1.6.6 Timsort
Lesson 1.6.7 PDQSort
Lesson 1.6.8 External Sorting
Lesson 1.6.9 Parallel Sorting
Lesson 1.6.10 Real-world Runtime Implementations
```

Today is **Lesson 1.6.1**.

---

# Lesson 1.6.1 — Fundamentals of Sorting

## Learning Objectives

By the end of this lesson you should understand:

- What sorting actually is
- Why sorting is one of the most important algorithms
- Properties of sorting algorithms
- Stable vs unstable sorting
- In-place vs out-of-place sorting
- Comparison vs non-comparison sorting
- Why no comparison sort can beat **O(n log n)**
- Why different languages choose different algorithms

---

# Chapter 1 — What is Sorting?

Sorting is the process of arranging elements according to an ordering relation.

Example

Before

```text
8 2 9 1 4
```

After

```text
1 2 4 8 9
```

Simple.

But sorting is far more important than it looks.

---

# Why Do We Sort?

Suppose you have:

```
100 million users
```

You want:

- search quickly
- remove duplicates
- merge datasets
- build indexes
- perform range queries

Sorting makes all of these easier.

Many algorithms first sort the data and then solve the actual problem.

---

# Real Systems That Depend on Sorting

Sorting is fundamental in:

- Database query execution
- Search engines
- Log aggregation
- Distributed systems
- MapReduce
- Git
- Linux kernel
- Memory allocators
- Compilers

Sorting is one of the most optimized algorithms in software engineering.

---

# Chapter 2 — Properties of a Sorting Algorithm

When evaluating a sorting algorithm, don't ask only:

> "How fast is it?"

Ask:

- Is it stable?
- Is it in-place?
- Worst-case complexity?
- Average-case complexity?
- Extra memory?
- Cache friendly?
- Parallelizable?
- Adaptive?
- Good for nearly sorted data?

A senior engineer evaluates algorithms across multiple dimensions.

---

# Stable Sorting

Suppose we sort employees by salary.

Before:

| Name    | Salary |
| ------- | ------ |
| Alice   | 5000   |
| Bob     | 4000   |
| Charlie | 5000   |

Sorted:

| Name    | Salary |
| ------- | ------ |
| Bob     | 4000   |
| Alice   | 5000   |
| Charlie | 5000   |

Notice:

Alice remains before Charlie.

The relative order of equal keys didn't change.

That is a **stable sort**.

---

## Why Stability Matters

Imagine:

First sort by

```
Department
```

Then sort by

```
Salary
```

If the second sort is stable,

employees with equal salary remain grouped by department.

Database engines rely on this behavior.

---

# Unstable Sort

Suppose after sorting:

| Name    | Salary |
| ------- | ------ |
| Bob     | 4000   |
| Charlie | 5000   |
| Alice   | 5000   |

Still sorted?

Yes.

But

Alice and Charlie swapped.

That's unstable.

---

# Chapter 3 — In-place Sorting

An algorithm is **in-place** if it uses only a small amount of additional memory.

Example:

```
Original Array

↓

Same Array Sorted
```

Examples:

- Heap Sort
- Quick Sort (mostly)
- Selection Sort

---

# Out-of-place Sorting

Merge Sort

```
Original

↓

Temporary Array

↓

Merged Result
```

Needs additional memory.

Trade-off:

More memory

↓

Better stability

↓

Often simpler merging

---

# Chapter 4 — Comparison Sorting

Algorithms like:

- Merge Sort
- Quick Sort
- Heap Sort

work by asking questions like:

```
Is A < B?
```

Everything they know comes from comparisons.

---

# Why O(n log n) is the Limit

This is one of the most important theoretical results in computer science.

Imagine sorting:

```
3 elements
```

Possible orders:

```
ABC
ACB
BAC
BCA
CAB
CBA
```

There are

```
3!

=

6
```

possible outcomes.

Every comparison splits possibilities.

Binary decisions create a decision tree.

To distinguish all outcomes,

the tree must have at least

```
n!
```

leaves.

The minimum height is

```
log₂(n!)
```

Using Stirling's approximation:

```
log₂(n!)

≈

n log₂ n
```

Therefore:

> **No comparison-based sorting algorithm can have a better worst-case complexity than O(n log n).**

This is a mathematical proof, not an implementation limitation.

---

# Then How Can Counting Sort Be O(n)?

Because it doesn't compare elements.

Instead it uses knowledge about the data.

Examples:

- Counting Sort
- Radix Sort
- Bucket Sort

These algorithms trade memory or assumptions about the input for better time complexity.

We'll study them later.

---

# Chapter 5 — Adaptive Sorting

Suppose the data is already:

```
1 2 3 4 5 6
```

Should sorting still take

```
O(n log n)
```

?

Not necessarily.

Adaptive algorithms exploit existing order.

Examples:

- Timsort
- Insertion Sort (for small arrays)
- PDQSort

Python's Timsort is extremely fast on nearly sorted data.

---

# Chapter 6 — Cache Behavior

Suppose two algorithms both have:

```
O(n log n)
```

One accesses memory sequentially.

The other jumps randomly.

Which is faster?

Usually:

Sequential.

Because of:

- cache locality
- hardware prefetching
- fewer cache misses

Modern sorting algorithms are designed with the CPU cache in mind.

---

# Chapter 7 — Parallel Sorting

Modern servers have:

- 8 cores
- 16 cores
- 64 cores

Can sorting use them?

Yes.

Algorithms like Merge Sort divide work naturally.

Quick Sort can also be parallelized.

This matters for big-data systems.

---

# Sorting in Major Languages

| Language        | Algorithm                |
| --------------- | ------------------------ |
| Go              | PDQSort + Insertion Sort |
| Python          | Timsort                  |
| C++             | Introsort                |
| Java Objects    | Timsort                  |
| Java primitives | Dual-Pivot QuickSort     |
| Rust            | PDQSort                  |

Notice:

No major language uses a plain textbook Quick Sort.

Runtime engineers optimize for real workloads.

---

# Trade-offs

| Property       | Merge      | Quick     | Heap       |
| -------------- | ---------- | --------- | ---------- |
| Stable         | ✅          | ❌         | ❌          |
| In-place       | ❌          | Mostly    | ✅          |
| Worst Case     | O(n log n) | O(n²)     | O(n log n) |
| Cache Friendly | Good       | Excellent | Poor       |
| Parallel       | Excellent  | Good      | Fair       |

We'll justify every cell in this table over the next lessons.

---

# Engineering Example

Imagine you're sorting:

```
10 million log records
```

Questions a senior engineer asks:

- Are records already nearly sorted?
- Is stability required?
- How much RAM is available?
- Can we use multiple cores?
- Will the data fit in memory?
- Are comparisons expensive?
- Is this latency-sensitive or throughput-oriented?

The algorithm choice depends on these answers—not just on Big O.

---

# Exercises

## Theory

Answer these in your own words:

1. What is a stable sort?
2. Why do databases often require stable sorting?
3. What is an in-place algorithm?
4. Why can't comparison sorting beat **O(n log n)**?
5. Why can Counting Sort achieve **O(n)**?
6. What makes an algorithm adaptive?
7. Why do modern sorting algorithms care about CPU caches?
8. Why doesn't every language simply use Merge Sort?

---

## Go

Implement:

- Bubble Sort
- Selection Sort
- Insertion Sort

Requirements:

- Generic (`cmp.Ordered`)
- Unit tests
- Benchmarks
- Count comparisons and swaps for each algorithm

Don't dismiss these algorithms as "slow." They're important because they form building blocks inside modern hybrid algorithms.

---

## Python

Implement the same three algorithms.

Then compare them with Python's built-in `sorted()` using benchmark data.

---

## C++

Implement the same algorithms using templates.

Then compare them against `std::sort`.

---

# Reading Assignment

This week, read:

1. Go's `sort` package documentation.
2. Python's Sorting HOWTO.
3. C++ `std::sort` documentation.

Don't focus only on APIs. Pay attention to the guarantees each language provides:

- Is the sort stable?
- What complexity is guaranteed?
- Is additional memory used?
- How are custom comparators handled?

---

# Senior Engineer Challenge

Imagine you're building an e-commerce platform.

Each product has:

```go
type Product struct {
    ID       int
    Price    int
    Rating   float64
    Name     string
}
```

The product list is already sorted by **Rating**.

Now a new requirement arrives:

> Display products sorted by **Price**, but if two products have the same price, preserve their original rating order.

### Questions

1. Would you choose a **stable** or **unstable** sorting algorithm?
2. Why?
3. If your language's default sort is unstable, how could you still satisfy the requirement?
4. Would you sort twice or design a custom comparator?

This is a realistic problem you'll encounter in backend services, recommendation systems, and search ranking pipelines.

---

This marks the beginning of the sorting section. Over the next several lessons, we'll progressively build from these simple algorithms to the production algorithms used by Go, Python, C++, Java, and Rust. By the end, you'll understand not only **how** they work, but **why** each runtime chose a different design.