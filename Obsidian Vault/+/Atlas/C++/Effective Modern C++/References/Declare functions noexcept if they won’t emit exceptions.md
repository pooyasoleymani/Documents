---
Created Date: 2026-02-02
tags:
  - cpp
  - programming
Up: "[[Prefer const_iterators to iterators]]"
Next:
---
---

## ## The Evolution: A Historical Perspective

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


## ### C++11: The Simple `noexcept` Model

```cpp
// C++11 style - simple binary choice
void safeOperation() noexcept;     // Guaranteed no exceptions
void riskyOperation();             // May throw exceptions
```


### ### Stack Unwinding: The Key Difference

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


### ### Real Compiler Output Comparison

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




### ## The Standard Library's Critical Dependency on `noexcept`

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