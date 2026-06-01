---
Created Date: 2026-06-01
tags:
  - golang
  - programming
---
---
# Lesson 1: JSON Encoding
Suppose we have:

```go
type User struct {	
	Name string	
	Age  int
}
```

Create a value:

```go
u := User{	Name: "Pooya",	Age:  30,}
```

Convert to JSON:

```go
data, err := json.Marshal(u)
if err != nil {
	fmt.Println(err)	
	return
}
fmt.Println(string(data))
```

Output:

```sh
{"Name":"Pooya","Age":30}
```

# JSON Tags
Normally API responses use lowercase field names.

```go
type User struct {	
	Name string `json:"name"`	
	Age  int    `json:"age"`
}
```

Now:

```sh
{"name":"Pooya","age":30}
```

---
# Ignore Fields

```go
type User struct {
	Name     string `json:"name"`	
	Password string `json:"-"`
}
```

Output:

```sh
{  "name": "Pooya"}
```

Password is *omitted*.
Very common in APIs.

# JSON Decoding
Suppose client sends:

```go
{  "name": "Pooya",  "age": 30}
```

Decode:

```go
var u Usererr := json.Unmarshal(data, &u)
if err != nil {	
	return
}
```

Notice:

```go
&u
```

We pass a *pointer* because **JSON** must modify the *struct*.

---
# JSON in HTTP Handlers

Instead of:

```go
fmt.Fprintln(w, "Hello")
```

we return **JSON**.

Example:

```go
func userHandler(w http.ResponseWriter,	r *http.Request,) {	
	user := User{		
		Name: "Pooya",		
		Age:  30,	
	}	
	w.Header().Set(
	"Content-Type",		
	"application/json",	
	)	
	json.NewEncoder(w).Encode(user)}
```

Response:

```go
{  "name":"Pooya",  "age":30}
```

---

# Why Encoder Instead of Marshal?
You could do:

```go
data, _ := json.Marshal(user)
w.Write(data)
```

But:

```go
json.NewEncoder(w).Encode(user)
```

is:
- *simpler*
- streams directly to *response*
- common *Go style*
