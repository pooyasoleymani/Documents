---
Created Date: 2026-05-29
tags:
  - golang
  - programming
---
---
# Channels
If **goroutines** are “**workers**”, then:
> **channels** are the **pipes** between *workers*

A **channel** is:
> a *typed queue* that *goroutines* can **send/receive** *values* through

# 🧠 Why channels exist
Before channels, we had:
- *shared memory*
- *mutex*
- *race conditions*
Go introduces a different idea:
>  **“Do not share memory — communicate instead”**


## Basic Syntax

```go
ch := make(chan int)

// Sending data
ch <- 42

// Receiving data
value := <-ch
```

### Example

```go
package main

import "fmt"

func main() {
	ch := make(chan int)
	
	go func() {
		ch <- 42
	}()
	
	value := <-ch
	
	fmt.Println(value)
}
```


## ⚠️ IMPORTANT BEHAVIOR
This line:

```
ch <- 42
```

will **BLOCK** until someone **receives**.


## 🧠 Channels are synchronous by default
Meaning:

| action  | behavior |
| ------- | -------- |
| send    | waits    |
| receive | waits    |

---

## 🔥 Buffered Channels
You can create buffer:

```go
ch := make(chan int, 2)
```

Now:
- can store 2 *values* without *blocking*

```go
package main

import "fmt"

func main() {
	ch := make(chan int, 2)

	ch <- 1
	ch <- 2

	fmt.Println(<-ch)
	fmt.Println(<-ch)
}
```


## 🧠 Buffered vs Unbuffered

| Type       | Behavior             |
| ---------- | -------------------- |
| unbuffered | sync handshake       |
| buffered   | async up to capacity |

---

## Real Example

```go
package main

import "fmt"

func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		results <- j * 2
	}
}

func main() {
	jobs := make(chan int, 5)
	results := make(chan int, 5)

	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}

	for j := 1; j <= 5; j++ {
		jobs <- j
	}
	close(jobs)

	for i := 1; i <= 5; i++ {
		fmt.Println(<-results)
	}
}
```

## Channel Direction
```go
jobs <-chan int       // receive only
results chan<- int    // send only
```


## Closing channels

```go
close(jobs)
```

Means:
> no more *values* will be *sent*


## 🔥 Range over channels

```go
for j := range jobs {
	fmt.Println(j)
}
```

Stops automatically when **channel** closes.


## 🧠 VERY Important Rule
Only *sender* should close *channel*.


## 🔥 Channel Blocking Behavior
If nobody receives:

```go
ch <- 10 // blocks forever
```


## 🧠 This is why Go concurrency is powerful
It naturally *synchronizes*:
- no *locks* needed in many cases
- no *shared memory* confusion


## 🔥 Channel vs Mutex

| Feature       | Mutex     | Channel          |
| ------------- | --------- | ---------------- |
| shared state  | yes       | no               |
| communication | no        | yes              |
| design style  | low-level | high-level       |
| complexity    | medium    | easier (usually) |


## 🧠 Mental Model

```
goroutine = execution
channel = coordination
```


## 🔥 Timeline view
Imagine time:

```
T1: goroutine A sends 1
T2: goroutine B receives 1
T3: goroutine A sends 2
T4: goroutine B receives 2
...
T10: goroutine A closes channel
T11: goroutine B finishes loop
```

**They overlap continuously.**