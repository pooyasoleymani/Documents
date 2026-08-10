---
Created Date: 2026-08-10
tags:
  - software_engineering
---
---
# Lesson 1.6.4 — Heap Sort & Priority Queues

We now move from partition-based sorting to a different idea: **maintaining an ordering invariant inside a tree-shaped data structure**.

This lesson is important because the heap will reappear later in:

- Operating-system scheduling
- Task queues
- Dijkstra's algorithm
- A* search
- Top-K problems
- Event-driven systems
- Job schedulers
- Rate limiting
- Streaming systems

---

# 1. What is a Heap?

A **binary heap** is a complete binary tree satisfying a heap property.

There are two common types.

### Min-Heap

The smallest element is at the root:

```text
          1
       /     \
      3       2
     / \     / \
    7   5   8   4
```

Property:

```text
parent <= children
```

Therefore:

```text
minimum = root
```

---

### Max-Heap

The largest element is at the root:

```text
          9
       /     \
      7       8
     / \     / \
    3   5   6   4
```

Property:

```text
parent >= children
```

Therefore:

```text
maximum = root
```

---

# 2. The Important Insight

A heap is **not fully sorted**.

For example:

```text
          1
       /     \
      4       2
     / \     / \
    9   7   8   5
```

We know:

```text
1 = minimum
```

But we do **not** know that the remaining elements are sorted.

This distinction is important.

A heap provides a fast way to access the **highest-priority element**, not arbitrary sorted access.

---

# 3. Why Is a Heap Usually Stored in an Array?

The tree:

```text
          A
       /     \
      B       C
     / \     / \
    D   E   F   G
```

can be stored as:

```text
[A B C D E F G]
```

No pointers are required.

For zero-based indexing:

### Parent

For node `i`:

```text
parent = (i - 1) / 2
```

### Left child

```text
left = 2*i + 1
```

### Right child

```text
right = 2*i + 2
```

Example:

```text
index:

       0
      / \
     1   2
    / \ / \
   3  4 5  6
```

This is another example of why **contiguous arrays are powerful**.

We represent a tree without pointers.

---

# 4. Heap Invariant

The critical concept is the **heap invariant**.

For a min-heap:

```text
parent <= child
```

For every node.

Suppose:

```text
          2
       /     \
      5       3
```

Valid.

But:

```text
          5
       /     \
      2       3
```

is invalid for a min-heap.

We need to restore the invariant.

---

# 5. Sift Down

Suppose:

```text
          8
       /     \
      3       5
```

Min-heap requirement is violated.

We compare `8` with its children.

Smallest child:

```text
3
```

Swap:

```text
          3
       /     \
      8       5
```

Now the invariant is restored.

This operation is called:

```text
siftDown
```

or sometimes:

```text
heapify
```

---

# 6. Sift Up

Now imagine inserting:

```text
1
```

into:

```text
          3
       /     \
      5       7
```

The new node initially goes at the next available position:

```text
          3
       /     \
      5       7
     /
    1
```

But:

```text
1 < 5
```

The heap invariant is broken.

Swap:

```text
          3
       /     \
      1       7
     /
    5
```

Again:

```text
1 < 3
```

Swap:

```text
          1
       /     \
      3       7
     /
    5
```

This is:

```text
siftUp
```

---

# 7. Complexity of Heap Operations

The heap height is:

```text
O(log n)
```

Therefore:

### Insert

```text
O(log n)
```

because the element may travel from the bottom to the root.

### Extract Min / Max

```text
O(log n)
```

because the root is removed and the replacement may need to move down.

### Peek

```text
O(1)
```

because the highest-priority element is at the root.

This gives us a powerful data structure:

```text
peek       O(1)
insert     O(log n)
extract    O(log n)
```

---

# 8. Priority Queue

A **priority queue** is an abstract data type where each element has a priority.

Example:

```text
Task A → priority 10
Task B → priority 3
Task C → priority 7
```

A normal FIFO queue gives:

```text
A → B → C
```

A priority queue might give:

```text
B → C → A
```

if lower numbers mean higher priority.

A heap is one of the most common implementations of a priority queue.

---

# 9. Real-World Example — Job Scheduler

Imagine a server receives:

