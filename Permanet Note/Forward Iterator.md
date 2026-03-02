---
Created Date: 2026-03-03
tags:
  - cpp
  - programming
---
---
A **Forward Iterator** is the most basic type of iterator that allows traversal in a single direction.

#### **Key Characteristics:**
- **Single Pass:** You can traverse the sequence only once. After you move an iterator past an element, you cannot go back to that element with the _same_ iterator instance.
- **Dereferencing:** You can read the value of the element the iterator points to (`*it`). You can also write to it (`*it = value`), meaning it’s a read/write iterator.
- **Increment:** You can move the iterator to the next element (`++it`).
- **Equality Comparison:** You can check if two forward iterators refer to the same element (`it1 == it2`).
- **Copyability:** Forward iterators are copyable.
- **“Non-End” State:** A forward iterator can be compared to the “end” iterator of a range.

**Analogy:** Think of a conveyor belt. You can pick items off it as they come by, and you can move to the next item. But once an item has passed you, you can’t rewind the belt to get it back with the same handler.

**Example Containers/Ranges:**

- `std::forward_list`
- Iterators obtained from `std::list` (though `list` iterators are actually Bidirectional)
- Iterators from `std::set`, `std::map` (also Bidirectional)
- Many custom-built sequence types.

#### **Typical Use Cases:**

- Iterating through a [[linked list]] to process each element.
- Reading elements from a [[stream]].

---
Ref: [[Concepts and Generic Programming]]