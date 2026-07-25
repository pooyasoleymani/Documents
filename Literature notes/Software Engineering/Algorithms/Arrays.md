---
Created Date: 2026-07-07
tags:
  - software_engineering
Next: "[[Dynamic Arrays & Amortized Growth]]"
---
---
# Lesson 1.3 — Arrays: The Foundation of Modern Software

## Learning Objectives

After this lesson you'll understand:

- What an array really is
- Memory layout    
- Why indexing is O(1)
- Why insertion is O(n)
- Static vs Dynamic arrays
- Arrays vs Linked Lists
- Why arrays dominate modern software
- How Go slices, Python lists and C++ vectors are built

---

# 1. What is an Array?

Many beginners think:

```text
Array

1
2
3
4
5
```

Wrong.

An array is actually:

> **A contiguous block of memory containing elements of identical size.**

Memory:

```
Address      Value

0x1000  ->   10
0x1004  ->   20
0x1008  ->   30
0x100C  ->   40
0x1010  ->   50
```

Notice something.

Addresses increase by **4 bytes**.

Why?

Because an `int32` occupies 4 bytes.

If it were `int64`:

```
0x1000
0x1008
0x1010
0x1018
```

Now addresses increase by **8 bytes**.

The CPU loves predictable memory.

---

# 2. Why is Array Access O(1)?

Suppose

```
Base Address

0x1000
```

Each element

```
8 bytes
```

Access

```
arr[5]
```

CPU computes

```
address = base + index * sizeof(element)
```

Example

```
0x1000 + 5 × 8

=

0x1028
```

No searching.

No traversal.

Just arithmetic.

That is why indexing is O(1).

---

# Important Insight

Arrays are **not searched**.

The CPU computes the address directly.

This is one of the fastest operations a CPU performs.

---

# 3. Why Insertion is O(n)

Suppose

```
1 2 3 4 5
```

Insert

```
99
```

at index

```
2
```

Result

```
1 2 99 3 4 5
```

What actually happened?

```
1 2 3 4 5

↓

move 5

↓

move 4

↓

move 3

↓

insert 99
```

Several elements must be moved.

Worst case

```
O(n)
```

---

# 4. Why Deletion is O(n)

Delete

```
3
```

```
1 2 3 4 5
```

Result

```
1 2 4 5
```

Everything after `3` shifts left.

Again

```
O(n)
```

---

# 5. Why Arrays Beat Linked Lists

Interview answer:

```
Array

Insert O(n)

Delete O(n)
```

```
Linked List

Insert O(1)

Delete O(1)
```

Looks like Linked Lists win.

Reality:

Almost nobody builds high-performance software using linked lists.

Why?

Because insertion isn't the whole story.

Usually you must first **find** where to insert.

```
Search

O(n)

+

Insert

O(1)

=

O(n)
```

The linked list loses its theoretical advantage in many real workloads.

---

# 6. Modern CPUs Prefer Arrays

Imagine

```
Packet

Packet

Packet

Packet
```

stored contiguously.

CPU loads

```
Packet 1

Packet 2

Packet 3

Packet 4
```

with very few cache misses.

Now imagine

```
Packet

↓

another page

↓

another page

↓

another page
```

The CPU repeatedly waits for memory.

Throughput drops.

This is why:

- Redis
    
- PostgreSQL
    
- Go runtime
    
- Java JVM
    
- Linux kernel
    
- Kafka
    

all try to maximize contiguous memory where practical.

---

# 7. Arrays in Different Languages

## Go

```go
var arr [5]int
```

Fixed size.

---

Slice

```go
s := []int{1,2,3}
```

Actually

```
Pointer

Length

Capacity
```

pointing to an underlying array.

---

## Python

```
list
```

Despite the name, it is **not** a linked list.

It is a dynamic array.

Many programmers don't realize this.

---

## C++

```
std::vector
```

Dynamic array.

---

Notice something interesting.

Three very different languages...

