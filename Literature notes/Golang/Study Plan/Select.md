---
Created Date: 2026-05-29
tags:
  - golang
  - programming
---
---
# 🧠 What does `select` do?
`select` lets a *goroutine*:
> 1. *wait* on **MULTIPLE channel** operations *simultaneously*
> 2. **select** is Go's traffic *controller* 

```go
select {
	case v := <-ch1:
		fmt.Println(v)
	case ch2 <- x:
		fmt.Println("send")
	default:
		fmt.Println("nothing ready")
}
```


# 🧠 Important Behavior
`select`:
- *waits* until one *case* is ready
- *executes* ONE *ready* *case*
- *ignores* others

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(1 * time.Second)
		ch1 <- "from ch1"
	}()

	go func() {
		time.Sleep(2 * time.Second)
		ch2 <- "from ch2"
	}()

	select {
	case msg := <-ch1:
		fmt.Println(msg)

	case msg := <-ch2:
		fmt.Println(msg)
	}
}
```

# 🧠 What happens?
- `ch1` becomes *ready first*
- select executes *first case*
- *program exits*

# 🧠 If multiple are ready?
Go picks: **pseudo-randomly**
This prevents *starvation*.


# 🔥 Infinite Select Loop
Very common server *pattern*.
### Example

```go
for {
	select {
		case msg := <-messages:
				fmt.Println(msg)
		case err := <-errors:
				fmt.Println(err)	
		}
	}
```

This is real *backend* *architecture* *style*.


# 🔥 `default` Case (VERY important)
`default` makes select: **non-blocking**

```go
package main

import "fmt"

func main() {
	ch := make(chan int)

	select {
	case v := <-ch:
		fmt.Println(v)

	default:
		fmt.Println("no value available")
	}
}
```


# 🧠 Mental Model

|select form|behavior|
|---|---|
|no default|blocking|
|with default|non-blocking|

# 🔥 Timeout Pattern (EXTREMELY IMPORTANT)
Used everywhere in *production* Go.

---
## Example
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch := make(chan string)

	go func() {
		time.Sleep(3 * time.Second)
		ch <- "done"
	}()

	select {
	case msg := <-ch:
		fmt.Println(msg)

	case <-time.After(1 * time.Second):
		fmt.Println("timeout")
	}
}
```

## 🧠 Why `time.After` works
It returns a *channel*:
```
<-chan Time
```

which *sends* value after *duration*.
VERY elegant Go design.


## 🚀 Real-world Usage
Timeouts are CRITICAL for:
- **HTTP requests**
- **DB queries**
- *APIs*
- *distributed systems*


## Multiple channels into one stream

```go
package main

import (
	"fmt"
	"time"
)

func worker(name string, ch chan string) {
	for {
		time.Sleep(time.Second)
		ch <- name
	}
}

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go worker("A", ch1)
	go worker("B", ch2)

	for i := 0; i < 5; i++ {
		select {
		case msg := <-ch1:
			fmt.Println(msg)

		case msg := <-ch2:
			fmt.Println(msg)
		}
	}
}
```

## 🧠 This is huge concept
You merged:
- **multiple concurrent producers**
- **into single consumer flow**

Used in:
- **logging** **systems**
- **event systems**
- `websocket` hubs
- `microservices`


## 🔥 Select + Channels = Go Concurrency Core
Most production *Go concurrency* revolves around:
- *goroutines*
- *channels*
- *select*
This trio is the heart of Go systems programming.