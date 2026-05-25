---
Created Date: 2026-05-11
tags:
  - golang
  - programming
Next: "[[Structs, interfaces, and Go’s approach to OOP]]"
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

### 1. **Conditional Statements (if, else if, else)**
Go’s `if` statements are quite standard. A key difference from *C++* and *Java* is that the *parentheses* `()` around the *condition* are *optional*, and the opening *curly brace* `{` **must** be on the same line as the `if` statement. You can also *declare* a *variable* within the `if` condition (similar to *C++*'s *initialization* in condition)

```go 
package main

import "fmt"

func main() {
	score := 85
	
	if score >= 90 {
		fmt.Println("Exelent!")
	} else if score >= 75 {
		fmt.Println("Good")
	} else {
		fmt.Println("Fail")
	}
	
	if num:=1; num%2 == 0 {
		fmt.Println(num, "is Even")
	} else {
		fmt.Println(num, "is odd")
	}
	// num dosen't declare in this scope
}
```


---
### 2. **Switch Statements**
Go’s `switch` statement is powerful and flexible. It doesn’t require `break` statements (each case automatically *“breaks”* by default), and you *can* switch on any *type*, not just constants or *integers*.
```go 
package main

import (
	"fmt"
	"time"
)

func main() {
	day := "Monday"
	
	switch day {
		case "Monday":
			fmt.Println("start of the week")
		case "Friday":
			fmt.Println("end of week")
		default: // default case 
			fmt.Println("mid-week")
	}
	
	// Switching on type 
	whatAmI := time.Now() 
	switch whatAmI.(type) { // Using a type switch 
	case bool: 
		fmt.Println("I'm a boolean") 
	case int: 
		fmt.Println("I'm an integer") 
	case float64: 
		fmt.Println("I'm a float64") 
	case string: 
		fmt.Println("I'm a string") 
	case time.Time: // Specific to our variable 
		fmt.Println("I'm a time object") 
	default: 
		fmt.Println("I'm something else.") }
}
```

**Key Points for `switch`:**

- **No `break` needed:** Cases execute and then exit the `switch` block automatically. If you _want_ a case to fall through to the next one, you use the `fallthrough` keyword.
- **No need for `case` or `default` constants:** You can use any expression in `case`.
- **Type Switch:** A special form allows you to determine the dynamic type of an interface value.
- **Initialization Statement:** Similar to `if`, you can have an initialization statement before the `switch` expression.

---
### 3. `For` Loop
Go **only has the `for` loop**. It can be used in several ways to mimic `while` loops, C-style `for` loops, and more.

- The classic *C-style*  `for` loop:
```go
package main 

import "fmt"

func main() {
	
	for i:=0; i<=10;i++ {
		fmt.Println("Count", i)
	} 
}
```

- The `while` loop equivalent:
```go
package main

import "fmt"

func main() {
    sum := 1
    // Condition only: loop while condition is true
    for sum < 10 {
        sum += sum
        fmt.Println("Current sum:", sum)
    }
}

```

- *Infinite* loop:
```go
package main

import "fmt"

func main() {
    i := 0
    for { // Infinite loop
        fmt.Println("Looping...")
        i++
        if i >= 3 {
            break // Essential to break out of infinite loops
        }
    }
}

```

---
### `for range` loop (for iterating over collections):
This is used for iterating over *arrays*, *slices*, *strings*, *maps*, and *channels*. It’s very similar to Python’s `for`

```go 
package main

import "fmt"

func main() {
	nums := []int{1, 2, 3, 4}
	
	for index, value := range nums {
		fmt.Printf("Index: %d, Value: %d", index, value)
	}
	
	for _, value := range nums {
	 fmt.Println("Value:", value) 
	 }
	
	myMaps := map[string]int{"apple": 2, "banana": 3}
	
	for key, value := range myMap {
		fmt.Printf("Key: %s, Value: %d\n", key, val)
	}
	
	// Iterating over a string (gives rune index and rune value) 
	for index, runeValue := range "Go" {
	 fmt.Printf("Rune index: %d, Rune value: %c\n", index, runeValue) 
	 }
}
```

**Key Points for `for`:**

- **Single Loop Construct:** Go achieves all loop behaviors using `for`.
- **No Parentheses:** Like `if`, conditions in `for` do not require parentheses.
- **`for range`:** Extremely useful and idiomatic for collections. It returns two values: the index and the element (for slices/arrays/strings) or the key and value (for maps). You can ignore values using `_`.
---

## Functions and Methods
- Function are simple and explicit
- methods are just function with a *receiver*
- Go doesn't have class *OPP* like C++ *inheritance* 
- Go often returns *multiple values*, especially *(value, error)*

### 1. Basic function syntax

```go
func functionName(parameterName type, parameterName type) returnType {
    // body
}
```

```go
package main

import "fmt"

func add(x int, y int) intt {
	return x + y
}

func main() {
	result := add(2, 3)
	fmt.Println(result)
}
```

### 2. Shorter parameter typing
If consecutive parameters have the *same type*, you write the type once.
```go
func add(x, y int) int {
	return x + y
}
```


### 3. Multiple return values
Go prefers **explicit error handling** instead of *exceptions*.

- common style in Go:
```go
value, err := someFunction()
if err != nil {
    // handle error
}
```

```go 
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}
//
// Usage 
//
result, err := divide(10, 2)
if err != nil {
    fmt.Println("error:", err)
    return
}
fmt.Println("result:", result)
```

#### Why this matter
In *Python*, you may *raise* *exceptions*.
In *C++*, you may:
- throw *exceptions*
- return *status codes*
- use `std::optional` or similar patterns


### 4. Returning multiple normal values
```go
func swap(a, b string) (string, string) {
	return b, a
}

// Usage
x, y := swap("hello", "world")
fmt.Println(x, y)
```


### 5. Named return values
Go allows *naming* return values.
```go
package main

func rectangle(width, height int) (area int, perimeter int) {
	area = width * height 
	perimeter = 2 * (width + height) 
	return
}
```

### 6. function with no return value 
```go
func greet(name string) {
    fmt.Println("Hello,", name)
}
```


### 7. Variadic functions
Like Python’s `*args` and C++ *variadic template*
```go
func sum(nums ...int) int {
	total := 0
	for _, value := range nums {
		total += value
	}
	return total
}

// usage
fmt.Println(sum(1, 2, 3)) 
fmt.Println(sum(10, 20, 30, 40))
```

- If we have *slice* the `...` can expands the *slice*:
```go 
numbers := []int{1, 2, 3, 4 ,5, 6}
fmt.Println(sum(numbers...)) 
```



### 8. Functions are first-class values
Like *Python* and modern *C++* *lambdas/function objects*, *functions* in Go can be assigned to variables and passed around.
```go
func mitliply(a, b int) int {
	return a * b
}

func main() {
	op := multiply
	fmt.Prinln(op(3, 5))
}
```


### 9. Anonymous functions
```go 
package main

import "fmt"

func main() {
	greet := func(name string) {
		fmt.Println("Hello.", name)
	}
	greet("Ali")
}
```

- We can invoke function immediately:
```go
func() {
	fmt.Println("run immediatly")
}()
```



### 10. Closures
A **closure** is *function* that captures *variables* from its surrounding *scope* , this is similar to *Python* **closures** and *C++* *lambdas capturing* variables.
```go 
func counter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// usage
c := counter()
fmt.Println(c()) // 1
fmt.Println(c()) // 2
```


### 11. Methods in Go
A **method** is just a function with a *receiver*.
```go
type Rectangle struct {
	Width float64
	Height float64
}

func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

// Usage 
rect := Rectangle{Width: 10, Height: 5}
fmt.Println(rect.Area())
```


### 12. Value receiver vs pointer receiver
This is very important.

- **Value receiver:** This *modifies* only a *copy*.
```go
func (r Rectangle) Scale(factor float64) {
	r.Width *= factor
	r.Height *= factor
}
```

- **Pointer receiver:** This *modifies* the original *object*.
```go
func (r *Rectangle) Scale(factor float64) {
	r.Width *= factor
	r.Heigth *= factor
}
// Usage
rect := Rectangle{Width: 10, Height: 5}
rect.Scale(2)
fmt.Println(rect.Width, rect.Height) // 20 10

```


>[!NOTE]
>*Go* automatically handles some *pointer* syntax for *method* calls, which makes usage feel *cleaner* than *C++ pointers*.



### 13. When to use pointer receivers
- Use a pointer receiver when:
	- you want to *modify* the *receiver*
	- *copying* the *struct* is *expensive*
	- you want *consistency* across *methods* on the same type

```go
type User struct {
    Name string
    Age  int
}

func (u *User) Birthday() {
    u.Age++
}
```


### 14. Structs + methods feel like lightweight classes
- Go doesn’t have *classes*, but this *combination*:
	- `struct`
	- *methods*
	- *interfaces*


> **gives you most of what you need for application design.**

```go
package main

import "fmt"

type BankAccount struct {
    Owner   string
    Balance float64
}

func (b *BankAccount) Deposit(amount float64) {
    b.Balance += amount
}

func (b *BankAccount) Withdraw(amount float64) error {
    if amount > b.Balance {
        return fmt.Errorf("insufficient balance")
    }
    b.Balance -= amount
    return nil
}

func (b BankAccount) Display() {
    fmt.Printf("Owner: %s, Balance: %.2f\n", b.Owner, b.Balance)
}

func main() {
    account := BankAccount{Owner: "Sara", Balance: 1000}

    account.Deposit(500)

    err := account.Withdraw(300)
    if err != nil {
        fmt.Println("error:", err)
        return
    }

    account.Display()
}
```




### 15. Key differences from Python and C++
##### Compared to Python
- no *default arguments*
- no *keyword arguments*
- no *exceptions* as normal *error handling*
- *methods* are *attached* to types, but no *class* system like Python
- *explicit* types everywhere

##### Compared to C++
- much simpler *syntax*
- no *default arguments*
- no *function overloading*
- no *constructors* in the *C++* sense
- no *inheritance*
- no *templates* in the old *C++* sense, though modern Go has *generics*
- *methods* with *receivers* instead of *member functions* inside *classes*



### 16. Important limitation: no function **overloading**

This is normal in *C++* but not in *Go*,  you cannot define multiple *functions* with the same *name* in the same *package*.
```cpp
int add(int a, int b);
double add(double a, double b);
```

- So you use:
	- *different* names
	- *interfaces*
	- *generics*
	- different *parameter* types through *design*



### 17. Idiomatic Go error pattern

```go
value, err := doSomething()
if err != nil {
    return err
}
```

As a *Python developer*, this may feel *repetitive* at first.
As a *C++ developer*, it may feel more *explicit* than *exceptions*.
But in *Go*, this is one of the core *design philosophies*:
- *simple*
- *explicit*
- *predictable*



### 18. Mini example combining functions and methods

```go
package main

import "fmt"

type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14 * c.Radius * c.Radius
}

func describeCircle(c Circle) string {
    return fmt.Sprintf("Circle with radius %.2f has area %.2f", c.Radius, c.Area())
}

func main() {
    circle := Circle{Radius: 5}
    fmt.Println(describeCircle(circle))
}
```



### 19. Mental model you should keep

- Think of Go like this:
	- **functions** = standalone behavior
	- **methods** = behavior attached to a type
	- **structs** = data containers
	- **interfaces** = behavior contracts
	- **errors** = explicit returned values

This mental model is extremely important for designing applications in Go.