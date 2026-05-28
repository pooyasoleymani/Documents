---
Created Date: 2026-05-28
tags:
  - golang
  - programming
---
---
## Name Rule
1. letters
2. digits
3. `_`
But names can't start with *digit*

```go
count
count1
_count
myVariable
```

## Uppercase and Lowercase
- For exported names are *Uppercase*
```go
TextStatus
PrintStats
```

- For unexported names are *Lowercase* 
```go
textStats
printStats
```


### This Is Go’s Visibility System
No:
- public
- private
- protected
> **Just naming convention.**



---
## Declaration

### 1. `var` method
zero value automatically assigned and we can initialize with `=` assignment operator
```go
var name string
var name string = "go"
```

### 2. Type Interface
Compiler can infer type

```go
var name = "go"
```


### 3. Shirt Declaration
we can use `:=` operator 
```go
name := "go"
```

>[!WARNING]
>Don't declare one variable again
>```go
>name := "go"
>name := "golang"
>```



---

## `new` function
With `new` function we can create pointer of one type.
**allocate zeroed storage for type T and return pointer**
```go
p := new(int)
```

This creates:
- *pointer* to *int*
- *initialized* with *zero value*

```go
package main

import (
	"fmt"
)

func main() {
	type User struct {
		Name string
		Age int
	}
	
	user := new(User)

	fmt.Println(user.Name)
	fmt.Println(user.Age)
}
```


---
## What Is Lifetime?
How long *variable* exists in *memory*.
Go *separate* variable *lifetime* from *scope* 
So Go *allocates* it on *heap* automatically.
This is called: **escape analysis**
```go
func createPointer() *int {
	x := 10
	return &x
}
```


## Package Variables
Exist for entire program *lifetime*.

```go 
var global int // outside function
```


---
## `init` function
This function run before `main()`

```go
package main 

import "fmt"

func init() {
	fmt.Println("init run before main")
}

func main() {
	fmt.Println("main function runed")
}
```


## Important warning
`init()` is powerful but should be used carefully.
Good use cases:
- **setup configuration**
- **initialize constants**
- **register drivers**

Bad use cases:
- **heavy logic**
- **business rules**


---
## Package Initialization Order
Go initializes in this order:
1. **imported packages**
2. **package-level variables**
3. `init()`
4. `main()`


---
## String
1. *Immutable*
2. *UTF-8 encoded*
3. *byte sequences*

### `len()` in string
Return *bytes* not *characters*

```go
s := "é"
fmt.Println(len(s)) // ---> 2
```

### Unicode and Runes
> `rune = int32 alias`

Represents a *Unicode* code point. 
```go
r := 'A'
fmt.Printf("%T\n", r) // int32
```


### String iteration

```go
for i, r := range "héllo" {
	fmt.Printf("%d %c\n", i, r)
}
```

- i = byte index
- r = rune(charter)


### strings are immutable
```go
s := "hello"
s[0] = 'H' // ❌ error
```

- Correct way
```go
b := []byte("hello")
b[0] = 'H'
s := string(b)
```

### Split
```go
strings.Split("a,b,c", ",")
```