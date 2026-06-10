---
Created Date: 2026-06-06
tags:
  - golang
  - programming
---
---
# Context + Database Queries
So far your repository methods look like:

```go
func (r *BookRepository) GetByID(id int) (*model.Book, error)
```

But in production we usually pass a `context.Context`.

---
# Why?

Suppose a client calls:

```http
GET /books/1
```

Then closes the browser.

Without context:

```text
Request cancelled
       ↓
Database query keeps running
```

Waste of resources.

With context:

```text
Request cancelled
       ↓
Context cancelled
       ↓
Database query cancelled
```

---

# New Repository Signature

Instead of:

```go
func (r *BookRepository) GetByID(id int) (*model.Book, error)
```

Use:

```go
func (r *BookRepository) GetByID(
	ctx context.Context,
	id int,
) (*model.Book, error)
```

---

# QueryRowContext

Instead of:

```go
r.db.QueryRow(...)
```

Use:

```go
r.db.QueryRowContext(
	ctx,
	query,
	args...,
)
```

Example:

```go
func (r *BookRepository) GetByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {

	var book model.Book

	err := r.db.QueryRowContext(
		ctx,
		`SELECT id, title, author, pages
		 FROM books
		 WHERE id = ?`,
		id,
	).Scan(
		&book.ID,
		&book.Title,
		&book.Author,
		&book.Pages,
	)

	if err != nil {
		return nil, err
	}

	return &book, nil
}
```

---

# ExecContext

Instead of:

```go
r.db.Exec(...)
```

Use:

```go
r.db.ExecContext(...)
```

Example:

```go
_, err := r.db.ExecContext(
	ctx,
	query,
	book.Title,
	book.Author,
	book.Pages,
)
```

---

# Query Context

Instead of:

```go
r.db.Query(...)
```

Use:

```go
r.db.QueryContext(...)
```

---

# Handler Passes Context

Every request already has one:

```go
ctx := r.Context()
```

Example:

```go
func (h *BookHandler) GetBook(
	w http.ResponseWriter,
	r *http.Request,
) {
	book, err := h.service.GetBookByID(
		r.Context(),
		1,
	)

	...
}
```

---

# Service Layer

Pass it through:

```go
func (s *BookService) GetBookByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {

	return s.repo.GetByID(ctx, id)
}
```

---

# Rule of Thumb

Whenever a function:

- performs I/O
- accesses DB
- calls HTTP
- calls `gRPC`
- waits for external resources
    
pass a context.

Example:

```go
func FetchUser(
	ctx context.Context,
	id int,
)
```

Good.

---

# What NOT to do

Never store context in a struct.

Bad:

```go
type BookService struct {
	ctx context.Context
}
```

We talked about this earlier.

Context belongs to a request, not to an object.

Pass it as a parameter.

---

# Common Production Signatures

Repository:

```go
Create(ctx context.Context, book Book) error
```

Service:

```go
CreateBook(ctx context.Context, book Book) error
```

HTTP:

```go
func (h *Handler) CreateBook(
	w http.ResponseWriter,
	r *http.Request,
)
```

using:

```go
r.Context()
```

---

# Why This Matters

When you later work with:

- MySQL
- PostgreSQL
- Redis
- Kafka
- RabbitMQ
- External REST APIs

you'll see `context.Context` everywhere.

It's one of the most important conventions in modern Go.
