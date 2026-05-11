---
Created Date: 2026-05-11
tags:
  - golang
  - programming
---
---
## Variables and Data Types
In *Go* variables must be declared with their type, and *statically type* like *C++*.

1. Using `var` keyword (Explicit declaration)
```go
var message string // its intialised with its zero value ""
var count int // initialized with its zero 0
var isReady bool // 
var pi float64 // 
```

2. Using `:=` short variable declaration
```go
func example() {
	name := "Co programming" // string
	score := 100  // int
	active := true // bool
	ratio := 3.14159 // float64
	// You cannot redeclare a variable using := in the same scope if it already exists.
	name = "learining go" // assign a new value
}
```

### Key different with Python/C++
- **Static Typing:** Unlike Python, you don’t have `type()` or *duck typing*. Types are explicit or inferred at *compile time*. This offers *compile-time* safety, similar to *C++.*
- **Zero Values:** When you declare a variable without explicitly initializing it, Go assigns it a *“zero value”* (e.g., `0` for *numeric* types, `false` for *booleans*, `""` for *strings*, `nil` for *pointers*, *slices*, *maps*, *channels*, and *functions*). This is a convenient feature that Python doesn’t have (Python variables must be assigned a value) and *C++* requires careful *initialization*.
- **`:=` Operator:** This is Go’s concise way to declare and initialize. In *C++* , you’d use `auto` or explicit types. In Python, you just assign.
- **No Implicit Type Conversion:** Go is *strict* about *types*. You can’t directly add an *integer* to a *float* without *explicit* *conversion*, unlike Python where it might work or *C++* where it might *implicitly convert*.

### Common Data Type in GO
- **`int`:** Typically 32 or 64 *bits*, depending on the *architecture*. There are also `int8`, `int16`, `int32`, `int64` for specific sizes.
- **`uint`:** Unsigned integer types (`uint8`, `uint16`, `uint32`, `uint64`).
- **`float32`, `float64`:** Floating-point numbers. `float64` is generally preferred.
- **`complex64`, `complex128`:** Complex numbers.
- **`bool`:** `true` or `false`.
- **`string`:** *Immutable* sequence of *bytes*, typically representing `UTF-8` characters. Strings are enclosed in double quotes (`"`).
```go 
package main

import "fmt"

func main() {
    var companyName string = "Awesome Corp" // Explicit declaration and initialization
    year := 2023                        // Short declaration, inferred as int
    var isPublic = true                     // Short declaration, inferred as bool
    var stockPrice float64 = 199.99         // Explicit type and value

    fmt.Println("Company:", companyName)
    fmt.Println("Year:", year)
    fmt.Println("Is Public:", isPublic)
    fmt.Println("Stock Price:", stockPrice)

    // Type conversion example:
    var i int = 42
    var f float64 = float64(i) // Explicit conversion from int to float64
    fmt.Println("Converted float:", f)
}

```

---
## Control Flow in Go
You’ll find similarities to C++ but with some Go-specific nuances, particularly how `for` loops work.

1. **Conditional Statements (if, else if, else)**: