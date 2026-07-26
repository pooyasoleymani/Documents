---
Created Date: 2026-07-22
tags:
  - software_engineering
Next: "[[Sorting]]"
---
---

# Module 1 — Algorithms & Performance Engineering

```text
✓ Lesson 1.1 Complexity Analysis
✓ Lesson 1.2 Memory Hierarchy
✓ Lesson 1.3 Arrays
✓ Lesson 1.4 Dynamic Arrays

▶ Lesson 1.5 Binary Search: From Algorithms to Storage Engines
```

---

# Lesson Objectives

After this lesson you'll understand:

- Binary search from first principles
- Loop invariants
- Correctness proofs
- Integer overflow
- Lower Bound
- Upper Bound
- Equal Range
- Monotonic predicates
- Binary search on answers
- Floating-point binary search
- Branch prediction
- Cache behavior
- How B-Trees search nodes
- Why databases use binary search

---

# Chapter 1 — The Problem

Suppose we have

```text
Index

0 1 2 3 4 5 6 7

Value

2 5 8 11 17 21 40 55
```

Find

```text
21
```

How many comparisons?

Linear search

Worst case

```text
8
```

Now imagine

```text
1 Billion
```

records.

Linear search

Worst case

```text
1 Billion comparisons
```

Impossible for many workloads.

---

# Chapter 2 — The Idea

Binary search asks one question:

> Which half can never contain the answer?

Instead of finding the answer immediately, we **eliminate impossible regions**.

Example

```text
2 5 8 11 17 21 40 55
```

Target

```text
21
```

Middle

```text
11
```

Since

```text
21 > 11
```

everything on the left is impossible.

New search space

```text
17 21 40 55
```

Repeat.

Each comparison halves the search space.

---

# Complexity

Suppose

```text
1,024 elements
```

Binary search

```text
1024

↓

512

↓

256

↓

128

↓

64

↓

32

↓

16

↓

8

↓

4

↓

2

↓

1
```

Comparisons

```text
10
```

General rule

```text
O(log₂ n)
```

---

# Chapter 3 — The Real Secret

Most people think binary search is about finding a value.

Wrong.

Binary search is about **maintaining an invariant**.

---

# What is an Invariant?

An invariant is a condition that is always true throughout the algorithm.

Example

```text
If the target exists,

it is inside

[low, high]
```

Every iteration must preserve this property.

If you violate the invariant, your algorithm is incorrect—even if it seems to work for many cases.

This mindset is fundamental in algorithm design.

---

# Example

Initial state

```text
low = 0
high = 7
```

Invariant

```text
Target ∈ [low, high]
```

Middle

```text
mid = 3
```

Value

```text
11
```

Target

```text
21
```

Update

```text
low = mid + 1
```

Why not

```text
low = mid
```

?

Because we already know

```text
arr[mid] != target
```

Keeping `mid` would violate progress and may cause an infinite loop.

---

# Chapter 4 — Overflow

Classic implementation

```go
mid := (low + high) / 2
```

Looks fine.

Imagine

```text
low = 2,000,000,000
high = 2,100,000,000
```

On a 32-bit integer

```text
low + high
```

overflows.

The safe version

```go
mid := low + (high-low)/2
```

This is now the standard implementation across many languages.

---

# Chapter 5 — Lower Bound

Suppose

```text
1 2 2 2 2 5 9
```

Find

```text
2
```

Which one?

There are four.

Lower Bound means

> Find the **first** element that is **greater than or equal to** the target.

Result

```text
Index 1
```

---

# Upper Bound

Upper Bound means

> Find the **first** element that is **greater than** the target.

Same array

```text
1 2 2 2 2 5 9
```

Upper Bound

```text
Index 5
```

---

Notice something interesting.

Neither function necessarily returns the exact element.

They return a **position**.

That position is often more useful.

---

# Why Databases Love Lower Bound

Suppose PostgreSQL stores

```text
100
101
105
109
120
125
130
```

Query

```sql
SELECT *

WHERE id >= 109
```

The storage engine doesn't search for 109 directly.

Instead it performs

```text
LowerBound(109)
```

and starts scanning from there.

This is why lower_bound is fundamental to B-tree indexes.

---

# Chapter 6 — Binary Search on Answers

This surprises many engineers.

Suppose you need to answer:

> What is the minimum bandwidth required to finish all uploads in one hour?

There's no sorted array.

Can we still use binary search?

Yes.

Search space

```text
Bandwidth

1 Mbps

↓

10 Gbps
```

