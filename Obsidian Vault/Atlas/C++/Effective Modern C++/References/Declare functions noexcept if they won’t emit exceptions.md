---
Created Date: 2026-02-02
tags:
  - cpp
  - programming
Up: "[[Prefer const_iterators to iterators]]"
Next: "[[Use constexpr whenever possible]]"
---
---
## C++98 vs C++11 Exception Specifications
### C++98: `throw()`
- Had to list specific *exception types*
- **Brittle**: changing implementation often required changing specification
- *Compilers* didn't enforce *consistency*
- Most programmers *avoided* them

### C++11: `noexcept`
- Simple *binary choice*: either `noexcept` or not
- Part of function interface (like `const`)
- *Compilers* can *optimize* based on it


---

<<<<<<< HEAD:Obsidian Vault/+/Atlas/C++/Effective Modern C++/References/Declare functions noexcept if they won’t emit exceptions.md

##  The Evolution: A Historical Perspective
=======
## The Evolution: A Historical Perspective
>>>>>>> 970e5a1657f4ec0c0cd22b1dd1925b9f73b1213b:Obsidian Vault/Atlas/C++/Effective Modern C++/References/Declare functions noexcept if they won’t emit exceptions.md

 - C++98: The Fragile `throw()` Specification
```cpp
// C++98 style - very problematic
void processFile() throw(IOException, SystemError, std::bad_alloc);
void calculate() throw();  // Empty list means "won't throw"
```


### Problem with C++98 Approach:

1. **Static Checking at Compile Time:**
```cpp
void helper() {
    throw 42;  // Throws int
}

void badFunction() throw(std::string) {  // Promises only std::string
    helper();  // COMPILE ERROR (if compiler checks) or UNDEFINED BEHAVIOR
}
```


2. **Runtime Overhead**:
When an *exception* *violates* the specification, the program calls `std::unexpected()`, which typically *terminates*. But before *termination*:
- *Stack* must be fully *unwound*
- All objects must be *destroyed* properly
- This requires *significant* *runtime* *bookkeeping*


2. **Maintenance Nightmare**:
```cpp
// Version 1
class Database {
    void connect() throw(NetworkError);  // Only network errors
};

// Version 2 - Added new error type
class Database {
    void connect() throw(NetworkError, AuthenticationError);  // Changed!
    // All callers must be reviewed!
};
```


##  C++11: The Simple `noexcept` Model

```cpp
// C++11 style - simple binary choice
void safeOperation() noexcept;     // Guaranteed no exceptions
void riskyOperation();             // May throw exceptions
```


### Stack Unwinding: The Key Difference

```cpp
void function() {
    Resource r1;  // Constructor may throw
    Resource r2;  // Constructor may throw
    // Compiler MUST generate code to:
    // 1. Track construction order (r1 then r2)
    // 2. Prepare to destroy in reverse order (r2 then r1)
    // 3. Keep stack frame unwindable
    operation();  // May throw
}
```

- **With `noexcept`:**
```cpp
void function() noexcept {
    Resource r1;
    Resource r2;
    operation();  // Compiler assumes no exceptions
    // Compiler CAN:
    // 1. Skip tracking destruction order
    // 2. Keep stack in non-unwindable state
    // 3. Optimize away exception handling tables
}
```


### Real Compiler Output Comparison

Consider this simple function:
```cpp
// Case 1: No exception specification
int sum1(int a, int b) {
    return a + b;
}

// Case 2: noexcept
int sum2(int a, int b) noexcept {
    return a + b;
}
```


#####  **What compilers can do with `sum2`**:
1. **Inlining**: More aggressive *inlining* since no *exception* handling code
2. **Code Motion**: Move operations around more freely
3. **Register Allocation**: Better register usage without EH overhead
4. **Smaller Binary**: No *exception* handling tables (.*gcc_except_table*)




<<<<<<< HEAD:Obsidian Vault/+/Atlas/C++/Effective Modern C++/References/Declare functions noexcept if they won’t emit exceptions.md
### The Standard Library's Critical Dependency on `noexcept`
=======
###  The Standard Library's Critical Dependency on `noexcept`
>>>>>>> 970e5a1657f4ec0c0cd22b1dd1925b9f73b1213b:Obsidian Vault/Atlas/C++/Effective Modern C++/References/Declare functions noexcept if they won’t emit exceptions.md

