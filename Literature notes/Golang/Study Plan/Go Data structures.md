---
Created Date: 2026-05-25
tags:
  - golang
  - programming
---
---
## Finding Duplicate Lines
You will learn:
- maps
- scanners
- reading `stdin`
- file processing
- error handling
- `make`
- counting patterns


---
## Maps in Go
Like` unordered_map` in C++.
Order is *Random*.
```go
map[keyType]valueType
//
map[string]int // map string to value
// 
make(map[string]int) // create empty map
```

- If key not exist in **map** we haven't *exception* like python and *undefined behavior* in C++
```go
counts["hello"] // --> 0
```

### Why is powerful
Because you can do this *WITHOUT* checking *existence* first.:
```go
counts[word]++
```


### Count word frequencies using:
- `strings.Fields`
- **map**


## `bufio.Scanner` 
This is your first real *streaming input* tool in Go.
```go
input := bufio.NewScanner(os.Sdtin)
```

## What is `Scanner`
A `Scanner` reads data piece-by-piece.
- line by line 
- word by word

## Why is this important?
Because real programs often process:
- files
- logs
- terminal input
- network streams
**WITHOUT** loading everything into *memory*.


## Understanding `os.Stdin`
This is standard input stream 
- keyboard input
- piped file
- terminal stream

```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	input := bufio.NewScanner(os.Stdin)
	for input.Scan() {
	fmt.Println("Input: ", input.Text())
	}
}
```

### 1. `scanner.Scan()`
Read *next line*, `Scan()` *moves* the scanner *forward*, Like an **iterator**.
- Return `true` if line exist 
- Return `false` if input ends

### 2. `scanner.Text()`
Return current line as **string**
-  **EOF** with (Linux -> *CTRL+D*, Windows -> *CTRL+Z* )

## Important Design
**Scanner** *processes* input **STREAMING**. 
This means:
- *memory efficient*
- *scalable*
- good for *large files*


### 3. `strings.TrimSpace()`
Remove:
- spaces
- tabs
- newline


## VERY Important Engineering Lesson
Real-world *input* is *messy*.
Good programs sanitize input:
- *trim spaces*
- *normalize case*
- *validate format*

#### Error handling in scanner
```go
if err := scanner.Err(); err != nil {  
fmt.Fprintln(os.Stderr, err)  
}
```


## Function Naming in Go
In Go, *exported/public functions* start with *uppercase*.
*internal/private functions* start with *lowercase*.


#### Example:

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	counter := make(map[string]int)
	scanner := bufio.NewScanner(os.Stdin)
	
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		counter[strings.ToLower(line)]++
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprint(os.Stderr, err)
		}
	PrintMap(counter)
}

func PrintMap(m map[string]int) {
	for key, value := range m {
		fmt.Println(key, "=>", value)
}
}
```