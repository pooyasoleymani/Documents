---
Created Date: 2026-06-01
tags:
  - golang
  - programming
---
---
# 🔥 Goroutine Leaks
Most Go production incidents involving concurrency are **not data races**.

They're:

```
goroutines that never exit
```

---

# What is a goroutine leak?
Suppose:
```go 
func worker(ch <-chan int) {
	for {
		job := <-ch
		fmt.Println(jon)
	}
}
```

Start it:
```go
go worker(ch)
```

Now imagine:

```
main exits
or
nobody sends jobs anymore
```

Worker is stuck forever:

```
waiting on channel receive
```

That **goroutine** can *never* finish.


# Why is this bad?
A goroutine contains:
- *stack*
- *scheduler metadata*
- *references to objects*

One leak:
```
tiny
```

100,000 leaks:
```
huge memory usage
scheduler slowdown
possible OOM
```

# Leak Example #1

```go
func main() {
	ch := make(chan int)	
	go func() {		
		for {			
			fmt.Println(<-ch)		
		}	
	}()
		
	time.Sleep(time.Hour)
}
```

Nobody sends.
*Worker blocks forever*.
Leak.


# Leak Example #2
This one is VERY common:

```go
func fetch() <-chan string {
	ch := make(chan string)	
	go func() {
		ch <- "hello"
	}()	
	return ch
}
```

Caller:
```go
fetch()
```

and ignores the *channel*.
What happens?

```
goroutine   
↓
trying to send   
↓
nobody receives   
↓
blocked forever
```

Leak.

# Solution: Context
Instead of:

```go
func worker(jobs <-chan int)
```

write:
```go
func worker(ctx context.Context,	jobs <-chan int)
```

---

# Context-Aware Worker

```go
func worker(
	ctx context.Context,
	jobs <-chan int,
) {
	for {		
	select {		
	case job, ok := <-jobs:			
		if !ok {
			return			
		}			
		fmt.Println(job)
	case <-ctx.Done():
		return		
		}	
	}
}
```

Now **worker** can **stop**.


# Why `ctx.Done()`?
Remember:

```go
ctx.Done()
```
returns a **channel**.

When **context** is *cancelled*:

```
channel closes
```

All *listeners* wake up.



# Example

```go
ctx, cancel := context.WithCancel(	
context.Background(),
)

go worker(ctx, jobs)

cancel()
```


Immediately:

```
ctx.Done()
fires
↓
worker exits
```


# Pipeline Leak Example
Suppose:

```
Producer   
↓
Worker   
↓
Consumer
```

*Consumer exits early*.

But worker keeps *sending*:

```go
results <- value
```

**Nobody** *receives* anymore.
Worker *blocks forever*.
**Leak**.

# Fix With Context
Worker:

```go
select {
	case results <- value:
		// do something
	case <-ctx.Done():
		return
}
```

Now worker won't get stuck.


# Production Pattern

Most mature Go code looks like:

```go
func Run(	ctx context.Context,) error
```

Examples:

```go
func Process(ctx context.Context)
func Fetch(ctx context.Context)
func Save(ctx context.Context)
func Handle(ctx context.Context)
```


# Why Context Matters
Imagine HTTP request:

```
Client   
↓
HTTP Handler   
↓
Service   
↓
Database
```

User closes browser.


Without context:
```
database still working
service still working
goroutines still alive
```

With *context*:
```
browser closes
↓
request context cancelled
↓
everything stops
```


# Real HTTP Example

```go
func handler(w http.ResponseWriter,	r *http.Request,) {
	ctx := r.Context()	
	result, err := queryDB(ctx)	
	if err != nil {		
		return	
	}	
	fmt.Fprintln(w, result)
}
```

---

# Common Mistake
Bad:

```go
go func() {	
	for {		
		doWork()
	}
}()
```

*No stop condition*.
*No cancellation*.
*Potential leak*.


Better:
```go
go func() {
	for {
		select {

		case <-ctx.Done():
			return

		default:
			doWork()
		}
	}
}()
```


# Another Common Mistake
Creating contexts and never cancelling:

```go
ctx, cancel := context.WithTimeout(...)
```

and forgetting:

```go
cancel()
```

Always:

```go
defer cancel()
```

*unless ownership is transferred*.


# Production Rule

Whenever you see:

```
go ...
```

ask:

> How does this goroutine stop?

If you can't answer immediately, there is a good chance of a leak.

---

# Concurrency Checklist
Before merging code, ask:

### Goroutines

```
How do they exit?
```

### Channels

```
Who closes them?
```

### Contexts

```
Who cancels them?
```

### WaitGroups

```
Can Wait() block forever?
```