#####  `std::vector`: The Perfect Case Study

```cpp
// Simplified vector::push_back implementation
void push_back(const T& value) {
    if (size_ == capacity_) {
        // Need to reallocate
        T* new_buffer = allocate_new_memory(capacity_ * 2);
        
        // MOVE or COPY existing elements?
        if constexpr (std::is_nothrow_move_constructible_v<T>) {
            // SAFE: Move elements - won't throw
            for (size_t i = 0; i < size_; ++i) {
                new (&new_buffer[i]) T(std::move(buffer_[i]));
                buffer_[i].~T();  // Destroy old
            }
        } else {
            // RISKY: Copy elements
            size_t i = 0;
            try {
                for (; i < size_; ++i) {
                    new (&new_buffer[i]) T(buffer_[i]);  // Copy
                }
            } catch (...) {
                // Rollback: destroy what we copied
                for (size_t j = 0; j < i; ++j) {
                    new_buffer[j].~T();
                }
                deallocate(new_buffer);
                throw;  // Strong guarantee preserved!
            }
            // Destroy old elements
            for (size_t i = 0; i < size_; ++i) {
                buffer_[i].~T();
            }
        }
        
        deallocate(buffer_);
        buffer_ = new_buffer;
        capacity_ *= 2;
    }
    
    // Add new element
    new (&buffer_[size_]) T(value);
    ++size_;
}
```


##### The Performance Impact: **Real Numbers**

```cpp
struct HeavyObject {
    std::array<double, 1000> data;
    
    // Version A: noexcept move
    HeavyObject(HeavyObject&& other) noexcept = default;
    
    // Version B: throwing move (or no noexcept)
    HeavyObject(HeavyObject&& other) { /* might throw */ }
};
```

**Benchmark results** (typical):
- With `noexcept` moves: 10,000 **push_back**s take **5ms**
- Without `noexcept` moves: 10,000 **push_back**s take **50ms** (10x slower!)


---

## Conditional `noexcept`: Advanced Usage

### Understanding the Syntax

```cpp
template<typename T>
void swap(T& a, T& b) noexcept(noexcept(a.swap(b)));
// Outer noexcept: function's exception specification
// Inner noexcept(...): Boolean condition
// The expression checks if a.swap(b) is noexcept
```


### Practical Example: Smart Pointer

```cpp
template<typename T>
class UniquePtr {
    T* ptr;
    
public:
    // Destructor - implicitly noexcept
    // Move constructor - conditionally noexcept
    UniquePtr(UniquePtr&& other) noexcept 
        : ptr(other.ptr) {
        other.ptr = nullptr;
    }
    
    // Move assignment
    UniquePtr& operator=(UniquePtr&& other) noexcept {
        delete ptr;
        ptr = other.ptr;
        other.ptr = nullptr;
        return *this;
    }
    
    // Dereference - never throws
    T& operator*() const noexcept {
        return *ptr;
    }
    
    // Arrow operator - never throws  
    T* operator->() const noexcept {
        return ptr;
    }
    
    // Reset - conditionally noexcept based on deleter
    void reset(T* p = nullptr) noexcept(noexcept(std::declval<Deleter>()(ptr))) {
        delete ptr;
        ptr = p;
    }
};
```

---

## The `noexcept` Operator: Compile-Time Detection

```cpp
// Check if an expression can throw
template<typename T>
constexpr bool can_throw_move = !noexcept(T(std::declval<T>()));

// Usage
static_assert(can_throw_move<std::string>, "string moves might throw");
static_assert(!can_throw_move<int>, "int moves never throw");

// Conditional compilation based on noexcept
template<typename T>
void process(T&& obj) {
    if constexpr (noexcept(T(std::forward<T>(obj)))) {
        // Fast path - use moves
        process_fast(std::forward<T>(obj));
    } else {
        // Safe path - use copies
        process_safe(obj);
    }
}
```


---

## Exception Safety Guarantees and `noexcept`
### The Three Levels:
1. **No-throw guarantee**: `noexcept` functions
2. **Strong guarantee**: Either complete success or no effect
3. **Basic guarantee**: No resource leaks on failure

