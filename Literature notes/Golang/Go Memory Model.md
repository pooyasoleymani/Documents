---
Created Date: 2026-05-11
tags:
  - golang
  - programming
---
---
Go design to simple but under the hood it still has:
	-  *Stack memory*
	- *Heap memory*
	- *Pointers*
	- *Garbage collection*
	- *Escape analysis*

> The key difference from *C++* is that *Go* tries to *manage* most *memory* automatically.


---
### 1. Stack vs Heap
##### Stack 
Used for *short-lived*, *local data*
- vary fast
- automatically *cleaned up* when a function returns
- usually preferred for *small value*

##### Heap
Used for data that must live beyond the current *function call*.

- managed by *garbage collector*
- slightly *slower* than *stack*
- used when the *compiler* decides a value must *“escape”*


### 2. Pointer
A *pointer* holds the *address* of a value.
```go
package main

import "ftm"

func main() {
	x := 10
	p := &x
	fmt.Println("x =", x) 
	fmt.Println("p =", p) 
	fmt.Println("*p =", *p) 
	*p = 20 
	fmt.Println("x after change =", x)
}
```

##### Output idea
- `&x` gives *address* of `x`
- `*p` *dereferences* the pointer
- changing `*p` changes the original *variable*


### 3. Pointer syntax compared to C++
##### If you know *C++*, this feels familiar:

- `&x` → *address* of `x`
- `*p` → *dereference* pointer

##### But *Go* is simpler:

- no *pointer* **arithmetic**
- no `++` on *pointers*
- no *manual* `delete`
- no `new`/`free` *management* like C++

> So *Go* gives you *pointer* power without *low-level memory* danger.



### 4. new vs &
We can create *pointer* in two ways.
```go 
// using &
x := 40
p1 := &x

// using new
p2 := new(int)
ftm.Println(*p2)
*p2 = 40
```

##### Difference
- `new(type)` allocates zeroed memory for type `T` ant return `*T`.
-  `&x` return address of an existing *variable*.


### 5. struct pointer
This is very common to using in *method*.
```go
type User struct {
	Name string
	Age int
}

func birthday(u *User) {
	u.Age++
}

u := User{Name: "pooya", Age: 35}
brithday(&u)
fmt.Println(u.Age) //  36
```

Because `birthday` **receives** a *pointer*, it can modify the original *struct*.




### 6. Go automatically dereferences in many cases
Go is convenient here.

```go
type Counter struct {
    Value int
}

func (c *Counter) Increment() {
    c.Value++
}

func main() {
    c := Counter{Value: 10}
    c.Increment() // Go automatically takes &c
}

// We dont neeed to write     (&c).Increment()
```


### 7. Why pointers matter in Go
**Use pointers when:**
- you want to *modify* the *original value*
- copying the value is *expensive*
- you want to avoid large *struct* copies

```go
type BigData struct {
	A [100000]int
}
```



### 8. Escape analysis
Go decides whether a variable can stay on the *stack* or must *move* to the *heap*.

*Example:* no escape
```go
func local() int {
	x:= 10
	return x
}
```
- `x` is *local variable* and stay in *stack*

*Example:* escape through pointer return
```go
func makePointer() *int {
	x := 10
	return &x
}
```
- Here, `x` must survive after the function ends, so it escapes to the *heap*. Why? Because returning `&x` would otherwise point to invalid *stack memory*.


### 9. Escape from Closure
```go
func counter() func() int {
	x := 0
	return func() int {
		x++
		return x
	}
}
``` 

- The variable `x` must survive after `counter()` returns, so it *escapes*.



### 10. Escape through interface
Sometimes values *escape* because they are stored in an *interface* value.

```go
func store(v interface{}) {
	_ = v
}

func store(v any) {
	_ = v
}
```
- If a value is *converted* into an *interface*, the *compiler* may decide it must *allocate* more carefully depending on usage.
- You don’t usually need to worry about this at the start, but it becomes important in *performance-*sensitive* code.
##### Why use it?
It’s used when a *function* must *accept* many *types*. (like *std::any* in c++)




### 11. Garbage collection
Go uses a *garbage collector* to reclaim *heap memory* automatically.
That means:
- you do **not** manually *free memory*
- *memory* is *cleaned up* when no longer *reachable*
- you don’t get the same *class* of *bugs* as *manual memory management* in C++

##### Benefit
Much *safer* and *easier*.

##### Tradeoff
A bit of *runtime overhead*.
For most applications, this *tradeoff* is excellent.




### 12. Zero values and memory
Go *initializes* all variables to *zero values*.

```go 
var i int
var s string
var f float64
var b bool
var p *int // nil
```


### 13. `nil` in Go
`nil` is like “no value” for:
- *pointers*
- *slices*
- *maps*
- *channels*
- *functions*
- *interfaces*
```go
var pi *int
fmt.Println(p==nil) // true
```

> Trying to dereference `nil` causes a *runtime panic*.



### 14. Common memory pitfalls
##### Dereferencing `nil`
```go 
var p *int
fmt.Println(*p) // panic
```

##### Returning references to temporary misunderstandings
Go handles most of this *safely*, but you should still understand what *escapes*.

##### Copying large structs unintentionally
If a *struct* is large, pass a *pointer* instead of a *value*.



### 15. Stack vs heap intuition
A simple mental model:

- **stack**: fast, temporary, local
- **heap**: longer-lived, shared, or escaping

>[!NOTE]
>Go tries to keep things on the *stack* when possible.


### 16. Practical example
```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func makePerson(name string, age int) *Person {
    p := Person{Name: name, Age: age}
    return &p
}

func celebrateBirthday(p *Person) {
    p.Age++
}

func main() {
    person := makePerson("Ali", 25)
    celebrateBirthday(person)

    fmt.Println(person.Name, person.Age)
}
```


#### What happens here?
- `p` is created inside `makePerson`
- returning `&p` makes it *escape*
- Go moves it to the heap if necessary
- `celebrateBirthday` modifies it through a *pointer*



### # 17. How to think like a Go developer

**Don’t think:**
- “I must manually manage memory”

**Think:**
- “Will this value need to outlive this function?”
- “Should I pass by value or pointer?”
- “Is this struct small enough to copy?”
- “Will this closure keep data alive?”



### 18. When to use value vs pointer
##### Use value when:
- the type is *small*
- *immutability* is fine
- you want to avoid *shared* *mutable* *state*

##### Use pointer when:
- you need *mutation*
- the *struct* is *large*
- copying is *wasteful*
- the method should *modify* the *receiver*



### 19. Very important Go style note
Go developers often prefer **simple code first**, performance second unless profiling says otherwise, So:
- use *values* for *small immutable structs*
- use *pointers* for *mutable* or *large objects*
- don’t prematurely *optimize*

---
### Summery
- *pointers* are *safe* and *simple*
- the *compiler* decides *stack* vs *heap*
- *escaping* values may *move* to the *heap*
- *garbage collection* handles *cleanup*
- you usually don’t manage *memory manually*