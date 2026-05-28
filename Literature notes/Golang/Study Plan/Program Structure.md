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


---
## Arrays
An array in Go has:
- **fixed size**
- **contiguous memory**
- **same-type element**
```go 
var numbers [4]int
```

- Arrays can't assign to each other
```go
var a [4]int
var b [5]int

b = a // Error
```

### Arrays initialization
```go
numbers := [5]intP{1, 2 ,3 , 4, 5}

var x [5]int // all elements are 0
```

- arrays can be *assignable* 
```go

numbers[4] = 100 
fmt.Println(numbers[4])
```

- arrays *length*
```go
len(numbers)
```

### Compare With C++
In C++ arrays *decay* into *pointers often*.
In Go:
- arrays are *real values*
Safer and more predictable.

### Arrays Are Value Types
```go
a := [5]int
b := a
b[4] = 100
```

- **full array copied**

### Why Arrays Are Rare in Go
Because:
- *fixed size* inconvenient
- *copying expensive*
Most *Go* code uses:
### slices


---
## Slices (CRITICAL)
### What Is Slice?
A slice is:
- *lightweight view* into array
- *dynamic-sized*
- *reference-like* *structure*

```go
numbers := []int{1, 2, 3}
```

### VERY Important Mental Model

```go
pointer + length + capacity
```

### Slice Shares Underlying Data
Because slices *reference* same *underlying array*.
```go
a := []int{1, 2, 3}
b := a
b[1] = 100
fmt.Println(a[1]) // 100
```

#### This Is Critical
Slices behave somewhat like:
- **shared views**
- **descriptors**
NOT *full copies*.


### Creating Slice with `make`
```go
numbers := make([]int, 5)
```


### Length and Capacity
```go
len(numbers)
cap(numbers)
```

#### Important Difference
**Length**:
- *accessible elements*
**Capacity**:
- *underlying storage size*


### Appending
The append *built-in function* appends *elements* to the end of a *slice*. If  it has *sufficient* *capacity*, the destination is *resliced* to accommodate the  new *elements*. If it *does not*, a new *underlying* array will be *allocated*. Append returns the *updated slice*.
`append()` may:
- **reuse array**  
    OR
- **allocate new array**


### Slice Expressions

```go
s[low: high]
```


### Copying Slices Properly
The copy *built-in function* *copies* elements from a *source* *slice* into a *destination* *slice*. (As a special case, it also will copy *bytes* from a  *string* to a *slice of bytes*.) The *source* and *destination* may *overlap*. *Copy* returns the *number* of elements *copied*, which will be the *minimum* of  `len(src)`and`len(dst)`.

```go
src := []int{1,2,3}
dst := make([]int, len(src))

copy(dst, src)
```

> Now:
> - **independent slices**



---
## Maps
Maps in Go are:
- hash tables
- key → value storage
- reference-like types
- extremely common in backend systems

- *nil* map
```go 
var m map[string]int
m["a"] = 1 // ❌ panic
```

- Create *map* with `make()`
```go
m := make(map[string]int)
m["a"] = 1
```

### Missing keys
If keys does not exist it return *zero-value* of the type, *no exception*
```go
fmt.Println(m["x"]) // 0
```

### Safe Lookup pattern
```go
value, ok := m["x"]
fmt.Println(value)  // 0
fmt.Println(ok)    // false
```

This pattern used every where in *Go*:
```go
if value, ok := m[key]; ok {
	// use value
}
```


### Deleting from map
Whit built-in function `delete()`
```go
delete(m, "a")
```


### Iterating in map
Go does NOT guarantee order.
because:
- **maps** are *hash-based*.

```go
for key, value := range m {
	fmt.Println(key, value)
}
```

### Sort maps
1. store keys
2. sort keys with *slice* package
3. Iterate 

```go
keys := make([]string, len(m))
for k := rage m {
	keys = append(keys, k)
}

slice.Sort(keys)

for _, key := range keys {
	fmt.Println(k, m[key])
} 
```


### Map with struct values
This is very common in *Go*

```go
type User struct {
	Name string
}

users := make(map[string]User)

// Or Pointer values for share updates
users := make(map[string]*User)
```

### Maps are reference types
If one *map* assign to other both *share* same *underling data* (like *slice*)

```go
m := make(map[string]int)

m["a"] = 1

m2 := m
m2["a"] = 100

fmt.Println(m["a"])
```


# VERY IMPORTANT ENGINEERING INSIGHT
Maps are used for:
- caching
- indexing
- counting
- configuration
- deduplication
- state tracking

