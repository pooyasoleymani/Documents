---
Created Date: 2026-07-16
tags:
  - software_engineering
Next: "[[Binary Search]]"
Related:
---
---
# Module 1 — Algorithms & Performance Engineering

```text
✓ Lesson 1.1 Complexity Analysis
✓ Lesson 1.2 Memory Hierarchy
✓ Lesson 1.3 Arrays

▶ Lesson 1.4 Dynamic Arrays & Amortized Growth

Lesson 1.5 Binary Search
Lesson 1.6 Sorting
...
```

---

# Lesson 1.4 — Dynamic Arrays: The Data Structure Behind Modern Languages

> "Every append has a cost—even when you don't pay for it immediately."

This lesson is one of the most valuable in the roadmap because it connects:

- Algorithms
- Memory
- Language runtimes
- Performance engineering
- System design

---

# Learning Objectives

After this lesson you will understand:

- Why static arrays are insufficient
- How dynamic arrays grow
- Amortized O(1)
- Reallocation
- Growth strategies
- Memory fragmentation
- Why Go, Python, Java and C++ all implement growth differently
- Why `append()` is not always O(1)

---

# Chapter 1 — The Problem

Imagine:

```text
Capacity = 4

+----+----+----+----+
| 10 | 20 | 30 | 40 |
+----+----+----+----+
```

Now execute

```go
Push(50)
```

Where should 50 go?

There is no free memory.

---

What are our options?

### Option 1

Move every element into a larger array.

```text
Old

+----+----+----+----+
|10|20|30|40|
+----+----+----+----+

↓

New

+----+----+----+----+----+----+----+----+
|10|20|30|40|50|
+----+----+----+----+----+----+----+----+
```

This is exactly what most dynamic arrays do.

---

# Chapter 2 — Reallocation

Reallocation consists of three steps.

## Step 1

Allocate new memory.

```text
Old

Capacity = 4
```

↓

```text
New

Capacity = 8
```

---

## Step 2

Copy data.

```text
10

↓

10
```

```text
20

↓

20
```

...

---

## Step 3

Free the old memory.

Now the new array becomes the backing storage.

---

Question:

Is this operation O(1)?

No.

It copies every element.

Complexity:

```text
O(n)
```

---

# Chapter 3 — Then Why Is append() O(1)?

Excellent question.

Let's simulate.

Capacity:

```text
1
```

Append:

```text
1
```

Cost:

```text
1 operation
```

---

Append again.

Need resize.

```text
copy 1

append
```

Cost:

```text
2
```

---

Append again.

No resize.

Cost:

```text
1
```

---

Append again.

Need resize.

Copy:

```text
3 elements
```

Cost:

```text
4
```

---

Suppose we append one million values.

Most appends cost:

```text
1
```

Only a few cost:

```text
1000

5000

20000
```

Average:

```text
O(1)
```

This is **amortized analysis**.

---

# Visualizing Growth

Imagine capacities:

```text
1

↓

2

↓

4

↓

8

↓

16

↓

32

↓

64
```

Number of reallocations:

```text
log₂(n)
```

Only about 20 reallocations are needed to reach roughly one million elements.

---

# Formal Intuition

Suppose we insert:

```text
1024 elements
```

How many copies happen?

```text
1

2

4

8

16

32

64

128

256

512
```

Total:

```text
1023
```

Interesting.

To insert **1024** elements,

we copy only about **1023** elements in total.

Average cost remains constant.

---

# Chapter 4 — Why Not Grow by One?

Imagine capacity:

```text
4
```

Need:

```text
5
```

Allocate:

```text
5
```

Next insertion:

Allocate:

```text
6
```

Next:

Allocate:

```text
7
```

Every insertion copies the entire array.

Complexity:

```text
O(n²)
```

Terrible.

---

# Chapter 5 — Why Not Double Forever?

Doubling seems perfect.

Not always.

Imagine:

```text
1 GB
```

Need one more element.

Doubling:

```text
2 GB
```

Huge waste.

This is why many runtimes stop doubling after a threshold.

---

# Real Runtime Growth

## Go

Go approximately:

```text
Small slices

×

2
```

Large slices

```text
~1.25x
```

Why?

Reduce memory waste.

---

## CPython

Python grows roughly:

```text
new = old + old/8 + constant
```

Not doubling.

Reason:

Lower fragmentation.

---

## Java

ArrayList:

```text
1.5x
```

---

## C++

`std::vector`

The standard does **not** specify the growth factor.

Different compilers choose different strategies.

---

# Why Languages Differ

Every runtime balances:

