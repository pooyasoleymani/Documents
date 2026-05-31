---
Created Date: 2026-05-31
tags:
  - golang
  - programming
---
---
# ✅ Real Use Case: Why Interfaces Exist
Interfaces are useful when:

> You want to **replace implementation easily**

Examples:
- **database** (Postgres vs Memory)
- **file storage** vs **S3**
- real **API** vs **mock API** (testing)

---
# 💡 Real Scenario: Bank System
We want:
- *real storage* (database)
- *mock storage* (for testing)

---
# Step 1: Define behavior (interface)
In Go, we define it where it is USED:

```go
package account

type Store interface {
	Save(name string, balance int)
	Get(name string) int
}
```

# Step 2: Business logic depends on interface

```go
package account

type Service struct {
	store Store
}

func NewService(s Store) *Service {
	return &Service{store: s}
}

func (s *Service) CreateAccount(name string) {
	s.store.Save(name, 0)
}
```


# Step 3: Real implementation (database)

```go
package storage

import "fmt"

type MemoryStore struct {
	data map[string]int
}

func NewMemoryStore() *MemoryStore {
	return &MemoryStore{
		data: make(map[string]int),
	}
}

func (m *MemoryStore) Save(name string, balance int) {
	m.data[name] = balance
}

func (m *MemoryStore) Get(name string) int {
	return m.data[name]
}
```


# Step 4: Wire everything together (main)

```go
package main

import (
	"fmt"

	"bank/account"
	"bank/storage"
)

func main() {
	store := storage.NewMemoryStore()

	service := account.NewService(store)

	service.CreateAccount("Pooya")

	fmt.Println("done")
}
```


# 🧠 What just happened?
We achieved:

```
Service → depends on interface (Store)
Storage → implements interface
Main → connects them
```

---

# 🔥 Why this is powerful
Now we can replace storage WITHOUT changing *business logic*:

---

## Swap 1: Memory DB

```
storage.NewMemoryStore()
```

---

## Swap 2: File DB

```
storage.NewFileStore()
```

---

## Swap 3: PostgreSQL

```
storage.NewPostgresStore()
```

*Service* code NEVER changes.

---

# 🧪 Testing becomes easy
You can create a fake store:

```go
type FakeStore struct {	
data map[string]int
}
```

Use it in tests:

```go
service := account.NewService(&FakeStore{})
```

No database needed.

---

# 🧠 Golden Rule of Go Interfaces

### ❌ Don’t do this:

Define interfaces “just in case”

### ✅ Do this:

Define interfaces ONLY when you need:

- swapping implementations
- testing isolation
- decoupling systems


# ⚡ Interface in Go = Behavior, not structure

Think:

```
Not WHAT it isBUT what it CAN DO
```

---
# 🧩 Real-world analogy

|Concept|Meaning|
|---|---|
|Interface|“Can Save + Get data”|
|MemoryStore|One implementation|
|PostgresStore|Another implementation|

---

# 🚀 Why Go feels different

In C++/Java:
- you design interfaces first

In Go:
> you write structs first, interfaces appear naturally later

---

# 🧪 Exercise (very important)

Build this:

## Interface:

```go
type Logger interface {
	Log(message string)
}
```

## Implementations:
1. `ConsoleLogger` → prints to terminal
2. `FileLogger` → writes to file

## Service:

```go
type App struct {
	logger Logger
}
```

---

### Goal:
Run **same service** with:
- *console logger*
- *file logger*
**WITHOUT** changing App code.


