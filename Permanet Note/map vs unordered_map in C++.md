---
Created Date: 2026-09-15
tags:
  - cpp
---
---
## map vs unordered_map in C++

In C++, ****map**** and ****unordered_map**** are the containers that store can store data in the form of key-value pairs, but they differ significantly in terms of underlying implementation and performance characteristics.

****The below table lists the primary differences between map and unordered_map container:****

| map                                                                       | unordered_map                                                                 |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| It stores key-value pairs in sorted order based on the key.               | It is also storing key-value pairs but not in any specific order              |
| It is implemented using ****red-black tree****.                           | It is implemented using ****hash table.****                                   |
| It is slower for most operations due to sorting.                          | It is faster for most operations.                                             |
| It takes O(log n) time for inserting, accessing, and deleting an element. | It takes O(1) average time for inserting, accessing, and deleting an element. |