|Goal|Trade-off|
|---|---|
|Fewer reallocations|More memory|
|Less memory|More reallocations|
|Better cache|Larger copies|
|Better throughput|Higher memory usage|

There is no universally optimal growth factor.

---

# Chapter 6 — Memory Fragmentation

Suppose memory looks like:

```text
AAAA

BBBB

CCCC

DDDD
```

Free:

```text
BBBB
```

Need:

```text
BBBBBBBB
```

Impossible.

Although total free memory exists,

there isn't a **contiguous** block large enough.

This is memory fragmentation.

Allocators work hard to reduce it.

---

# Chapter 7 — Reserve()

C++ provides:

```cpp
vector.reserve(1000000);
```

Meaning:

> "I already know I'll insert one million elements."

Result:

Only one allocation.

No repeated growth.

---

Go has a similar optimization:

```go
make([]int, 0, 1000000)
```

A senior Go engineer uses this whenever the approximate size is known.

---

# Chapter 8 — Hidden Cost of append()

Many beginners think:

```go
slice = append(slice, x)
```

always modifies the same slice.

Wrong.

Sometimes:

```text
append

↓

new allocation

↓

copy

↓

new underlying array
```

The backing array changes.

We'll later see how this causes subtle bugs when multiple slices share the same array.

---

# Engineering Example

Imagine:

```go
messages := make([]Packet, 0)
```

Receiving:

```text
10 million packets
```

If you know this in advance:

```go
messages := make([]Packet, 0, 10_000_000)
```

You may eliminate dozens of reallocations and copy operations.

This simple optimization can noticeably improve throughput in high-volume systems.

---

# Trade-offs

|Strategy|Advantages|Disadvantages|
|---|---|---|
|Double|Fast growth|Higher memory usage|
|1.5×|Better memory efficiency|More reallocations|
|1.25×|Lower fragmentation|Increased copy frequency|
|Grow by 1|Minimal wasted space|O(n²) behavior|

---

# Exercises

## Theory

Answer in your own words:

1. Why isn't `append()` always O(1)?
    
2. Why is the average append cost still O(1)?
    
3. Why doesn't Go always double slice capacity?
    
4. Why does CPython use a smaller growth factor?
    
5. What is memory fragmentation?
    
6. Why should you preallocate when possible?
    
7. When is doubling the best strategy?
    
8. When is doubling a poor strategy?
    

---

## Go

Extend your `DynamicArray[T]`:

Implement:

```go
Reserve(capacity int)
ShrinkToFit()
Clear()
IsEmpty()
Front()
Back()
```

Add benchmarks comparing:

- Preallocated vs non-preallocated insertion
    
- Capacity doubling vs 1.5× growth
    
- Manual copy vs built-in `copy` (for comparison after your own implementation)
    

---

## Python

Improve your `DynamicArray` so it no longer relies on `list.append()`. Instead:

- Maintain your own logical `size` and `capacity`.
    
- Allocate a backing list of fixed capacity.
    
- Grow it manually when full.
    
- Shift elements manually for insertions.
    

This mirrors what CPython's list implementation does internally.

---

## C++

Add to your `Vector<T>`:

- `reserve()`
    
- `resize()`
    
- `clear()`
    
- `shrink_to_fit()`
    

Then compare your behavior with `std::vector`.

---

# Reading

This week, begin reading source code—not just books.

## Go

Browse:

```text
src/runtime/slice.go
```

Focus on:

- `growslice`
    
- Capacity calculation
    
- Allocation
    
- Copy behavior
    

Don't worry if you don't understand everything yet. The goal is to become comfortable reading runtime code.

---

# Senior Engineer Discussion

Here's something to think about.

Suppose you're building a telemetry service that receives **100 million events per day**.

Two engineers propose:

**Engineer A**

```go
events := []Event{}
```

**Engineer B**

```go
events := make([]Event, 0, 5_000_000)
```

Both implementations are correct.

### Your challenge

Which implementation would you approve in a production code review, and what questions would you ask before making that decision?

Notice the subtlety: don't immediately pick Engineer B. A senior engineer first asks about the workload, memory budget, request lifecycle, and allocation patterns. Learning to ask those questions is as important as knowing the implementation details.

---

## Next milestone

After Lesson 1.4, we'll move to **Lesson 1.5: Binary Search Beyond Interviews**, where we'll cover:
- Branch prediction
- Overflow-safe midpoint calculation
- Lower bound / upper bound
- Binary search on answers
- Monotonic predicates
- B-tree search
- CPU behavior during branching
- How databases and storage engines use binary search internally

That's the point where algorithm analysis starts intersecting with database internals and storage systems.