Same underlying data structure.

---

# 8. Static vs Dynamic Arrays

Static

```
Capacity fixed forever
```

Advantages

- Simple
    
- Fast
    
- No reallocations
    

Disadvantages

- Wasted memory
    
- Cannot grow
    

---

Dynamic

```
Grow when needed
```

Advantages

- Flexible
    

Disadvantages

- Occasionally reallocates
    

We'll study growth algorithms in Lesson 1.4.

---

# 9. Trade-offs

|Operation|Array|Linked List|
|---|---|---|
|Index|O(1)|O(n)|
|Search|O(n)|O(n)|
|Insert End|O(1) amortized|O(1)|
|Insert Middle|O(n)|O(n) (after search)|
|Delete|O(n)|O(n) (after search)|
|Cache Friendly|Excellent|Poor|
|Memory Usage|Low|High|
|Random Access|Excellent|Impossible|

A senior engineer doesn't choose based only on asymptotic complexity. They also consider:

- Cache locality
    
- Memory overhead
    
- Allocation frequency
    
- Access patterns
    
- Expected workload
    

---

# Engineering Insight

Suppose you're designing a telecom message queue.

You expect:

- 8 million messages per second
    
- Sequential processing
    
- FIFO behavior
    
- Minimal latency
    

Would you choose:

- Linked list
    
- Dynamic array
    
- Ring buffer
    

A senior engineer quickly narrows this to a **ring buffer backed by an array** because it minimizes allocations, maximizes cache locality, and provides predictable memory access patterns.

---

# Exercises

## Theory

Answer in your own words:

1. Why is indexing O(1)?
    
2. Why are arrays contiguous?
    
3. Why are Python lists not linked lists?
    
4. Why is insertion in the middle O(n)?
    
5. Why does the CPU prefer arrays?
    
6. When would you deliberately choose a linked list?
    
7. Why do most standard libraries implement dynamic arrays?
    

---

## Go

Implement your own generic dynamic array API (do **not** use `append` internally):

```go
type DynamicArray[T any] struct {
    // fields
}

func (d *DynamicArray[T]) Push(v T)
func (d *DynamicArray[T]) Pop() T
func (d *DynamicArray[T]) Insert(index int, value T)
func (d *DynamicArray[T]) Remove(index int)
func (d *DynamicArray[T]) Get(index int) T
func (d *DynamicArray[T]) Set(index int, value T)
func (d *DynamicArray[T]) Size() int
func (d *DynamicArray[T]) Capacity() int
```

Requirements:

- Allocate memory yourself with `make`.
    
- Grow capacity manually.
    
- Copy elements manually with loops.
    
- Do not use the built-in `append` or `copy`.
    
- Write unit tests and benchmarks.
    

---

## Python

Implement a simplified `DynamicArray` class with the same operations to reinforce the concepts.

---

## C++

Implement a `Vector<T>` with:

- constructors
    
- destructor
    
- copy constructor
    
- move constructor
    
- `push_back`
    
- `pop_back`
    
- `reserve`
    
- `operator[]`
    
- `size`
    
- `capacity`
    

This will prepare you for understanding RAII and move semantics later.

---

# Reading

This week, start building a reading habit alongside coding.

From the books you've uploaded, read:

- **Efficient Go**: Chapters on benchmarking and memory awareness.
    
- **Introducing Go**: Arrays and slices.
    
- **Building Maintainable Software**: The introduction and first chapter. Focus on why code quality and maintainability are engineering concerns, not just style.
    

---

## Mentor Challenge

Here's a question that many experienced developers answer incorrectly:

> **Why doesn't Go expose the capacity of an array, but it does expose the capacity of a slice?**

Don't search for the answer. Think from first principles about what an array is versus what a slice represents. We'll discuss your reasoning before moving to **Lesson 1.4: Dynamic Arrays and Amortized Growth**, where you'll build the core data structure behind Go slices, Python lists, and `std::vector`.