```text
Normal request     priority 10
Database backup    priority 20
Emergency request  priority 1
```

A priority queue lets the scheduler efficiently select:

```text
Emergency request
```

first.

Then:

```text
Normal request
```

then:

```text
Database backup
```

This is much more appropriate than repeatedly sorting the entire task list.

---

# 10. Heap Sort

Now we can use a heap to sort.

For ascending order:

1. Build a max-heap.
    
2. Largest element is at root.
    
3. Move root to the end.
    
4. Reduce heap size.
    
5. Restore heap property.
    
6. Repeat.
    

Example:

```text
[4 1 7 3 8 5]
```

Build max heap:

```text
          8
       /     \
      4       7
     / \     /
    3   1   5
```

Array representation:

```text
[8 4 7 3 1 5]
```

Move `8` to the end:

```text
[5 4 7 3 1 | 8]
```

Heapify:

```text
[7 4 5 3 1 | 8]
```

Continue.

Eventually:

```text
[1 3 4 5 7 8]
```

---

# 11. Heap Sort Complexity

Building the heap:

```text
O(n)
```

Then:

```text
n extractions × O(log n)
```

Therefore:

```text
O(n log n)
```

Worst case:

```text
O(n log n)
```

Best case:

```text
O(n log n)
```

Average:

```text
O(n log n)
```

And importantly:

```text
Auxiliary memory = O(1)
```

Heap Sort is therefore:

> **In-place + O(n log n) worst-case**

This is one of its biggest advantages.

---

# 12. The Important Interview Question

## Why is Build Heap O(n), not O(n log n)?

This is a classic interview question.

You might initially think:

```text
n elements
×
log n per insertion
=
O(n log n)
```

That's true if you build a heap by repeatedly inserting elements.

But bottom-up heap construction is different.

We start from the last non-leaf node and call `siftDown`.

Most nodes are near the bottom and can move only a tiny distance.

Only a few nodes can move `log n` levels.

The total work is:

```text
n/2 × O(1)
+
n/4 × O(2)
+
n/8 × O(3)
+
...
```

This converges to:

```text
O(n)
```

This is a very important example of why you shouldn't determine complexity by simply multiplying:

```text
number of operations × worst-case cost
```

You must understand **how the work is distributed**.

---

# 13. Heap Sort vs Quick Sort

Both can sort in:

```text
O(n log n)
```

But Quick Sort is generally faster in practice.

Why?

Heap traversal jumps around the array:

```text
0
1
2
...
```

but heap relationships frequently access positions such as:

```text
i
2i+1
2i+2
```

This produces less favorable memory-access patterns.

Quick Sort performs relatively sequential partition scans.

Therefore:

```text
Quick Sort
→ better cache behavior

Heap Sort
→ stronger worst-case guarantee
```

This is an excellent example of:

> **Same Big-O does not mean same performance.**

---

# 14. Priority Queue vs Sorting

Suppose you have:

```text
1,000,000 tasks
```

and every second you need the highest-priority task.

Would you sort everything every time?

No.

A priority queue is better.

Instead:

```text
sort all tasks
O(n log n)

remove one

sort again
O(n log n)

...
```

Use:

```text
heap

insert     O(log n)
peek       O(1)
remove     O(log n)
```

This is an important data-structure selection principle:

> Don't perform more work than the problem requires.

---

# 15. Top-K Problems

Suppose you have:

```text
10 million users
```

and need:

> Find the 100 users with the highest score.

Do you need to fully sort 10 million users?

No.

Maintain a **min-heap of size 100**.

Process each user:

```text
score > heap.minimum?
        ↓
      yes
        ↓
replace minimum
```

Complexity:

```text
O(n log k)
```

instead of:

```text
O(n log n)
```

When:

```text
k << n
```

this is a major improvement.

This pattern appears constantly in real backend and data-processing systems.

---

# 16. Go

Go provides:

```go
container/heap
```

It defines a heap interface around methods such as:

```go
Len()
Less()
Swap()

Push()
Pop()
```

The important design lesson is that Go's heap implementation works through an **interface**, allowing you to define your own priority semantics.

Later, we'll implement a production-style priority queue using it.

---

# 17. C++

C++ provides:

```cpp
std::priority_queue
```

Example:

```cpp
std::priority_queue<int> q;
```

