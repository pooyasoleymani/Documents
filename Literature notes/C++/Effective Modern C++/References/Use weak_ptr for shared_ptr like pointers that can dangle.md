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
### 1. Breaking Cyclic References (Preventing Memory Leaks)
```cpp
class Node {
	sdt::shared_ptr<Node> next;
	std::weak_ptr<Node> prev;
}
```

Without `weak_ptr`, two nodes pointing to each other with `shared_ptr` create a *reference cycle* *→* *neither is ever destroyed*.


### 2. Caching (Non-Owning References)
```cpp
class WidgetCache {
    std::map<std::string, std::weak_ptr<Widget>> cache;
public:
    std::shared_ptr<Widget> get(const std::string& key) {
        if (auto sp = cache[key].lock()) return sp;  // Cache hit
        
        auto sp = std::make_shared<Widget>(key);     // Cache miss
        cache[key] = sp;
        return sp;
    }
};


// other cache
std::shared_ptr<const Widget> fastLoadWidget(WidgetID id)
{
	static std::unordered_map<WidgetID,std::weak_ptr<const Widget>> cache;
	auto objPtr = cache[id].lock(); // objPtr is std::shared_ptr
	// to cached object (or null
	// if object's not in cache)
	if (!objPtr) { // if not in cache,
	objPtr = loadWidget(id); // load it
	cache[id] = objPtr; // cache it
	}
	return objPtr;
}
```
- Cache doesn't prevent `Widget` destruction
- Stale entries automatically detected via `lock()`
- No manual cache cleanup needed

### 3. Observer Pattern (Safe Event Listeners)
```cpp
class Subject {
    std::vector<std::weak_ptr<Observer>> observers;
public:
    void notify() {
        // Remove expired observers while notifying
        std::erase_if(observers, [](auto& wp) {
            if (auto sp = wp.lock()) {
                sp->update();
                return false;  // Keep alive observers
            }
            return true;       // Remove dead observers
        });
    }
};
```
Observers can be destroyed independently without leaving dangling pointers.


### 4. Thread-Safe Lazy Initialization (Double-Checked Locking)
```cpp
class Factory {
    mutable std::mutex m;
    mutable std::weak_ptr<ExpensiveObject> cached;
public:
    std::shared_ptr<ExpensiveObject> get() const {
        if (auto sp = cached.lock()) return sp;  // Fast path (no lock)
        
        std::lock_guard lock(m);
        if (auto sp = cached.lock()) return sp;  // Re-check after lock
        
        auto sp = std::make_shared<ExpensiveObject>();
        cached = sp;
        return sp;
    }
};
```

`weak_ptr` enables lock-free fast path while safely handling object destruction.


## ⚠️ Important Caveats

### 1. `weak_ptr` ≠ Null Pointer
Both empty and expired `weak_ptr`s return `true` for `expired()`, but only the latter _was_ associated with an object.
```cpp
std::weak_ptr<Widget> wp;  // Empty weak_ptr (no control block)
wp.expired();              // true

auto sp = std::make_shared<Widget>();
wp = sp;
sp.reset();                // Widget destroyed
wp.expired();              // true (now dangling)
```

### 2. Thread Safety
- `weak_ptr` operations (`lock()`, `expired()`) are **thread-safe** with respect to the control block
- But `lock()` + use is **not atomic**:

```cpp
// ❌ Race condition!
if (!wp.expired()) {
    wp.lock()->doSomething();  // Object could die between checks!
}

// ✅ Safe
if (auto sp = wp.lock()) {
    sp->doSomething();  // sp keeps object alive during use
}
```


### 3. No Direct Dereferencing
```cpp
std::weak_ptr<Widget> wp = /* ... */;
wp->foo();  // ❌ Compilation error!
wp.lock()->foo();  // ✅ Must convert first
```



---

>[!IMPORTANT] **Things to Remember**
>- Use **std::weak_ptr** for **std::shared_ptr**-like pointers that can *dangle*.
>- Potential use cases for **std::weak_ptr** include *caching*, *observer lists*, and the prevention of *std::shared_ptr* cycles.