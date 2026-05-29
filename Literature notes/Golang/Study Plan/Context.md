---
Created Date: 2026-05-29
tags:
  - golang
  - programming
---
---
# 🧠 Why `context` exists
Imagine:
- client disconnects
- request times out
- user cancels operation
- server shutting down

How do all goroutines know they should stop?
Before `context`:
- messy custom channels
- hard *coordination*
- *goroutine* leaks
*Go* solved this with:
> **context.Context**



# 🧠 Core Idea
A **context** carries:
- *cancellation signal*
- *timeout/deadline*
- *request-scoped values*
across **goroutines** and *APIs*.


## Important rule
**Context** is  *immutable*
Every modification creates:
- derived *child context*


## Basic Usage

```go
cnx := context.Background()
```

This is root **context**.
Usually used in:
- **main**
- **tests**
- **server startup**


## 🔥 Cancellation Example

```go
package main

import (
	"fmt"
	"context"
	"time"
)

func worker(cnx context.Context) {
	for {
		select {
			case <-ctn.Done():
				fmt.Println("worker done")
				return
				
			default:
				fmt.Println("Working ...")
				time.Sleep(time.Second)
		}
	}
}


func main() {
	cnt, cancel := context.WithCancel(context.Background())
	
	go worker(cnt)
	
	time.Sleep(2 * time.Second)
	
	cancel()
	
	time.Sleep(time.Second)
}
```


Main calls:
```go
cancel()
```
All **listeners** *stop*.




# VERY Important Insight
`Done()` returns:

```go
<-chan struct{}
```

Meaning:
- **context** *cancellation* is **channel-based**
This connects directly to everything you learned earlier.


# 🔥 Timeout Context
VERY common in real systems.

---
# Example

```go
package main
import (
	"context"
	"fmt"
	"time"
	)
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	
	defer cancel()
	
	select {
		case <-time.After(5 * time.Second):
			fmt.Println("finished")
		case <-ctx.Done():
			fmt.Println("timeout:", ctx.Err())	
		}
	}
```

---
# Output

```
timeout: context deadline exceeded
```