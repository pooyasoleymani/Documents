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


# Importing Local Packages
Suppose:

```
bank/
├── go.mod
├── main.go
└── account/    
	└── account.go
```

---

### account/account.go

```go
package account

type Account struct {
	Name string
}
```

---

### main.go

```go
package main

import (	
	"fmt"	
	"github.com/pooya/bank/account"
)

func main() {	
	a := account.Account{
			Name: "Pooya",
	}	
	fmt.Println(a.Name)
}
```

# Important Rule
Import path comes from:

```
module name + folder path
```

Example:

```go
module github.com/pooya/bank
```

and:
```
account/
```

becomes:
```go
import "github.com/pooya/bank/account"
```



# 4. Package Initialization
You already saw:

```go
func init() {	...}
```

---

Go executes:
1. **package variables**
2. *init()*
3. *main()*

---

Example

```go
package main

import "fmt"

var x = setup()

func setup() int {
	fmt.Println("setup")
	return 42
}

func init() {
	fmt.Println("init")
}

func main() {
	fmt.Println("main")
}
```

Output:

```
setup
init
main
```


# 5. Aliased Imports
Sometimes names conflict.

---
Example

```go
import (
	m "github.com/pooya/bank/math"
)
```

Use:
```go
m.Add(1, 2)
```


# Blank Imports
The purpose is:
> *Execute* the **package's** `init()` *functions* without directly using any *exported* *names* from the package.
> - Loads the package
> - Initializes package variables
> - Runs all `init()` functions


You've already used:
```go
import _ "fmt"
```

Actually that import is *useless*, but **blank imports** have a real purpose.

Example:
```go
import _ "github.com/lib/pq"
```

Import *only* for *package initialization*.
Common with *database drivers*.


# 6. `go mod tidy`
One of the most important commands.

Run:
```bash
go mod tidy
```

It:
- removes *unused dependencies*
- downloads *missing dependencies*
- *cleans* `go.mod`
You'll run this constantly.


# 7. Package Design Rule
Prefer:
```
user/
order/
storage/
config/
```

over:
```
utils/
helpers/
common/
misc/
```

Why?
Because package names should describe **what they contain**, not that they are "**shared**."


# Real Project Layout (Small Application)

```
bank/
├── go.mod
├── cmd/
│   └── bank/
│       └── main.go
├── account/
│   ├── account.go
│   └── account_test.go
├── storage/
│   └── memory.go
└── api/
    └── handler.go
```

