---
Created Date: 2026-06-02
tags:
  - golang
  - programming
---
---
# Making a Go Module

```bash 
mkdir ch1
cd ch1
go mod init hello_world
```

After that in `ch1` directory create `go.mod` file:
```bash 
cat go.mod

// output
module hello_world

go 1.20
```


# Build Go file
All *Go* programs start from the main **function** in the main package. You declare this function with `func main()` and a left brace. Like Java, JavaScript, and C, Go uses braces to mark the start and end of code blocks.

```go
package main

import "fmt"

func main() {
	fmt.Println("hello world")
}
```

For build Go module or file:
```bash
go build
```

Or:

```bash
go build -o hello_world
```


# go fmt
*Developers* have *historically* wasted extraordinary amounts of time on *format wars*. Since **Go** defines a *standard* way of *formatting code*, Go developers avoid *arguments* over *brace style* and *tabs versus* *spaces*.
For example, **Go** programs use *tabs* to *indent*, and it is a *syntax error* if the opening brace is not on the same line as the declaration or command that begins the block.

>[!IMPORTANT]
>`go fmt`, which *automatically* fixes the *whitespace* in your code to match the standard format. However, it *can’t fix braces* on the *wrong line*.


```go
// ./... it tell go apply command for all the files in current directory
go fmt ./...
```

# go vet

In one class of **bugs**, the code is *syntactically* *valid* but quite *likely incorrect*. The go tool includes a command called go vet to detect these kinds of *errors*.

```go
fmt.Printf("Hello, %s!\n")
```

```bash
go vet ./...
```

Output:
```
# hello_world
./hello.go:6:2: fmt.Printf format %s reads arg #1, but call has 0 args
```


