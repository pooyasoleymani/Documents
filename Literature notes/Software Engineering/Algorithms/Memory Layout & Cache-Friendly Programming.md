---
Created Date: 2026-07-03
tags:
  - software_engineering
Related:
Next:
---
---
# Lesson 1.2 — Memory Layout & Cache-Friendly Programming

> "Programs don't run on algorithms. They run on hardware."

This lesson is one of the most important in the entire roadmap.

---

# Learning Objectives

After this lesson you should understand:

- Stack vs Heap
- Virtual Memory
- CPU Cache
- Cache Lines
- Locality of Reference
- Cache Miss
- Pointer Chasing
- False Sharing (introduction)
- Why contiguous memory is king

These concepts will appear again when we study:

- Go slices
- Go GC
- Redis
- PostgreSQL
- Linux kernel
- TCP networking
- Lock-free programming

---

# Chapter 1 — The Memory Hierarchy

Most people think memory looks like this:

```text
Program
    │
    ▼
	RAM
```

Reality is much more complex.

```
                 CPU

      Registers (~1 cycle)
            │
            ▼
      L1 Cache (~4 cycles)
            │
            ▼
      L2 Cache (~12 cycles)
            │
            ▼
      L3 Cache (~40 cycles)
            │
            ▼
       RAM (~100 ns)
            │
            ▼
	 SSD (~100 μs)
            │
            ▼
	 HDD (~10 ms)
```

Notice something.

The CPU is **thousands to millions of times faster** than storage.

Most optimization is about **avoiding slow memory**, not making the CPU faster.

---

# Question

Imagine this code:

```go
for i := range arr {
    sum += arr[i]
}
```

What is the CPU doing?

Many beginners answer:

> Reading one integer.

Wrong.

The CPU almost never fetches one integer.

It fetches an entire **cache line**.

---

# Chapter 2 — Cache Line

Most modern CPUs have:

```
64-byte cache lines
```

Suppose:

```
int64 = 8 bytes
```

Then one cache line contains:

```
+----+----+----+----+----+----+----+----+
| 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  |
+----+----+----+----+----+----+----+----+
```

When you read

```
arr[0]
```

the CPU actually loads

```
arr[0]
arr[1]
arr[2]
...
arr[7]
```

at once.

This is called **spatial locality**.

---

# Chapter 3 — Spatial Locality

Imagine:

```go
for _, x := range arr {
    sum += x
}
```

Access pattern:

```
0
1
2
3
4
5
6
7
8
9
```

Perfect.

Every cache line is fully utilized.

The CPU loves this.

---

Now imagine:

```
0
100
4
900
25
701
```

The CPU constantly loads new cache lines.

Performance drops dramatically.

---

# Chapter 4 — Temporal Locality

Suppose:

```go
counter++
counter++
counter++
counter++
```

The CPU keeps `counter` in cache (and often in a register), making repeated accesses extremely fast.

This is called **temporal locality**: data that was used recently is likely to be used again soon.

---

# Chapter 5 — Pointer Chasing

Consider a linked list:

```
Node A
   |
   v
Node B
   |
   v
Node C
   |
   v
Node D
```

Memory:

```
A -> 0x1000

B -> 0x9A1200

C -> 0xF00200

D -> 0x12345000
```

The nodes are scattered throughout memory.

To reach `D`:
1. Load `A`.
2. Read the pointer to `B`.
3. Load `B`.
4. Read the pointer to `C`.
5. Load `C`.
6. Read the pointer to `D`.
7. Load `D`.

Each load may result in a cache miss.

This sequence of dependent memory accesses is called **pointer chasing**.

---

# Why Arrays Win

Array:

```
1 2 3 4 5 6 7 8
```

The CPU prefetcher recognizes the sequential access pattern and starts loading future cache lines before you request them.

Linked list:

```
A -> B -> C -> D
```

The next address isn't known until the current node is read, so the CPU can't effectively *prefetch*.

This is one reason arrays often outperform linked lists by a large margin despite both having O(n) traversal.

---

# Chapter 6 — Stack vs Heap

We'll spend an entire lesson on this later, but you need the basic idea now.

## Stack

```
func main() {
    x := 10
}
```

`x` typically lives on the stack.

Properties:

- Very fast allocation.
- Very fast deallocation.
- Managed automatically by function calls.

---

## Heap

```
new(User)
```

or in Go, values that escape the function.

Properties:

- Larger.
- Slower to allocate.
- Managed by the garbage collector.

Heap allocation is often more expensive than stack allocation.

---

# Chapter 7 — Why Go Slices Are Fast

A slice is a descriptor:

```
Pointer
Length
Capacity
```

The underlying array is contiguous.

So when you write:

```go
for _, v := range slice {
}
```

Go iterates over contiguous memory, which is cache-friendly.

Understanding this will become important when we study slice growth and escape analysis.

---

# Chapter 8 — Real-World Example

Suppose you're building your telecom event queue.

Option A:

```
Linked List
```

Option B:

```
Ring Buffer (Array)
```

Which will usually achieve higher throughput?

The ring buffer.

Not because of Big O, but because:

- contiguous memory
- fewer allocations
- better cache locality
- fewer pointer dereferences
- better branch prediction

This is why high-performance systems like packet processors, trading systems, and message queues frequently use ring buffers.

---

# Reading Assignment

Continue with:

- **Efficient Go**: Focus on chapters discussing benchmarking and performance mindset.
- **Introducing Go**: Review slices and arrays, paying attention to how they differ.

---

# Exercises

## Theory

Answer these in your own words:

1. Why is RAM much slower than CPU registers?
2. What is a cache line?
3. Why does sequential memory access improve performance?
4. What is pointer chasing?
5. Why can an array outperform a linked list even though both have O(n) traversal?
6. What are spatial and temporal locality?
7. What is the difference between stack and heap memory?

---

## Go Programming

Create a new package:

```
algorithms/memory
```

Implement:

1. Reverse an array **in place**.
2. Reverse a slice by creating a **new** slice.
3. Rotate left.
4. Rotate right.
5. Copy a slice manually (without using `copy`).
6. Compare manual copy vs. built-in `copy` using benchmarks.
7. Benchmark iterating over:
    - a slice (`[]int`)
    - a linked list implementation (your own from a later lesson, or the standard library for an initial comparison)

Document the time complexity and expected memory behavior for each.

---

## C++ Track

Implement a minimal `Vector` class supporting:

- Dynamic growth
- `push_back`
- `pop_back`
- `reserve`
- `size`
- `capacity`

Do **not** use `std::vector` internally. This exercise will prepare you for understanding Go slices.

---

## Python Track

Write a script that compares:

- Iterating over a `list`
- Iterating over a `collections.deque`

Measure execution time using the `timeit` module and explain the observed differences.

---

# Mentor Challenge

Suppose you are designing a high-throughput TCP server expected to handle **5 million packets per second**.

You have two queue implementations:

- A linked-list queue.
- A circular buffer (ring buffer) backed by an array.

**Without looking anything up**, explain which one you would choose and justify your decision using the concepts from Lessons 1.1 and 1.2—not just Big O, but memory layout, cache behavior, allocation patterns, and CPU efficiency.

This style of reasoning is what we'll apply throughout the roadmap, from data structures all the way to distributed systems and operating system internals.