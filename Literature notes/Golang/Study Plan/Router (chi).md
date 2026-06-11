---
Created Date: 2026-06-06
tags:
  - golang
  - programming
---
---
# Router (`chi`)

So far you've used:

```go
http.HandleFunc("/books", handler.Books)
```

This works, but becomes painful when you need:

```text
GET    /books
GET    /books/1
POST   /books
PUT    /books/1
DELETE /books/1
```

The standard library doesn't have path parameters built-in.

---

# Why Routers Exist

Without a router:

```go
id := r.URL.Query().Get("id")
```

Request:

```text
GET /books?id=1
```

With a router:

```text
GET /books/1
```

Much cleaner REST API.

---

# Install Chi

```bash
go get github.com/go-chi/chi/v5
```

---

# Basic Router

```go
package main

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

func main() {

	r := chi.NewRouter()

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("hello"))
	})

	http.ListenAndServe(":8080", r)
}
```

Notice:

```go
r.Get(...)
```

instead of:

```go
http.HandleFunc(...)
```

---

# Path Parameters

Route:

```go
r.Get("/books/{id}", getBook)
```

Request:

```text
GET /books/15
```

Extract parameter:

```go
id := chi.URLParam(r, "id")
```

Example:

```go
func getBook(w http.ResponseWriter, r *http.Request) {

	id := chi.URLParam(r, "id")

	w.Write([]byte("book id: " + id))
}
```

Response:

```text
book id: 15
```

---

# REST Style Routes

Instead of:

```text
GET    /books?id=1
DELETE /books?id=1
```

Use:

```text
GET    /books/1
DELETE /books/1
```

---

# Route Groups

```go
r.Route("/books", func(r chi.Router) {

	r.Get("/", handler.GetAll)

	r.Post("/", handler.Create)

	r.Get("/{id}", handler.GetByID)

	r.Put("/{id}", handler.Update)

	r.Delete("/{id}", handler.Delete)
})
```

Much cleaner.

---

# Middleware with Chi

Instead of wrapping manually:

```go
Auth(Logging(handler))
```

You can register globally:

```go
r.Use(middleware.Logging)
r.Use(middleware.Recovery)
r.Use(middleware.Auth)
```

Every route gets them automatically.

---

# Route-Specific Middleware

Example:

Public route:

```go
r.Get("/health", healthHandler)
```

Protected routes:

```go
r.Group(func(r chi.Router) {

	r.Use(Auth)

	r.Get("/books", getBooks)

	r.Post("/books", createBook)
})
```

---

# URL Parameter Conversion

Remember:

```go
idStr := chi.URLParam(r, "id")
```

returns:

```go
string
```

Convert:

```go
id, err := strconv.Atoi(idStr)
if err != nil {
	http.Error(w, "invalid id", http.StatusBadRequest)
	return
}
```

---

# Example Delete Handler

```go
func (h *BookHandler) Delete(
	w http.ResponseWriter,
	r *http.Request,
) {

	idStr := chi.URLParam(r, "id")

	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(
			w,
			"invalid id",
			http.StatusBadRequest,
		)
		return
	}

	err = h.service.DeleteBook(
		r.Context(),
		id,
	)
	if err != nil {
		http.Error(
			w,
			err.Error(),
			http.StatusNotFound,
		)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}
```

---

# Why Chi Is Popular

Advantages:

✅ Small

✅ Fast

✅ Standard library compatible

✅ Excellent middleware support

✅ Widely used in Go companies

---

# New Project Main

```go
r := chi.NewRouter()

r.Use(middleware.Recovery)
r.Use(middleware.Logging)

r.Route("/books", func(r chi.Router) {

	r.Get("/", h.GetAll)

	r.Get("/{id}", h.GetByID)

	r.Post("/", h.Create)

	r.Put("/{id}", h.Update)

	r.Delete("/{id}", h.Delete)
})

http.ListenAndServe(":8080", r)
```

This starts to look like a professional Go service.

---

# Your Exercise

Convert your current book API to use `chi`:

Routes:

