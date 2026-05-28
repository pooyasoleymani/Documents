---
Created Date: 2026-05-28
tags:
  - golang
  - programming
---
---
# What Is a Method?
A method is:
- a *function*
- attached to a *type*

## Normal function

```go
func printUser(user USer) 
```



## Method version
First part before name of *function*  called **receiver**

```go
func (u User) Print() {
	fmt.Println(u.name)
}

// This is method of the User type
user.Print()
```


### VERY Important Idea
Methods improve:
- *organization*
- *readability*
- *discoverability*



## Value Receivers
This method receive copy of the *struct* **(pass by value)** and not effect on *original*
```go
func (u User) Print()
```


## Pointer Receivers
This method *receive* pointer of the *struct* and can modify original struct
```go
func (u *User) ChangeName(name string) {
	u.name = name
}
```


### VERY Important Go Feature
Go automatically *handles*:
- `&`
- `*`
for *method calls*.


### When To Use Pointer Receivers
Use pointer receiver when:
- *method modifies struct*
- *struct large (avoid copying)*
- *shared mutable state desired*

### When Value Receiver Is Fine
Use value receiver when:
- *read-only methods*
- *small immutable-like structs*

### VERY Important Go Convention
If one *method* uses *pointer receiver*,  
usually ALL *methods* should.


### Design Insight
*Methods* attach to:
- *any type*
Even custom **primitive-like types**.

```go
type Counter int

func (c *Counter) Increment() {
	*c++
}
```

