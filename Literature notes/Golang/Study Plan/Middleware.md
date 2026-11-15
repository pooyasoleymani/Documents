---
Created Date: 2026-05-30
tags:
  - golang
  - programming
---
----
# What is Middleware?
**Middleware** is:
> a *function* that *wraps* another *handler*

When we don't want to repeat something:
- *logging*
- *authentication*
- *method checks*
- *request timing*
- *rate limiting*
in every **handler**.
**Middleware** solves this.


```
Request
   ↓
Logging Middleware
   ↓
Authentication Middleware
   ↓
Handler
   ↓
Response
```

# First Middleware

Suppose we want to log every request.

```go
func logging(next http.Handler) http.Handler {
	return http.HandlerFunc(
		func(w http.ResponseWriter, r *http.Request) {
			fmt.Println(
				r.Method,
				r.URL.Path,
			)

			next.ServeHTTP(w, r)
		},
	)
}
```

---

# What is `next`?

```go
next http.Handler
```

represents the *next handler* in the *chain*.

Eventually:

```go
next.ServeHTTP(w, r)
```

calls it.

---

# Using Middleware

Instead of:

```go
http.HandleFunc("/", rootHandler)
```

use:

```go
http.Handle(	"/",	logging(http.HandlerFunc(rootHandler)),)
```

---

# Request Flow
User visits:

```
/
```

*Execution*:

```
logging()   
	↓
rootHandler()
```




# Middleware Can Run Code Before AND After

```go
func logging(next http.Handler) http.Handler {
	return http.HandlerFunc(
		func(w http.ResponseWriter, r *http.Request) {

			fmt.Println("Before")

			next.ServeHTTP(w, r)

			fmt.Println("After")
		},
	)
}
```


# Timing Middleware

```go
func timing(next http.Handler) http.Handler {
	return http.HandlerFunc(
		func(w http.ResponseWriter, r *http.Request) {

			start := time.Now()

			next.ServeHTTP(w, r)

			fmt.Println(
				r.URL.Path,
				time.Since(start),
			)
		},
	)
}
```



# Authentication Middleware

```go
func auth(next http.Handler) http.Handler {
	return http.HandlerFunc(w http.ResponseWrite, r *http.Request) {
		token := r.Header.Get("X-API-Key")
		if token != "secret" {
			http.Error(
				w,
				"Unauthorized",
				http.StatusUnauthorized,
			)
			return
		}
		next.ServeHTTP(w, r)
	}
}
```


# Chaining Middleware

```go
handler :=
	logging(
		timing(
			auth(
				http.HandlerFunc(rootHandler),
			),
		),
	)
```

### Flow
```
Request
 ↓
logging
 ↓
timing
 ↓
auth
 ↓
handler
```


# Cleaner Helper

```go
func chain(
	h http.Handler,
	middlewares ...func(http.Handler) http.Handler,
) http.Handler {

	for i := len(middlewares)-1; i >= 0; i-- {
		h = middlewares[i](h)
	}

	return h
}
```


Usage:
```go
http.Handle(
	"/",
	chain(
		http.HandlerFunc(rootHandler),
		logging,
		timing,
		auth,
	),
)
```


# Panic Recover Middleware

```go
func recoverMiddleware(
	next http.Handler,
) http.Handler {

	return http.HandlerFunc(
		func(
			w http.ResponseWriter,
			r *http.Request,
		) {

			defer func() {
				if err := recover(); err != nil {
					http.Error(
						w,
						"Internal Server Error",
						http.StatusInternalServerError,
					)
				}
			}()

			next.ServeHTTP(w, r)
		},
	)
}
```