```cpp
class Transaction {
    Database& db;
    std::vector<Operation> operations;
    
public:
    // Strong guarantee (but not noexcept - might fail)
    void execute() {
        auto backup = operations;  // Copy - might throw
        
        try {
            for (auto& op : operations) {
                db.execute(op);  // Might throw
            }
        } catch (...) {
            // Rollback
            operations = std::move(backup);
            throw;
        }
    }
    
    // No-throw guarantee
    void clear() noexcept {
        operations.clear();  // clear() is noexcept
    }
};
```


---

## Advanced Patterns and Pitfalls

### The `noexcept` Destructor Rule

```cpp
class ResourceHolder {
    FILE* file;
    
public:
    ~ResourceHolder() {
        // DANGER: fclose might fail!
        if (file) fclose(file);  // Not noexcept!
    }
    // Implicitly noexcept(false)! Violates Rule of Five
};
```

**FIX:**
```cpp
class ResourceHolder {
    FILE* file;
    
public:
    ~ResourceHolder() noexcept(false) {  // Explicit!
        if (file) {
            int result = fclose(file);
            if (result != 0) {
                // Log error, but can't throw from destructor!
                std::terminate();  // Or handle differently
            }
        }
    }
};
```


### `noexcept` and Virtual Functions

```cpp
class Base {
public:
    virtual void process() noexcept;  // All overrides must be noexcept
};

class Derived : public Base {
public:
    void process() noexcept override;  // OK
    // void process() override;  // ERROR: less restrictive
};

class BadDerived : public Base {
public:
    void process() override;  // ERROR: Base is noexcept
    // Can't make virtual function less restrictive
};
```


---

## Real-World Guidelines
### When to Use `noexcept`:
. **✅ Always**:
- *Move constructors* and *move assignment* operators
- *Swap functions* (member and non-member)
- *Destructors* (unless they call throwing operations)
- Simple *getters* and *trivial* operations
        
2. **✅ Consider**:  
- *Functions* that only call other `noexcept` functions
- *Mathematical* *operations* on built-in types
- *Memory management* functions
        
2. **❌ Avoid**:
- Functions that *allocate memory* (unless using `nothrow` versions)
- Functions that call *virtual functions* (unless you control all overrides)
- Functions that perform *I/O operations*


### The Decision Flowchart:

```
Should function be noexcept?
         │
         ▼
Does it guarantee no exceptions?
         │
    ┌────┴────┐
    │         │
    Yes       No
    │         │
    ▼         ▼
Use      Don't use
noexcept noexcept
    │         │
    ▼         ▼
Check if   Consider if
all called it should offer
functions  strong exception
are also   safety instead
noexcept
```


---
## Performance Case Study: `std::sort`

```cpp
// Without noexcept on swaps:
// - sort must assume swap might throw
// - Cannot use certain optimizations
// - Must preserve strong exception safety

// With noexcept swaps:
// - sort can use faster algorithms
// - Can rearrange elements more aggressively
// - ~30-50% faster for large collections

template<typename RandomIt>
void sort(RandomIt first, RandomIt last) {
    // If swap is noexcept, use faster unstable sort
    if constexpr (noexcept(std::iter_swap(first, first + 1))) {
        unstable_fast_sort(first, last);
    } else {
        stable_safe_sort(first, last);
    }
}
```



## The Future: Contracts and Beyond
*C++20* and beyond are exploring contracts, which combine with `noexcept`:
```cpp
// Hypothetical C++23
void process(int x) 
    [[pre: x > 0]]           // Precondition
    [[post: result > x]]     // Postcondition  
    noexcept                 // Exception specification
{
    return x * 2;
}
```


## Summary: The Complete Picture
`noexcept` is not just an optimization hint—it's a fundamental part of C++'s type system and contract system. It affects:

1. **Performance**: Enables compiler optimizations
2. **API Design**: Part of function's contract
3. **Standard Library**: Determines algorithm choices
4. **Exception Safety**: Integral to safety guarantees
5. **Binary Compatibility**: Affects ABI in some cases

**Golden Rule**: If you know a function won't throw, declare it `noexcept`. Your containers, algorithms, and callers will thank you with better performance and clearer interfaces.