```text
GET    /books
GET    /books/{id}
POST   /books
PUT    /books/{id}
DELETE /books/{id}
```

Update your handlers to use:

```go
chi.URLParam(r, "id")
```

instead of:

```go
r.URL.Query().Get("id")
```

After you finish, we'll move to the next major topic:

# Testing HTTP Handlers

using:

```go
net/http/httptest
```


You've already written unit tests like:

```go
func TestMax(t *testing.T)
```

Now we'll test HTTP handlers.

---

# Why Test Handlers?

Suppose you have:

```go
func HealthHandler(
	w http.ResponseWriter,
	r *http.Request,
) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}
```

How do we verify:

- status code?
    
- response body?
    
- headers?
    

Without starting a real server?

Go provides:

```go
net/http/httptest
```

---

# Basic Handler Test

Handler:

```go
func HealthHandler(
	w http.ResponseWriter,
	r *http.Request,
) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}
```

Test:

```go
func TestHealthHandler(
	t *testing.T,
) {

	req := httptest.NewRequest(
		http.MethodGet,
		"/health",
		nil,
	)

	rec := httptest.NewRecorder()

	HealthHandler(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf(
			"expected %d got %d",
			http.StatusOK,
			rec.Code,
		)
	}
}
```

---

# What's Happening?

## Fake Request

```go
req := httptest.NewRequest(...)
```

Creates:

```text
GET /health
```

without a real network.

---

## Fake Response Writer

```go
rec := httptest.NewRecorder()
```

Captures everything written by the handler.

Think:

```text
Browser
```

but in memory.

---

## Call Handler

```go
HealthHandler(rec, req)
```

Exactly what the HTTP server would do.

---

# Testing Response Body

Handler:

```go
func HealthHandler(
	w http.ResponseWriter,
	r *http.Request,
) {
	w.Write([]byte("OK"))
}
```

Test:

```go
body := rec.Body.String()

if body != "OK" {
	t.Errorf(
		"expected OK got %s",
		body,
	)
}
```

---

# Testing JSON Responses

Handler:

```go
func BookHandler(
	w http.ResponseWriter,
	r *http.Request,
) {

	book := Book{
		ID: 1,
		Title: "Go",
	}

	json.NewEncoder(w).Encode(book)
}
```

Test:

```go
var book Book

err := json.Unmarshal(
	rec.Body.Bytes(),
	&book,
)
if err != nil {
	t.Fatal(err)
}
```

Verify:

```go
if book.ID != 1 {
	t.Error("wrong id")
}
```

---

# Testing POST Requests

Request body:

```go
body := strings.NewReader(
	`{
		"title":"Go",
		"author":"Alan"
	}`,
)
```

Create request:

```go
req := httptest.NewRequest(
	http.MethodPost,
	"/books",
	body,
)
```

Set JSON header:

```go
req.Header.Set(
	"Content-Type",
	"application/json",
)
```

---

# Testing Middleware

Suppose:

```go
handler := Auth(CreateBook)
```

Request without token:

```go
req := httptest.NewRequest(
	http.MethodPost,
	"/books",
	nil,
)
```

Verify:

```go
if rec.Code != http.StatusUnauthorized {
	t.Error("expected 401")
}
```

---

# Table-Driven Handler Tests

Very common in Go.

Example:

```go
tests := []struct {
	method string
	want   int
}{
	{
		method: http.MethodGet,
		want:   http.StatusOK,
	},
	{
		method: http.MethodPost,
		want:   http.StatusMethodNotAllowed,
	},
}
```

Run:

```go
for _, tc := range tests {

	req := httptest.NewRequest(
		tc.method,
		"/health",
		nil,
	)

	rec := httptest.NewRecorder()

	HealthHandler(rec, req)

	if rec.Code != tc.want {
		t.Errorf(...)
	}
}
```

This pattern is everywhere in Go projects.

---

# Testing Repository?

Not yet.

Repository testing usually requires:

- Docker MySQL
    
- test database
    
- fixtures
    

We'll learn that later.

For now:

```text
Handler tests
Service tests
```

give the biggest value.

