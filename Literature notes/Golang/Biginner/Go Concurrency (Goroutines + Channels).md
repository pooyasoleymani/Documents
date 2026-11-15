---
Created Date: 2026-05-12
tags:
  - golang
  - programming
---
---

### 1. Goroutine: lightweight `thread`
A **goroutine** is started with the `go` keyword.
```go
package main

import (
	"fmt"
	"time"
)

func work(id int) {
	for i:=0; i<10;i++ {
		fmt.Println("worker %d: %d", id, i)
		time.Sleep(100 * time.Millisecond)
	}
	
func main() {

	go work(1)
	go work(2)
	
	time.Sleep(500 * time.Millisecond)
}
}
```

#### Key points

- `go f()` starts `f` *concurrently*.
- *Goroutines* are much lighter than *OS threads*.
- You **must coordinate** if you need results (don’t rely on `Sleep` in real code).



### Channels: safe communication between between goroutines
A **channel** lets goroutines exchange values *safely*.

#### Create Channel
```go
ch := make(chan int)
```

- `chan int` means “channel carrying `int`”
- `make(chan int)` creates it

#### Send/Receive
```go
ch <- 10   // send 10
x := <-ch  // receive into x
```

This is **blocking**:
- *send* blocks until someone *receives* (unless *buffered* channel)
- *receive* blocks until someone *sends* (unless *buffered* channel)



### 3) The simplest producer/consumer
```go 
package main
import "fmt"

func producer(ch chan<- int) {
	ch <- 42
}

func main() { 
	ch := make(chan int) 
	go producer(ch) 
	v := <-ch 
	fmt.Println(v) 
}

```

#### Why `chan<- int`?
It documents intent:
- `producer` only *sends*
- `main` only *receives*

Similarly, you can use:
- `ch <-chan int` for *receive-only*


### 4) Buffered channels (avoid some blocking)
```go
ch := make(chan int, 3) // capcity is 3
```
- We can send up to 3 values without an *immediate* *receiver*
- after if fill send block again

#### What does “block” mean?
- The goroutine **pauses** at that line.
- It cannot continue running.
- It *sleeps* inside the Go *scheduler*.
- It stays there **until another goroutine receives from the channel**.
- After a *receive* occurs, the blocked *goroutine* **wakes** up and *continues*.
```go
ch := make(chan int, 2)

go func() {
    fmt.Println("sending 1")
    ch <- 1

    fmt.Println("sending 2")
    ch <- 2

    fmt.Println("sending 3 (will block)")
    ch <- 3    // <-- blocks until someone receives
    fmt.Println("sent 3") 
}()

time.Sleep(1 * time.Second)

fmt.Println("receiving...")
fmt.Println(<-ch)
fmt.Println(<-ch)
fmt.Println(<-ch) // receive third value
```



### 5) Coordinating goroutines: don’t use `Sleep`
Use *channels* (or `sync.WaitGroup`) to know when work is done.

```go 
package main
import "fmt"

func worker(done chan <- struct{}, id int) {
	fmt.Println("worker", id, "starting")
	// do work
	fmt.Println("worker", id, "finished")
}


func main() {
 done := make(chan struct{}, 2)
 
 go worker(done, 1)
 go worker(done, 2)
 
 <-done
 <-done
 fmt.Println("all workers finished")
}
```

#### Why `struct{}` ?
- Because its a *zero-size* type
- It  carry no data , just a *signal*



### 6) Common deadlock patterns to watch for
#### Deadlock #1: receive before send
```go 
ch := make(chan int)
x := <-ch // block forever
```

#### Deadlock #2: send with no receiver (unbuffered)
```go
ch := make(chan int)
ch <- 1 // blocks until someone receives
```