---
Created Date: 2026-05-25
tags:
  - golang
  - programming
---
---
## Hello World

```go
package main

import "fmt"

func main() {
	fnt.Println("Hello GO!")
}
```


1. `package main`: Every **Go** file belongs to a package. 
2. `import "fmt"`: import the standard formatting package.
	1. Python → `import printlib`
	2. C++ → `#include <iostream>`
	- **Go** import *package* not *header files*.
 
 3. `func main ()`: define main function
 
### Important Go Philosophy
**Go** imports *must* be *used* if you *import* something unused *compilation fails*.

---
## Go functions
Syntax:
```go
func functionName(parameters) returnType {
}

func add(a, b int) int {
	return a + b
}
```


## Important Difference from C++
Go avoid *operator overloading*.


## Braces style
The `{` must be on *same line*, This is because **Go** automatically inserts *semicolons*.

```go 
func main() // this wrong
{
}
```

## No Semicolons
**Go** inserts *semicolons* automatically.


## Formatting Philosophy
Go has strict formatting culture.

```bash
go fmt
```


## Third Task — Learn `Printf`
Write:

```go
fmt.Printf("%d\n", 10)
fmt.Printf("%f\n", 3.14)
fmt.Printf("%s\n", "hello")
fmt.Printf("%T\n", 10)
```

>[!NOTE]
> We can reflect type of variable or value with `fmt.Printf("%T\n", variable)`


## Join strings
For join strings we can use **string** package and *Join* function

```go
func main() {
 fmt.Println(strings.Join(os.Args[1:], " ")) 
 }
```
---
### Exercises

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("OS:", runtime.GOOS)
	fmt.Println("ARCH:", runtime.GOARCH)
	fmt.Println("Go Version:", runtime.Version())
}
```
