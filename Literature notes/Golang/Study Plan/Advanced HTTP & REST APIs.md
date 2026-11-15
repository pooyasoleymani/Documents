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



# Lesson 2: Receiving JSON (POST Requests)
## request
Client sends:

```json
{
	"title": "clean code",
	"author": "robert martin",
	"pages": 464
}
```

Book Struct:
```go
type Book struct {
	Title string `json:"name"`,
	Author string `json:"author"`
	Pages: int `json:"pages"`
}
```

# Reading JSON from Request Body

The body is:

```go
r.Body
```

which is an `io.ReadCloser`.

Instead of manually reading bytes, Go usually does:
```go
var book Book

err := json.NewDecoder(r.Body).Decode(&book)
if err != nil {
	http.Error(
		w,
		"invalid json",
		http.StatusBadRequest,
	)
	return
}
```

because **Decode** needs to *modify* the *struct*.

## Simple POST Handler
```go
func createBookHandler(
	w http.ResponseWriter,
	r *http.Request,
) {
	if r.Method != http.MethodPost {
		http.Error(
			w,
			"method not allowed",
			http.StatusMethodNotAllowed,
		)
		return
	}

	var book Book

	if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
		http.Error(
			w,
			"invalid json",
			http.StatusBadRequest,
		)
		return
	}

	fmt.Printf("%+v\n", book)

	w.Header().Set(
		"Content-Type",
		"application/json",
	)

	json.NewEncoder(w).Encode(
		map[string]string{
			"message": "book received",
		},
	)
}
```


## Testing with curl
```sh
curl -X POST \
-H "Content-Type: application/json" \
-d '{"title":"Clean Code","author":"Robert Martin","pages":464}' \
http://localhost:8080/book
```

Response:

```
{  "message":"book received"}
```

Server output:

```
{Title:Clean Code Author:Robert Martin Pages:464}
```



# Why Decode Directly?

Bad:

```go
body, _ := io.ReadAll(r.Body)
json.Unmarshal(body, &book)
```

Good:

```go
json.NewDecoder(r.Body).Decode(&book)
```

Less memory and more idiomatic.


# Validation
Currently this is accepted:

```json
{  "title":"",  "author":"",  "pages":0}
```

Usually we validate:

```go
if book.Title == "" {	
	http.Error(w,
		"title required",		
		http.StatusBadRequest,	
	)	
	return
}
```

We'll improve validation later.



# Common Beginner Mistake
Wrong:

```go
json.NewDecoder(r.Body).Decode(book)
```

Correct:

```go
json.NewDecoder(r.Body).Decode(&book)
```

Because Decode needs a *pointer*.



# Lesson 3: In-Memory REST API
Instead of returning a hardcoded book, we'll store books in *memory*.

# Step 1: Models

```go
type Book struct {	
	ID     int    `json:"id"`
	Title  string `json:"title"`	
	Author string `json:"author"`	
	Pages  int    `json:"pages"`
}
```

---

# Step 2: Storage
For now, we'll use a slice.

```go
var books []Book
var nextID = 1
```

In production we'd use a database, but this lets us focus on HTTP.

---

# Endpoint 1: POST /books
Request:

```json
{  "title":"Clean Code",  "author":"Robert Martin",  "pages":464}
```

Handler:

```go
func createBook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {		
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)		
		return	
	}	
	var book Book	
	if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
			http.Error(w, "invalid json", http.StatusBadRequest)
				return	
	}	
	book.ID = nextID	
	nextID++	
	books = append(books, book)	
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)	
	json.NewEncoder(w).Encode(book)}
```

---

# Endpoint 2: GET /books
Return all books.

```go
func listBooks(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
	}	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(books)}
```

---

# Testing
Create:

```sh
curl -X POST \-H "Content-Type: application/json" \-d '{"title":"Clean Code","author":"Robert Martin","pages":464}' \http://localhost:8080/books
```

Response:
```sh
{  "id":1,  "title":"Clean Code",  "author":"Robert Martin",  "pages":464}
```

---

Then:

```go
curl http://localhost:8080/books
```

Response:

```sh
[  
	{
    "id":1,    
	"title":"Clean Code",    
	"author":"Robert Martin",    
	"pages":464  
	}
]
```

