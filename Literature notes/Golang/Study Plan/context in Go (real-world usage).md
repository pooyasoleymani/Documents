---
Created Date: 2026-05-31
tags:
  - golang
  - programming
---
---
# 💡 What is `context`?
`context.Context` is used to:

> carry **deadlines**, **cancellation** **signals**, and **request-scoped values** across *API* boundaries

Think:
```
request lifecycle manager
```

# 🔥 Why context exists
In real systems:
- HTTP requests can be slow
- DB queries can hang
- goroutines may outlive requests
So we need a way to say:

```
STOP THIS WORK NOW
```

---

# 📦 Basic example

```go
ctx := context.Background()
```

This is the *root context*.

---
# ⏱ Context with timeout

```go
ctx, cancel := context.WithTimeout(	context.Background(),	2*time.Second,)
defer cancel()
```

Now:
> *context automatically cancels after 2 seconds*


# 🧪 Example: Simulated slow task

```go
func slowTask(ctx context.Context) {
	select {	
	case <-time.After(5 * time.Second):
		fmt.Println("done work")	
	case <-ctx.Done():		
		fmt.Println("cancelled:", ctx.Err())	
	}
}
```

---
# 🚀 Usage

```go
func main() {	
	ctx, cancel := context.WithTimeout(		
		context.Background(),		
		2*time.Second,	
	)	
	defer cancel()	
	
	slowTask(ctx)}
```

Output:

```
cancelled: context deadline exceeded
```

---
# 🧠 How context works internally

```go
ctx.Done() → channel
```

When **context** is *cancelled*:
- *channel closes*
- *all listeners react immediately*

# 🔗 Context propagation
Real Go systems pass context everywhere:

```go
func handler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()	
	doWork(ctx)
}
```

```go
func handler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	select {
	case <-time.After(3 * time.Second):
		fmt.Fprintln(w, "done")
	case <-ctx.Done():
		http.Error(w, "timeout", http.StatusRequestTimeout)
	}
}
```