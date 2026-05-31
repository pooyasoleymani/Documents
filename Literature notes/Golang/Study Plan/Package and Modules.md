---
Created Date: 2026-05-30
tags:
  - golang
  - programming
---
---
# 1. What is a Package?
A package is:

> a collection of **Go files** in the *same directory*.

```
math/  
├── add.go  
├── subtract.go  
└── multiply.go
```

All files:
```go
package math
```


# Package Names
Convention:

```go
package math
package user
package config
package logger
```

Use:
- short names
- lowercase
- singular when possible

# 2. Exported vs Unexported
You've already seen this with JSON.

---
## Exported
Starts with *uppercase*:

```go
func Add() {}
type User struct {}
```

*Accessible* from *other* packages.

## Unexported
Starts with *lowercase*:

```go
func add() {}
type user struct {}
```

Only accessible *inside* the package.



# Example
### math/add.go

```go
package math
func Add(a, b int) int {
	return a + b
}

func helper() {}
```

### main.go

```go
package main

import "project/math"

func main() {
	math.Add(1, 2)
	math.helper() // compile error
}
```

Because `helper` is private.

---

# 3. What is a Module?
A module is:

> a *versioned* Go *project*

Defined by:
```
go.mod
```

---

# Create One

```bash
go mod init github.com/pooya/bank
```

Creates:
```bash
go.mod
```

Example:
```go
module github.com/pooya/bank

go 1.25
```


# Why Modules Exist
Before modules:

```bash
GOPATH nightmare
```

Modern Go uses modules for:
- *dependency management*
- *versioning*
- *imports*


# Project Structure Example

```
bank/
├── go.mod
├── main.go
├── account/
│   ├── account.go
│   └── account_test.go
└── storage/
    └── file.go
```
