---
Created Date: 2026-05-25
tags:
  - golang
  - programming
Next: "[[Test-Driven Development (TDD)]]"
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
Go inserts semicolons automatically.