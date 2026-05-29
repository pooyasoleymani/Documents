---
Created Date: 2026-05-29
tags:
  - golang
  - programming
---
---
# Why Go Avoids Exceptions
Go designers wanted:
- predictable *control flow*
- simple *debugging*
- *explicit failure handling*
- low *runtime* complexity

```go
package main

import (
	"errors"
	"fmt"
)

func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}

	return a / b, nil
}

func main() {
	result, err := divide(10, 0)

	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println(result)
}
```

# Error in Go
In go *error* just a interface and defined in standard library

```go
type error interface 
```

# The Built-in Error Interface

```go
type error interface {
	Error() string
}
```
Any thing implementing this is an error


## `errors.New`
Creates simple *error*:

```go
errors.New("somthing failed")
```

## `fmt.Errorf`
More powerful:

```go
fmt.Errorf("user %s not found", name)
```


### Why `fmt.Errorf` is preferred often
**Dynamic context.**
```go
fmt.Errorf("cannot open file %s", filename)
```


## 🔥 Error Wrapping (VERY IMPORTANT)
Modern Go supports wrapping:

```go
fmt.Errorf("reading config: %w", err)
```


### Why wrapping matters
Preserves:
- *original error*
- *context chain*


## Error Comparison
Use:
```go
errors.Is(err, target)
///
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) {
	// ....
}
```



## Custom Error Types
Very important in real applications.

```go
type ValidationErro struct {
	Field string
}

func (v ValidationError) Error() string {
	return fmt.Sprintf("Invalid field: %s", v.Field)
}

// Usage
return ValidationError{Field: "email"}
```



### Why Custom Errors Matter
You can:
- *attach metadata*
- *inspect errors*
- build *structured systems*



# Panic 
**Panic** is something like *exception* and stop normal *execution*.

## When to use panic
ONLY for:
- *unrecoverable* programmer *errors*
- *impossible states*
- *startup failures*
NOT normal *business logic*.

```go
func main() {
	panic("boom!")
}
```

## Recover
*Go* allow *catching*  panic, but only inside *deferred* function.

`recover()` is mostly used by:
- **frameworks**
- **HTTP** servers
- **middleware**
NOT everyday *business logic*.

```go
package main

import "fmt"

func safe() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered:", r)
		}
	}()

	panic("boom")
}

func main() {
	safe()

	fmt.Println("program continues")
}
```


# Why `defer` Exists
Main purpose: **cleanup**
Examples:
- closing files
- unlocking mutexes
- closing DB connections
- network cleanup


```go
file, err := os.Open("data.txt")
if err != nil {
	return err
}

defer file.Close()
```

This guarantees:
- file closes
- even if function returns early


## 🔥 Deferred Calls Are STACKED (LIFO)

```go
package main

import "fmt"

func main() {
	defer fmt.Println("1")
	defer fmt.Println("2")
	defer fmt.Println("3")

	fmt.Println("start")
}

// start-> 3-> 2-> 1
```


## 🔥 Arguments Evaluated IMMEDIATELY

```go
package main

import "fmt"

func main() {
	x := 10

	defer fmt.Println(x)

	x = 20
}

// Output : 10
```

### Why?
Because arguments evaluated when `defer` is *declared*.
NOT when *executed*.


## 🔥 Deferred Closures Can Access Updated Variables
Different behavior.

```go
package main

import "fmt"

func main() {
	x := 10

	defer func() {
		fmt.Println(x)
	}()

	x = 20
}
```


### Why?
*Closure* captures *variable* itself,  
not value *copy*.

## 🔥 Named Return Values + defer (Advanced)
Go allows:

```go
func test() (x int)
```

Now **deferred functions** can modify **return** **value**.

```go
package main

import "fmt"

func test() (x int) {
	defer func() {
		x++
	}()

	x = 10

	return
}

func main() {
	fmt.Println(test())
}
```