---

# ⚠️ Problem: Global Variables

This works:

```go
var books []Book
var nextID int
```

but it's not ideal.

As APIs grow, we usually create a struct:

```go
type BookStore struct {	
	books  []Book	
	nextID int
}
```

and attach methods to it.

We'll do that soon.

---

# ⚠️ Another Problem: Concurrency

Suppose two requests arrive simultaneously:

```
Request A -> append bookRequest B -> append book
```

Now multiple goroutines access:

```
books
```

at the same time.
This is a data race.

We'll eventually fix it with:
`sync.Mutex`

---
# Lesson 4: Handler Structs & Dependency Injection
Instead of:
```go 
var book []book
var nexID int
```

Create store:
```go
type Store struct {
	books []Book
	nextId int
}

// Initialize it
store := &BookStore{
	nexID: 1,
}
```

# Why?
Because *handlers* need data.

Instead of:

```go
func createBook(w http.ResponseWriter, r *http.Request)
```

we can do:

```go
func (s *BookStore) createBook(	w http.ResponseWriter,	r *http.Request,)
```

Now the handler has access to:

```go
s.books
s.nextID
```

*without globals*.


## Create book
```go
func (s *BookStore) createBook(
	w http.ResponseWriter,
	r *http.Request,
) {
	if r.Method != http.MethodPost {
		http.Error(
			w,
			"method not allowed",
			http.StatusMethodNotAllowed,
		)
		return
	}

	var book Book

	if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
		http.Error(
			w,
			"invalid json",
			http.StatusBadRequest,
		)
		return
	}

	book.ID = s.nextID
	s.nextID++

	s.books = append(s.books, book)

	w.WriteHeader(http.StatusCreated)

	json.NewEncoder(w).Encode(book)
}
```

## List books
```go
func (s *BookStore) listBooks(
	w http.ResponseWriter,
	r *http.Request,
) {
	json.NewEncoder(w).Encode(s.books)
}
```

## Main 
```go
func main() {
	store := &BookStore{
		nextID: 1,
	}

	http.HandleFunc(
		"/books",
		store.listBooks,
	)

	http.HandleFunc(
		"/books/create",
		store.createBook,
	)

	http.ListenAndServe(":8080", nil)
}
```


# What is Dependency Injection?
You may hear this term often.

Dependency:

```go
BookStore
```

Injection:

```go
store := &BookStore{}
```

passed into *handlers*.

Instead of *handlers* creating their own *store*.


# Why is this better?
Bad:

```go
func createBook(...) {	
	db := connectDatabase()
}
```

Every handler creates its own *dependencies*.


Good:

```go
type Server struct {
	store *BookStore
}
```

Created once:

```go
server := &Server{	store: store,}
```

Then *reused*.



# Real Production Version

Eventually you'll see:

```go
type Server struct {	
	db     *sql.DB	
	logger *log.Logger	
	config Config
}
```

Handlers become:

```go
func (s *Server) createBook(...)
```

This is extremely common in Go services.



# Next Problem: Concurrency
Imagine:

```
Request ARequest BRequest C
```

all hit:

```go
s.books = append(...)
```

simultaneously.
That is *unsafe*.

Multiple *goroutines* can access the slice at the same time.



# Solution: Mutex

Add:

```go
type BookStore struct {
	mu     sync.Mutex	
	books  []Book	
	nextID int
}
```

When modifying:

```go
s.mu.Lock()
defer s.mu.Unlock()
s.books = append(...)
```

Now only one request can modify the slice at a time.

# Exercise
Refactor the API so:

```go
type BookStore struct {	
	mu     sync.Mutex
	books  []Book
	nextID int
}
```

Requirements:

1. Convert handlers to methods.
2. Remove all global variables.
3. Protect writes with `Mutex`.
4. Protect reads too:

```go
s.mu.Lock()
defer s.mu.Unlock()
```

5. Keep:
    - POST `/books`
    - GET `/books`

---

Once you've done that, we'll move to:

### Project Structure for Real APIs

```
cmd/
internal/
handlers/
storage/
models/
```

which connects directly to the project structure questions you were asking earlier.