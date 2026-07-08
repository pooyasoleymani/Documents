---
Created Date: 2026-07-08
tags:
  - software_engineering
Next:
Related:
---

---

# Week 1 — Lesson 1.3-
# Arrays: The Most Important Data Structure

> "Every high-performance system is built on arrays."

Examples:

- Go slices → arrays
- C++ `std::vector` → arrays
- Python `list` → arrays
- Redis → arrays
- PostgreSQL → arrays inside pages
- Linux kernel → arrays
- Network ring buffers → arrays
- CPU caches → arrays

Arrays are the foundation of modern software.

---

# Learning Objectives

After this lesson you will understand:

- Physical memory layout
- Static vs Dynamic arrays
- How arrays are stored in RAM
- Why indexing is O(1)
- Why insertion is O(n)
- Why deletion is O(n)
- Dynamic array growth
- Why Go slices are powerful
- Why `std::vector` exists
- Python list internals (high level)

---

# Chapter 1 — What is an Array?

An array is a **contiguous block of memory** containing elements of the same type.

Example:

```text
Index

0 1 2 3 4

Values

8 2 5 9 1
```

Memory:

```text
Address

1000
1008
1016
1024
1032
```

Assume:

```text
int64

8 Bytes
```

Each element occupies exactly 8 bytes.

---

# Chapter 2 — Address Calculation

Suppose:

```text
Base Address = 1000

Element Size = 8 bytes
```

Question:

Where is

```text
arr[4]
```

located?

Formula:

```text
address = base + index × element_size
```

Calculation:

```text
1000 + (4 × 8)

=

1032
```

The CPU computes this directly. No searching is required.

That's why indexing is O(1).

---

# Why Linked Lists Cannot Do This

A linked list stores:

```text
value

pointer
```

To access element 1000:

```
Node1

↓

Node2

↓

Node3

↓

...

↓

Node1000
```

The CPU must traverse every pointer.

Time:

```text
O(n)
```

---

# Chapter 3 — Why Access is O(1)

The processor performs:

```text
Base Address

+

Index

×

Element Size
```

No loop.

No traversal.

One address calculation.

This is true in Go, C++, Rust, Java, and many other languages.

---

# Chapter 4 — Insertion

Array:

```text
1 2 3 4 5
```

Insert:

```text
99
```

at index 2.

Result:

```text
1 2 99 3 4 5
```

To make space, every following element must move one position.

Elements moved:

```text
3

4

5
```

Time complexity:

```text
O(n)
```

---

# Chapter 5 — Deletion

Delete:

```text
2
```

Array becomes:

```text
1 3 4 5
```

Again:

Every remaining element shifts left.

Complexity:

```text
O(n)
```

---

# Chapter 6 — Dynamic Arrays

Suppose capacity:

```text
4
```

Current:

```text
1 2 3 4
```

Append:

```text
5
```

No space.

The runtime:

1. Allocates a larger array.
2. Copies existing elements.
3. Frees the old array (or lets the GC reclaim it in Go).
4. Appends the new element.

---

# Chapter 7 — Go Slice Growth

A slice contains:

```text
Pointer

Length

Capacity
```

Example:

```go
numbers := []int{1,2,3}
```

Internally:

```text
Pointer -----> Array

Length = 3

Capacity = 3
```

Append:

```go
numbers = append(numbers,4)
```

If capacity is exhausted:

A new backing array is allocated and elements are copied.

---

# Why Capacity Exists

Without extra capacity:

Every append would require:

- allocation
- copy
- free/GC

Complexity:

```text
O(n)
```

Instead:

Go over-allocates.

Result:

Most appends are:

```text
O(1)

Amortized
```

---

# Chapter 8 — Real-World Example

Imagine building a TCP packet queue.

Packets:

```text
Packet1

Packet2

Packet3
```

Store them in:

### Linked List

Pros:

Easy insertion.

Cons:

- many allocations
- cache misses
- pointer chasing

---

### Dynamic Array

Pros:

- contiguous
- cache-friendly
- fewer allocations
- higher throughput

This is why many high-performance networking systems use arrays or ring buffers.

---

# Chapter 9 — Trade-offs

| Operation                        |          Array |               Linked List |
| -------------------------------- | -------------: | ------------------------: |
| Index                            |           O(1) |                      O(n) |
| Search                           |           O(n) |                      O(n) |
| Insert End (with spare capacity) | Amortized O(1) |                      O(1) |
| Insert Middle                    |           O(n) |      O(1) (if node known) |
| Delete Middle                    |           O(n) |      O(1) (if node known) |
| Cache Locality                   |      Excellent |                      Poor |
| Memory Overhead                  |            Low | Higher (pointer per node) |

Notice that complexity alone doesn't determine the better choice.

---

# C++ Perspective

`std::vector` exists because contiguous memory is usually the fastest representation for general-purpose sequences.

You'll implement your own version later, which will deepen your understanding of Go slices as well.

---

# Python Perspective

Python's `list` is **not** a linked list.

It's a dynamic array that over-allocates capacity to make `append()` efficient.

That's why:

```python
numbers.append(5)
```

is amortized O(1).

---

# Engineering Insight

Many developers think:

> Arrays are a beginner topic.

Experienced systems engineers know:

> Arrays are the foundation of almost every high-performance data structure.

Hash tables, heaps, B-trees, ring buffers, vectors, matrices, CPU caches, and many database storage layouts all rely heavily on contiguous arrays.

---

# Exercises

## Theory

Answer these without searching:

1. Why is array indexing O(1)?
2. Why is insertion in the middle O(n)?
3. Why do dynamic arrays keep extra capacity?
4. Why doesn't Go allocate exactly one more element on every `append`?
5. Why is Python's `list.append()` amortized O(1)?
6. When would a linked list still be a better choice than an array?

---

## Go

Create:

```text
algorithms/arrays/
```

Implement:

- `Insert(index, value)`
- `Delete(index)`
- `Append(value)`
- `Prepend(value)`
- `Contains(value)`
- `IndexOf(value)`
- `Reverse()`
- `RotateLeft(k)`
- `RotateRight(k)`
- `Clone()`
- `Clear()`

For each operation:

- Write unit tests.
- Write benchmarks.
- Document time and space complexity.

---

## C++

Implement your own `Vector<T>` with:

- `push_back`
- `pop_back`
- `reserve`
- `resize`
- `operator[]`
- `size`
- `capacity`

Avoid using `std::vector` internally.

---

## Python

Implement a simple `DynamicArray` class using a backing list and a capacity field to simulate how dynamic arrays grow. This exercise is educational rather than idiomatic Python.

---

# Documentation Pack

Add these files:

```text
docs/
├── notes/
│   └── lesson-1.3-arrays.md
├── glossary/
│   ├── array.md
│   ├── dynamic-array.md
│   ├── contiguous-memory.md
│   └── capacity.md
├── interview/
│   └── arrays.md
└── diagrams/
    └── lesson-1.3/
        ├── array-layout.md
        ├── dynamic-array-growth.md
        └── insert-delete.md
```

---

# Mentor Challenge

You're designing a messaging system that receives **10 million events per minute**. Engineers propose two implementations for the in-memory queue:

1. A dynamic array that occasionally resizes.
2. A linked list that allocates one node per event.

Analyze the proposal from multiple angles:

- Time complexity
- Cache locality
- Allocation overhead
- Garbage collection pressure
- Memory overhead
- Throughput
- Latency

Don't stop at saying "arrays are faster." Explain _why_, using the concepts from Lessons 1.1–1.3. This is the type of reasoning expected in senior engineering design reviews.