We test:

```text
500 Mbps

Enough?

YES
```

Then

```text
250 Mbps

Enough?

NO
```

The answer space is **monotonic**.

---

# Monotonic Predicate

Suppose

```text
Bandwidth

100 Mbps

❌

200 Mbps

❌

300 Mbps

✅

400 Mbps

✅

500 Mbps

✅
```

Notice

```text
False False False True True True
```

Once it becomes true,

it stays true.

Binary search works whenever the predicate is monotonic—not just on sorted arrays.

---

# Real Engineering Examples

Find minimum:

- Number of servers
    
- Buffer size
    
- Cache size
    
- Timeout
    
- Maximum packet size
    
- Compression level
    

If the answer space is monotonic, binary search applies.

---

# Chapter 7 — Branch Prediction

Modern CPUs try to guess:

```go
if target < arr[mid]
```

before the comparison completes.

Random searches are harder to predict.

Mispredictions flush the CPU pipeline and reduce performance.

This is one reason branchless search techniques exist in high-performance code.

---

# Chapter 8 — Binary Search Inside a B-Tree

Suppose a B-tree node stores

```text
5
11
19
22
35
48
60
```

To decide which child to visit,

the database performs a binary search within the node.

This reduces comparisons while keeping the tree shallow.

So binary search is used _inside_ larger data structures, not just on standalone arrays.

---

# Common Production Bugs

Avoid these pitfalls:

1. Incorrect loop condition (`low < high` vs. `low <= high`).
    
2. Overflow when computing `mid`.
    
3. Infinite loops due to not advancing `low` or `high`.
    
4. Failing on empty slices.
    
5. Returning an arbitrary duplicate instead of the first or last occurrence.
    
6. Not considering integer overflow on 32-bit platforms.
    
7. Ignoring branch prediction effects in hot code paths.
    

---

# Trade-offs

|Algorithm|Lookup|Ordered Data|Range Queries|
|---|---|---|---|
|Linear Search|O(n)|No|No|
|Binary Search|O(log n)|Yes|Yes|
|Hash Table|O(1) avg|No|No|
|B-tree|O(log n)|Yes|Excellent|

This table should immediately suggest why databases favor B-trees over hash tables for general-purpose indexing.

---

# Exercises

## Theory

Answer these:

1. Why is binary search fundamentally about eliminating impossible regions rather than "finding" an element?
    
2. What is a loop invariant?
    
3. Why does `low = mid` sometimes lead to an infinite loop?
    
4. Why do databases rely on `lower_bound` more often than ordinary binary search?
    
5. What is a monotonic predicate?
    
6. Give three real-world optimization problems where binary search can be applied to the answer space.
    

---

## Go

Implement a generic package:

```go
package binarysearch
```

Functions:

```go
func Search[T constraints.Ordered](...)
func LowerBound[T constraints.Ordered](...)
func UpperBound[T constraints.Ordered](...)
func EqualRange[T constraints.Ordered](...)
```

Requirements:

- Generic over ordered types.
    
- Iterative implementations.
    
- Comprehensive tests, including:
    
    - empty slice
        
    - one element
        
    - duplicates
        
    - target absent
        
    - target smaller than all elements
        
    - target larger than all elements
        
- Benchmarks for:
    
    - linear search
        
    - binary search
        
    - lower bound
        

---

## Python

Implement the same APIs manually. Then compare your implementation with Python's `bisect` module and explain any differences in behavior.

---

## C++

Implement:

- `binary_search`
    
- `lower_bound`
    
- `upper_bound`
    

Then compare your implementations with `<algorithm>` and verify they produce identical results.

---

# Reading Assignment

This week, begin reading code from real systems:

- Go's `sort.Search` implementation in the standard library.
    
- CPython's `bisect` module (Python source).
    
- C++ `std::lower_bound` documentation and, if possible, your standard library implementation.
    

Observe not only the algorithm, but also the API design choices.

---

# Senior Engineer Challenge

Imagine you're implementing a storage engine for a database.

Each disk page contains **512 sorted keys**.

When searching for a key, would you:

1. Perform a linear scan of the page?
    
2. Use binary search?
    
3. Use another strategy?
    

Your answer should consider:

- CPU cache behavior
    
- Branch prediction
    
- Number of comparisons
    
- Typical B-tree page sizes
    
- Overall throughput
    

This question has a subtle answer. The asymptotically optimal algorithm is not always the fastest in practice, and understanding why will take us deeper into modern CPU architecture.