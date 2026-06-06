---
Created Date: 2026-06-06
copilot-command-model-key: true
tags:
  - golang
  - programming
---
---
# Middleware (Real Production Pattern)

Middleware is how you “wrap” **HTTP** handlers.

---

# What is Middleware?

Think of it like this:

```text
Request
  ↓
Logging Middleware
  ↓
Auth Middleware
  ↓
Timeout Middleware
  ↓
Handler
```

Each layer can:
- read request
- modify request
- block request
- log request
- recover from panic

---

# Step 1: Basic Middleware Pattern

In Go, middleware is just a function:

```go
func Middleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// before
		next(w, r)
		// after
	}
}
```

---

# Step 2: Logging Middleware

```go
func Logging(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		start := time.Now()

		fmt.Println("Incoming request:", r.Method, r.URL.Path)

		next(w, r)

		fmt.Println("Completed in:", time.Since(start))
	}
}
```

---

# Step 3: Apply Middleware

Instead of:

```go
http.HandleFunc("/books", h.Create)
```

We wrap it:

```go
http.HandleFunc("/books", Logging(h.Create))
```

Now every request is logged automatically.

---

# Step 4: Auth Middleware (Simple Example)

```go
func Auth(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		token := r.Header.Get("Authorization")

		if token != "secret" {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}

		next(w, r)
	}
}
```

Usage:

```go
http.HandleFunc("/books", Auth(Logging(h.Create)))
```

Order matters:

```text
Auth → Logging → Handler
```

---

# Step 5: Middleware Chain Problem

This becomes hard to read:

```go
Auth(Logging(SomeMiddleware(h.Create)))
```

So we improve it.

---

# Step 6: Middleware Chain Helper

```go
func Chain(
	h http.HandlerFunc,
	middlewares ...func(http.HandlerFunc) http.HandlerFunc,
) http.HandlerFunc {

	for i := len(middlewares) - 1; i >= 0; i-- {
		h = middlewares[i](h)
	}

	return h
}
```

---

# Step 7: Clean Usage

Now you write:

```go
http.HandleFunc(
	"/books",
	Chain(
		h.Create,
		Logging,
		Auth,
	),
)
```

Much cleaner.

---

# Step 8: Real-World Middleware Examples

In production Go services you often have:

### 1. Recovery Middleware

```go
func Recover(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		defer func() {
			if err := recover(); err != nil {
				http.Error(w, "internal error", 500)
			}
		}()

		next(w, r)
	}
}
```

---

### 2. Request ID Middleware

Adds tracking:

```go
r.Header.Set("X-Request-ID", uuid)
```

---

### 3. Timeout Middleware

```go
ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
defer cancel()
```

---

# Step 9: Middleware Order Rule

Very important:

```text
Recover (outermost)
  ↓
Logging
  ↓
Auth
  ↓
Handler
```

Because:

- Recover must catch everything
- Logging should see all requests
- Auth should block early

---

# Exercise
Create these 3 middleware:

### 1. Logger

Print:

```text
METHOD PATH DURATION
```

---

### 2. Auth

Only allow:

```text
Authorization: Bearer token123
```

---

### 3. Chain them together

Apply to:

```text
POST /books
```

---

# Next Step (VERY IMPORTANT)

After middleware, we move to:

## Advanced HTTP Router (Mux)

You will learn:

- path parameters (`/books/{id}`)
    
- routing libraries (`chi`)
    
- real REST structure
    

Then your API will feel like real production services.

---

Say **go next** when ready.