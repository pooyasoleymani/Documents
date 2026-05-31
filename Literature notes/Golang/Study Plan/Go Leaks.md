---
Created Date: 2026-05-31
tags:
  - golang
  - programming
---
---
# 1. Goroutine Leaks (Most Common)
A goroutine is not automatically garbage collected while it's still running or blocked.

```go
func worker(ch <-chan int) {
	for {
		x := <-ch
		fmt.Println(x)
	}
}

func main() {
	ch := make(chan int)

	go worker(ch)

	time.Sleep(time.Hour)
}
```

## Fix
Provide a cancellation mechanism:
```go
func worker(ctx context.Context, ch <-chan int) {
	for {
		select {
		case x := <-ch:
			fmt.Println(x)

		case <-ctx.Done():
			return
	}
}
```


# 2. Unfinished Channel Operations

```go
func main() {
	ch := make(chan int)

	go func() {
		ch <- 42
	}()

	return
}
```

The **sender** may *block forever* because *nobody receives*.
A blocked goroutine stays *alive*.


# 3. Forgetting to Close Files
Example:
```go
file, err := os.Open("data.txt")
if err != nil {
	return
}
// forgot file.Close()
```

`GC` eventually *frees memory*, but:

```
file descriptor
socket
OS resource
```

remains **open**.

Enough leaks:
```
too many open files
```

---

## Correct

```go
file, err := os.Open("data.txt")
if err != nil {	
	return
}
defer file.Close()
```

---

# 4. HTTP Response Body Leaks
Very common.

Bad:
```go
resp, err := http.Get(url)
if err != nil {	
return
}
data, _ := io.ReadAll(resp.Body)
// forgot Close()
```

---

Correct:

```go
resp, err := http.Get(url)
if err != nil {	
return
}
defer resp.Body.Close()
```

Otherwise connections remain allocated.

---

# 5. Huge Slice Retention

Example:
```go
data := make([]byte, 100_000_000)
small := data[:10]
```

You think:
```
small = 10 bytes
```

But actually:
```
small points to 100 MB backing array
```

So **100 MB** cannot be **collected**.

---

Fix:
```go
smallCopy := append([]byte(nil), small...)
```

Now only 10 bytes remain.

---
# 6. Maps That Grow Forever

Example:
```go
var cache = map[string]string{}
```

Server:
```go
cache[userID] = value
```

but never *removes* entries.

After months:
```
millions of entries
gigabytes of memory
```

---
# 7. Timers and Tickers

Bad:
```go
ticker := time.NewTicker(time.Second)
for range ticker.C {
	// work
}
```

If you exit without:
```go
ticker.Stop()
```

**resources remain active.**

---

Correct:
```go
ticker := time.NewTicker(time.Second)
defer ticker.Stop()
```

---
# 8. Context Misuse
This is related to your earlier question.

Bad:
```go
type Service struct {
	ctx context.Context
}
```

Now the **context** may *live* much longer than intended.
*Request-specific objects* become retained.

---
Correct:
```go
func (s *Service) Process(ctx context.Context)
```

Pass context, don't store it.

---
# 9. Database Connection Leaks

Bad:
```go
rows, err := db.Query(...)
if err != nil {
	return
}
// forgot rows.Close()
```

Connections stay occupied.

Eventually:
```
database connection pool exhausted
```

---

Correct:
```go
rows, err := db.Query(...)
if err != nil {
	return
}
defer rows.Close()
```

---
# 10. Infinite Background Goroutines

Bad:

```go
go func() {	
	for {		
	doWork()		
	time.Sleep(time.Second)	
	}
}()
```

No **stop condition**.

When the service **shuts down**, the *goroutine* keeps running until process exit.

---

Better:

```go
go func() {	
	for {		
		select {		
		case <-ctx.Done():			
			return		
		case <-time.After(time.Second):			
			doWork()		
		}	
	}
}()
```

---
# Production Go Rule
Whenever you create one of these:

```go
go ...o
s.Open(...)
http.Get(...)
db.Query(...)
time.NewTicker(...)
```

immediately ask:

> **How does this stop?**