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


## 🧠 What happened?
**Timeout automatically triggered:**
- *cancellation*
- *shutdown signal*





# 🔥 Deadline Context
Instead of *duration*:

```go
context.WithDeadline(...)
```
Uses **exact time**.


# 🔥 Context Values
You can store *request-scoped data*.

```go 
ctx := context.WithValue(context.Background(), "userID", 42)

id := ctx.Value("userID")
```

## ⚠️ IMPORTANT WARNING

Use values ONLY for:
- *request metadata*
- *tracing IDs*
- *auth info*
**NOT** general *parameter* *passing*.



## 🚨 Common Go Rule
Never store:
- *database connections*
- *config structs*
- *huge objects*
inside **context**.


## 🔥 Real HTTP Example
This is how real servers work.

```go
func handler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	select {
	case <-time.After(5 * time.Second):
		fmt.Println("finished")

	case <-ctx.Done():
		fmt.Println("client disconnected")
	}
}
```


## 🚨 Common Beginner Mistakes
### ❌ storing context in struct
Bad:

```go
type App struct {
	ctx context.Context
}
```

Why?
	-  Because **context** represents of specific *operation/request*  NOT *lifetime* of object.


### The Official Recommendation
The Go team recommends:

```go
func DoSomething(ctx context.Context, ...)
```

**Example:** Each request gets its own *context*

```go
func handler(w http.ResponseWriter, r *http.Request) {  
ctx := r.Context()  
  
service.Process(ctx)  
}
```



# Contexts Are Short-Lived

A **context** often lives for:

```
HTTP request
Database query
Background task
CLI command
```

Maybe:
- *milliseconds*
- *seconds*
- *minutes*

A *struct* may live for:
- hours
- days
- entire program lifetime

These lifetimes don't match.