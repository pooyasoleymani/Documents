---
Created Date: 2026-02-22
tags:
  - cpp
  - programming
Next:
---
---

When you need a pointer that _observes_ an object without affecting its *lifetime* and must safely handle the case where the object disappears—`std::weak_ptr` is the solution.

## 🔍 The Core Problem: Dangling References with Shared Ownership
Consider a cache that holds `shared_ptr`s to frequently used objects:
```cpp
class Cache {
	std::map<std::string, std::shared_ptr<Widget>> cache;
	
	public:
		std::shared_ptr<Widget> get(std::string& key) {
			return cache[key]; // Returns shared_ptr → keeps object alive!
		}
}
```

**Problem**: Even if _no one else_ needs a `Widget`, the cache's `shared_ptr` keeps it alive forever → **memory leak**.


### What we _really_ want: a pointer that:
- ✅ Observes the object _if it still exists_
- ❌ Doesn't prevent destruction when all _real owners_ release it
- 🔒 Safely detects when the object has been destroyed ("dangled")


## How `std::weak_ptr` Works

| Feature             | std::shared_ptr                                  | std::weak_ptr                                                 |
| ------------------- | ------------------------------------------------ | ------------------------------------------------------------- |
| **Ownership**       | Owns object (increments ref count)               | Non-owning observer (doesn't affect ref count)                |
| **Lifetime effect** | Keeps object alive                               | Object can be destroyed while `weak_ptr` exists               |
| **Dereferencing**   | Direct (`*ptr`, `ptr->foo()`)                    | ❌ Must convert to `shared_ptr` first                          |
| **Detects expiry**  | Always valid while alive                         | `expired()` or `lock()` reveals if object gone                |
| **Control block**   | Shares same control block as other `shared_ptr`s | Shares control block but doesn't increment _strong_ ref count |

### Key Operations

```cpp
std::weak_ptr<Widget> wp = /* ... */;

// Check if object still exists
if (!wp.expired()) { /* ... */ }

// Safely acquire temporary ownership
if (auto sp = wp.lock()) {  // Returns shared_ptr if alive, else empty
    sp->doSomething();      // Safe to use
} else {
    // Object was destroyed → handle gracefully
}
```



## 🧩 Primary Use Cases
