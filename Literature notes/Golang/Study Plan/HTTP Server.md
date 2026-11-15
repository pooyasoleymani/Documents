---
Created Date: 2026-05-30
tags:
  - golang
  - programming
---
---
# Why HTTP?

A huge percentage of Go code in industry is:
- REST APIs
- Microservices
- Backend services
- Internal tools
- Webhooks

Go's standard library includes a full HTTP server.


```go 
func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello, Go")
}

func main() {
	http.HandleFunc("/hello, helloHandler)
	fmt.Println("Server running on: 8080")
	
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println(err)
	}
}
```

# Understanding the Handler

```go
func hello(	w http.ResponseWriter,	r *http.Request,)
```

This is the most important HTTP function signature in Go.

---

## ResponseWriter

```go
w http.ResponseWriter
```

Used to send data back.

Example:

```go
fmt.Fprintln(w, "hello")
```

---

## Request

```go
r *http.Request
```

Contains:
- URL
- Headers
- Body
- Method
- Context

Example:

```go
fmt.Println(r.Method)fmt.Println(r.URL.Path)
```

---

# Reading Query Parameters
Request:

```
http://localhost:8080/hello?name=pooya
```

Handler:

```go
func hello(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")	
	fmt.Fprintf(w, "Hello %s\n", name)
}
```

Response:

```
Hello pooya
```

---

# Routing Multiple Endpoints

```go
http.HandleFunc("/", home)
http.HandleFunc("/users", users)
http.HandleFunc("/health", health)
```

Each path gets a handler.

---

# HTTP Methods
You should inspect:

```go
r.Method
```

Example:

```go
if r.Method != http.MethodGet {	
	http.Error(	
		w,
		"Method Not Allowed",		
		http.StatusMethodNotAllowed,	
		)	
		return
	}
```

---

# Returning JSON

Very common.

```go
package main

import (
	"encoding/json"
	"net/http"
)

type User struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func userHandler(
	w http.ResponseWriter,
	r *http.Request,
) {
	user := User{
		Name: "Pooya",
		Age:  25,
	}

	w.Header().Set(
		"Content-Type",
		"application/json",
	)

	json.NewEncoder(w).Encode(user)
}
```

Response:

```
{  "name": "Pooya",  "age": 25}
```

---

# Reading JSON Request Body

Request:

```
{  "name": "Ali",  "age": 30}
```

Handler:

```go
var user User
err := json.NewDecoder(	r.Body,).Decode(&user)
if err != nil {	
	http.Error(		
		w,		
		"invalid json",		
		http.StatusBadRequest,	
		)	
		return
}
```

Notice:

```
&user
```

We decode into a struct.



# Middleware Concept
Suppose you want *logging*.
Instead of putting *logging* everywhere:

```go
func logging(
	next http.Handler,
) http.Handler {

	return http.HandlerFunc(
		func(
			w http.ResponseWriter,
			r *http.Request,
		) {
			fmt.Println(
				r.Method,
				r.URL.Path,
			)

			next.ServeHTTP(w, r)
		},
	)
}
```
