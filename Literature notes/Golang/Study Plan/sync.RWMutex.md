---
Created Date: 2026-06-04
tags:
  - golang
  - programming
---
---
# Problem With Mutex
So far you've used:

```go
var mu sync.Mutex
```

which allows:

```
1 goroutine inside
everyone else waits
```


Imagine:

```
100 GET /books requests
1 POST /books request
```

With:

```go
mu.Lock()
defer mu.Unlock()
```

every request **waits**.

Even readers wait for other readers.

```
Reader 1   
↓
Reader 2 waits   
↓
Reader 3 waits   
↓
Writer waits
```

Very inefficient.

---

# `RWMutex`

Go provides:

```go
var mu sync.RWMutex
```

`RW` = **Read/Write**

---

## Read Lock
For **reads**:

```go
mu.RLock()
defer mu.RUnlock()
```

Many **goroutines** may hold a read **lock simultaneously**.

Example:

```
Reader A  ✓
Reader B  ✓
Reader C  ✓
```

All run together.

---

## Write Lock
For writes:

```go
mu.Lock()
defer mu.Unlock()
```

Only one writer.

Example:

```
Writer A ✓
Writer B waits
Readers wait
```

---

# Visual

Using `Mutex`:

```
GET
GET
GET
POST
all serialized
```

Using `RWMutex`:

```
GET GET GET GET GET       
		||       
		||      
		POST
```


# Your BookStore

Instead of:

```go
type BookStore struct {
	Mu     sync.Mutex	
	books  []Book	
	NextID int
}
```

Use:

```go
type BookStore struct {
	Mu     sync.RWMutex
	books  []Book
	NextID int
}
```

**Readers** run concurrently.
Writer still gets **exclusive access**.



# GET Handler
*Read-only* operation:

```go
s.Mu.RLock()
defer s.Mu.RUnlock()

json.NewEncoder(w).Encode(s.books)
```

---

# POST Handler
Modifies state:

```go
s.Mu.Lock()
defer s.Mu.Unlock()

s.books = append(s.books, book)
```

---
# Rule of Thumb
Use:
```go
RLock()
```

when:
- reading **maps**
- reading **slices**
- reading **counters**
- reading **caches**


Use:
```go
Lock()
```

when:
- **append**
- **delete**
- **update**
- **increment**

---
# Common Bug

Wrong:
```go
s.Mu.RLock()
defer s.Mu.RUnlock()

s.books = append(s.books, book)
```

You are **writing** while holding a **read lock**.
**That is a bug.**

Always:

```go
Lock()
```

for **writes**.