By default:

```text
largest element
```

has highest priority.

For a min-priority queue:

```cpp
std::priority_queue<
    int,
    std::vector<int>,
    std::greater<int>
> q;
```

---

# 18. Python

Python provides:

```python
heapq
```

It implements a min-heap.

Example:

```python
import heapq

heap = []

heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)

print(heapq.heappop(heap))
```

Result:

```text
2
```

---

# 19. Heap Use Cases

Remember these.

### Operating Systems

Process scheduling.

```text
highest priority process
```

### Networking

Packet scheduling.

### Databases

Top-K queries.

### Graph algorithms

Dijkstra:

```text
extract closest vertex
```

### A*

```text
extract lowest estimated cost
```

### Event systems

```text
next event by timestamp
```

### Distributed systems

Task scheduling and delayed jobs.

---

# 20. Heap Trade-offs

|Operation|Complexity|
|---|--:|
|Peek|O(1)|
|Insert|O(log n)|
|Extract|O(log n)|
|Search arbitrary element|O(n)|
|Build Heap|O(n)|

A heap is **not** a general-purpose sorted structure.

If you need:

> "Find arbitrary element quickly"

a heap may be the wrong data structure.

If you need:

> "Repeatedly get the minimum/maximum"

a heap is an excellent choice.

---

# Exercises

## Theory

Answer these in your own words:

1. What is the heap invariant?
    
2. Why can a binary heap be represented efficiently using an array?
    
3. Why is `peek()` O(1)?
    
4. Why are insertion and extraction O(log n)?
    
5. What is the difference between `siftUp` and `siftDown`?
    
6. Why is bottom-up Build Heap O(n)?
    
7. Why is Heap Sort O(n log n)?
    
8. Why is Heap Sort usually slower than Quick Sort despite the same O(n log n) complexity?
    
9. Why is a heap useful for a priority queue?
    
10. Why can a heap solve Top-K problems in O(n log k)?
    

---

# Go Exercise

Implement your own **MinHeap** without using `container/heap` initially.

API:

```go
type MinHeap[T cmp.Ordered] struct {
    data []T
}

func (h *MinHeap[T]) Push(value T)
func (h *MinHeap[T]) Pop() (T, bool)
func (h *MinHeap[T]) Peek() (T, bool)
func (h *MinHeap[T]) Len() int
```

Requirements:

- Implement `siftUp`.
    
- Implement `siftDown`.
    
- Maintain the heap invariant.
    
- Write unit tests.
    
- Test empty heap.
    
- Test one element.
    
- Test duplicates.
    
- Test already sorted input.
    
- Test reverse sorted input.
    

Then implement:

```go
HeapSort[T cmp.Ordered](arr []T)
```

and benchmark it against:

```text
Quick Sort
Merge Sort
slices.Sort
```

---

# Python Exercise

Implement:

```python
class MinHeap:
    ...
```

without using `heapq`.

Then compare your implementation against:

```python
heapq
```

---

# C++ Exercise

Implement:

```cpp
template <typename T>
class MinHeap {
    std::vector<T> data;

public:
    void push(const T& value);
    T pop();
    const T& top() const;
};
```

Then compare it with:

```cpp
std::priority_queue
```

---

# Senior Engineer Challenge

You are designing a job scheduler.

You have:

```text
10,000,000 jobs
```

Each job has:

```text
job ID
priority
creation time
deadline
```

Requirements:

1. Always execute the highest-priority job.
    
2. If two jobs have the same priority, execute the oldest first.
    
3. New jobs arrive continuously.
    
4. You cannot repeatedly sort all 10 million jobs.
    
5. You need efficient insertion and removal.
    

### Questions

**A.** What data structure would you choose?

**B.** What should the comparison rule be?

**C.** What is the complexity of inserting a job?

**D.** What is the complexity of selecting/removing the next job?

**E.** How would you handle this ordering?

```text
priority ↓
creation_time ↑
```

**F.** What happens if you need to cancel an arbitrary job by ID? Is a normal heap sufficient?

That last question is particularly important. It introduces the difference between a data structure that is excellent for one operation and one that supports **all required operations efficiently**.

That is exactly the kind of trade-off we want you to start recognizing as a senior engineer.