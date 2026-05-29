---
Created Date: 2026-05-28
tags:
  - golang
  - programming
---
---
# Interface Use cases
- backend systems
- cloud infrastructure
- networking
- large-scale services


# What is an Interface?
An **interface** defines:
- *behavior*
- *method set*
*NOT data*.

```go 
type Speaker interface {
	Speak() 
}
```

Meaning:
> *Any type* with `Speak()` *method* satisfies this *interface*.


## VERY Important Go Philosophy
Go **interfaces** are:
 *implicit* NOT *explicit*.


```go
package main

import "fmt"

type Speaker interface {
	Speak()
}

type Dog struct {
	Name string
}

func (d Dog) Speak() {
	fmt.Println(d.Name, "says woof")
}

func main() {
	var s Speaker

	s = Dog{Name: "Max"}

	s.Speak()
}
```


## Why Interfaces Matter
Interfaces allow:
```
different types
same behavior
```

```go
type Cat struct {
	Name string
}

func (c Cat) Speak() {
	fmt.Println(c.Name, "says meow")
}
```


## Polymorphism is  Go
```go
func makeSpeak(s Speaker) {
	s.Speak()
}

makeSpeak(Dog{Name:"Max"})
makeSpeak(Cat{Name:"Luna"})
```

## This Is HUGE
**Behavior-based programming**.
NOT *inheritance-based programming*.


### Design Philosophy
**Interfaces** most be small

```go
type Reader interface {
	Read(p []byte) (n int, err error)
}
```

### Anti pattern

```go
type MegaManager interface {
	Run()
	Stop()
	Read()
	Write()
	Close()
	...
}
```


## This Is Why Go Interfaces Are Powerful
*Small interfaces* are:
- *composable*
- *reusable*
- *flexible*


## VERY Important Engineering Insight
*Interfaces enable*:
- decoupling
- testing
- extensibility
- dependency injection
This is foundational for large Go systems.

## VERY Important Go Philosophy
In Go:
> accept *interfaces*, return *structs*


---
# Empty Interface (`interface{}`) and `any`
This is the bridge between:
- **static typing** (Go’s strength)
- **dynamic data** (JSON, logs, generic input)

## What is `interface{}`?
Every `interface{}` value stores:  `(type, value)`

```go
var x interface {}

// Modern Go
var x any
```

## ⚠️ Important Warning
You lose *type safety*.
So Go forces you to **check types manually**.


## Type Assertion
If wrong type → **program crashes**.
```go
var x any = "hello"
s := x.(string)
fmt.Println(s)
```

- Safe version
```go
s, ok := x.(string)
if ok {
	fmt.Println(x)
} else {
	fmt.Println("not a string")
}
```