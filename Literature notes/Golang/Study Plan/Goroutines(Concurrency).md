---
Created Date: 2026-06-05
tags:
  - golang
  - programming
---
---
# 🧠 What is a goroutine?
A **goroutine** is:
> a *lightweight thread* managed by the *Go runtime*


```go
package main

import (
	"fmt"
	"time"
)

func sayHello() {
	fmt.Println("Hello")
}

func main() {
	go sayHello()

	time.Sleep(time.Second)
	fmt.Println("Main done")
}
```


# 🧠 Go runtime model
Go does NOT use OS threads directly for every **goroutine**.
Instead:
```
many goroutines → few OS threads
```

This is called:
 > **M:N scheduling**
 
 # 🚀 Why goroutines are powerful
Creating threads in other languages:

| Language      | Cost       |
| ------------- | ---------- |
| Java thread   | heavy      |
| C++ thread    | heavy      |
| Python thread | limited    |
| Go goroutine  | very cheap |

# ⚠️ Concurrency ≠ Parallelism

|Concept|Meaning|
|---|---|
|concurrency|multiple tasks in progress|
|parallelism|multiple tasks at same time (CPU cores)|

**Go supports both.**


## Race condition

```go
package main

import (
	"fmt"
	"sync"
)

var counter = 0
var mu sync.Mutex

func increment() {
	for i := 0; i < 1000; i++ {
		mu.Lock()
		counter++
		mu.Unlock()
	}
}

func main() {
	go increment()
	go increment()

	// wait (temporary)
	select {}
}
```


```go
package main

import (
	"fmt"
	"sync"
)

var counter = 0
var mu sync.Mutex

func increment(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < 1000; i++ {
		mu.Lock()
		counter++
		mu.Unlock()
	}
}

func main() {
	var wg sync.WaitGroup

	wg.Add(2)

	go increment(&wg)
	go increment(&wg)

	wg.Wait()

	fmt.Println(counter)
}
```


# 🧠 Mental Model
Think:

|Tool|Purpose|
|---|---|
|goroutine|run task|
|mutex|protect data|
|waitgroup|wait for completion|

---

