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

which is how Go APIs are tested professionally.Excellent. Now we move to something used in almost every modern Go API:

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

which is how Go APIs are tested professionally.