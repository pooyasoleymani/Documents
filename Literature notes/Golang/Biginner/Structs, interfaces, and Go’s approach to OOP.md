---
Created Date: 2026-05-11
tags:
  - golang
  - programming
Next: "[[Go Memory Model]]"
---
---
### 1. Struct in Go
`struct` in Go is a container of *data*
- C++ `struct` or `class` **without** inheritance
- Python class **without** methods (methods are added separately)
```go
type Person struct {
    Name string
    Age  int
}

// Usage
p1 := Person{"Alice", 50}
p2:= Person{Name: "Alice", Age: 50} // idiomatic
p3 := Person{} // zero value initialization
p4 := new(Person) // return Person pointer
```

- Zero values matter a lot in Go:
	- string → `""`
	- int → `0`
	- bool → `false`
	- struct → all fields set to zero-values


### 2. Methods on Structs
In Go, *methods* are added *externally* using **receiver** syntax.
```go
func (p Person) Greet() { // value receiver
    fmt.Println("Hello, my name is", p.Name)
}

func (p *Person) HaveBirthday() { // pointer receiver
    p.Age++
}
```

#### When to use which?
- **Use pointer receiver if:**
	- you want to modify the struct
	- copying is expensive
	- to be consistent across all methods
	- Real-world practice → **95% pointer receivers**.



### 3. Struct Embedding (Composition)
This is Go’s replacement for *OOP* *inheritance*.

```go
type Animal struct {
	Name string
}

type Dog struct { 
Animal // embedded 
Breed string 
}

// Usage

d := Dog{
    Animal: Animal{Name: "Rex"},
    Breed:  "German Shepherd",
}

fmt.Println(d.Name)  // promoted field from Animal
fmt.Println(d.Breed)

```

##### Notice:
`Dog` _automatically gains_ the *fields (and methods)* of `Animal`.



### 4. Methods on Embedded Structs
Go implements *“behavior sharing”* without *inheritance*.

```go 
func (a Animal) Speak() {
	fmt.Println(a.Name, "Make sound!")
}
// Dog automaticlly get method
d.Speak() // promoted method
```


### 5. Interface
*Interfaces* in Go are *extremely* different from *C++* and *Python*:
- **implicit**
- **behavior-only**
- **no need to declare “implements”**

```go
type Speaker interface {
    Speak()
}

func MakeSpeak(s Speaker) {
    s.Speak()
}
```

- Any *type* with a `Speak()` method _automatically_ satisfies this **interface** (like protocol in python)
- And this works even though *Dog* never said *“I implement Speaker”*:
```go 
d := Dog{Animal: {Name: "Rex"}}
d.Speak()
```


### 6.  Empty Interface(interface{})
- Equivalent to Python’s `object` or C++’s `std::any`.
- But using `interface{}` everywhere is **bad practice**; Go prefers *explicit* types.
- *Empty interface* is *built-in* type because of that its declare with `var` not `type`, `type` keyword just use for define *new type*.
```go
var x interface{}
x = 10
x = "hello"
x = Person{"Alex", 20}
```


### 7. Type Assertions
When you have an *interface* and want the *underlying type*:
```go
val, ok := x.(string)
if ok {
    fmt.Println("It's a string:", val)
}
```


### 8. Type Switch
Useful for handle *multiple type*:
```go 
switch v := x.(type) {
	case int:
		fmt.Println("int: ", v)
	case string: 
		fmt.Println("string:", v) 
	case Person: 
		fmt.Println("Person:", v.Name)
	 default: 
		 fmt.Println("unknown type")
}
```


### 9. Interfaces + Structs -> Go's OOP Model
Go avoids deep *inheritance* trees like C++.
Instead:
- define *behavior* using **interfaces**
- *compose* objects using **embedded structs**
It’s simple, predictable, and extremely *maintainable* for applications.



### 10. Practical Example: Designing a small System

```go 
type PaymentMethod interface {
	Pay(amount float64) error
}

type Card struct {
	Name string
}

func (c Card) Pay(amount float64) error {
	fmt.Println("Charging %.2f vai Car account %s\n", amount, c.Name)
	return nil
}

type PayPal struct {
	Email string
}

func (p PayPal) Pay(amount float64) error {
	fmt.Println("Charging %.2f vai PayPal account %s\n", amount, p.Email)
	return nil
}

func Checkout(mehtod PaymentMethod, amount float64) {
	err := method.Pay(amount)
	if err != nil {
		fmt.Println("payment faild:", err)
	}
}


func main() {
	card := Card{Name: "pooya"}
	paypal := PayPal{Email: "pooyasoleymain@gmail.com"}
	
	Checkout(Card, 100)
	Checkout(PayPal, 200)
}
```

##### Result 
Both work because both satisfy the *interface*
