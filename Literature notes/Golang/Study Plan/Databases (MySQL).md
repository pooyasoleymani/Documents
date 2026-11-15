---
Created Date: 2026-06-06
tags:
  - golang
  - programming
---
---
**This connects directly to your original goal:**
> "create a *model* to *communicate* with *database* and a *web service* to *serialize* data and *send* to other *services*"


# Why move to databases now?
Currently:

```go
type BookStore struct {
	books []Book
}
```

Data lives only in *memory*.

If the server restarts:

```
all books lost
```

A database gives:

```
persistent storage
```


# Architecture we're aiming for

```
HTTP Handler     
↓
Service     
↓
Repository     
↓
MySQL
```

Example:

```
POST /books     
↓
CreateBookHandler     
↓
BookService     
↓
BookRepository     
↓
INSERT INTO books
```


# Lesson 1: database/sql
Go's standard package:

```go
import "database/sql"
```

It doesn't talk to *MySQL* directly.

You also need a *driver*.

For *MySQL*, the common driver is:

```go
import _ "github.com/go-sql-driver/mysql"
```

Notice the blank import (`_`) we discussed earlier.

The driver *registers* itself with `database/sql`.

# Install driver

From your module root:

```go
go get github.com/go-sql-driver/mysql
```


# Open Connection

```go
db, err := sql.Open(
	"mysql",	
	"user:password@tcp(localhost:3306)/booksdb",
)
if err != nil {	
	log.Fatal(err)
}
defer db.Close()
```

Important:

```go
sql.Open()
```

does not *verify* the *connection*.

Always test:
```go
if err := db.Ping();err != nil {
	log.Fatal(err)
}
```


# Create Table

Example SQL:

```sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	author VARCHAR(255) NOT NULL,
	    pages INT NOT NULL
);
```


# Repository Pattern

Instead of:

```go
func createBookHandler(...) {	
	db.Exec(...)
}
```

we **separate storage**.


## Book Model

```go
type Book struct {
	ID     int
	Title  string
	Author string
	Pages  int
}
```

---

## Repository

```go
type BookRepository struct {
	db *sql.DB
}
```


## Constructor

```go
func NewBookRepository(db *sql.DB) *BookRepository {
	return &BookRepository{
		db: db,
	}
}
```


## Insert book
```go
func (r *BookRepository) Create(book Book) error {

	query := `
	INSERT INTO books(title, author, pages)
	VALUES (?, ?, ?)
	`

	_, err := r.db.Exec(
		query,
		book.Title,
		book.Author,
		book.Pages,
	)

	return err
}
```

Notice:

```
?,?,?
```

These are *parameter placeholders*.

Never build *SQL* like:

```go
query := "INSERT ... " + title
```

because of *SQL injection.*


# Why Repository?
Bad:

```
handler    
↓
database
```

Every *handler* knows *SQL*.

---

Good:

```
handler    
↓
repository    
↓
database
```

*Only repository* knows **SQL**.


---
# Start MySQL with Docker

## Step 1: Create container
Run:
```bash
docker run -d \
--name mysql-dev \
-e MYSQL_ROOT_PASWORD=password \
-e MYSQL_DATABASE=booksdb \
- p 3306:3306
  mysql:8
```

Check it;s running:
```bash
docker ps
```

You should see a container named:

```
mysql-dev
```

---

## Step 2: Connect to MySQL

Open a shell inside the container:

```bash
docker exec -it mysql-dev mysql -u root -p
```

Enter:
```
rootpass
```

## Step 3: Verify Database

Inside MySQL:

```sql
SHOW DATABASES;
```

You should see:

```
booksdb
```

Switch to it:

```sql
USE booksdb;
```

---

## Step 4: Create Table

```sql
CREATE TABLE books (    
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	author VARCHAR(255) NOT NULL,    
	pages INT NOT NULL
);
```

Verify:

```sql
SHOW TABLES;
```

and:

```sql
DESCRIBE books;
```

---

## Step 5: Create Go Project Structure
A typical layout:

```
book-api/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── model/
│   │   └── book.go
│   └── repository/
│       └── book.go
├── go.mod
```

## Step 6: Install MySQL Driver

From the module root:

```bash
go get github.com/go-sql-driver/mysql
```


## Step 7: Connect From Go

```go
package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func main() {
	dsn := "root:rootpass@tcp(localhost:3306)/booksdb"

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		panic(err)
	}

	fmt.Println("Connected!")
}
```


Run:
```bash
go run .
```

Expected:
```
Connected!
```

### Correct `GetAll()`

```go
func (r *BookRepository) GetAll() ([]model.Book, error) {

	var books []model.Book

	rows, err := r.db.Query(
		"SELECT id, title, author, pages FROM books",
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {

		var book model.Book

		err := rows.Scan(
			&book.ID,
			&book.Title,
			&book.Author,
			&book.Pages,
		)
		if err != nil {
			return nil, err
		}

		books = append(books, book)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return books, nil
}
```

# Important SQL Methods
You'll use these constantly:

|Method|Purpose|
|---|---|
|`Exec()`|INSERT, UPDATE, DELETE|
|`Query()`|Multiple rows|
|`QueryRow()`|Single row|
|`Scan()`|Read columns into variables|


# Next Repository Method: `GetByID`
Very common pattern.

```go

func (r *BookRepository) GetByID(
	id int,
) (*model.Book, error)

// Implement

func (r *BookRepository) GetByID(
	id int,
) (*model.Book, error) {

	var book model.Book

	err := r.db.QueryRow(
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
		if err == sql.ErrNoRows {
			return nil, err
		}
		return nil, err
	}

	return &book, nil
}
```


# Mini Exercise

Implement:

```go
func (r *BookRepository) Delete(id int) error
```

SQL:

```sql
DELETE FROM booksWHERE id = ?
```

Hint:

```go
result, err := r.db.Exec(...)
```

Then inspect:

```go
rowsAffected, err := result.RowsAffected()
```

If:

```
rowsAffected == 0
```

return an error like:

```go
fmt.Errorf("book not found")
```

This teaches a very common repository pattern.



# Update Method

Signature:

```go
func (r *BookRepository) Update(book model.Book) error
```

---

## SQL

```sql
UPDATE books
SET title = ?, author = ?, pages = ?
WHERE id = ?
```

---

## Implementation

```go
func (r *BookRepository) Update(book model.Book) error {

	result, err := r.db.Exec(
		`UPDATE books
		 SET title = ?, author = ?, pages = ?
		 WHERE id = ?`,
		book.Title,
		book.Author,
		book.Pages,
		book.ID,
	)
	if err != nil {
		return err
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return err
	}

	if rowsAffected == 0 {
		return errors.New("book not found")
	}

	return nil
}
```

---

# CRUD Complete

Your repository now contains:

```go
Create(book)
GetAll()
GetByID(id)
Update(book)
DeleteByID(id)
```

This is the standard CRUD repository you'll build hundreds of times in backend work.

---

# Next Step: Service Layer

Right now:

```text
HTTP Handler
    ↓
Repository
    ↓
Database
```

Works, but business logic ends up in handlers.

Instead:

```text
HTTP Handler
    ↓
Service
    ↓
Repository
    ↓
Database
```

---

## Why?

Imagine a rule:

```text
Pages must be > 0
Title cannot be empty
```

Where should this **live**?

Not in the repository.

Repository should only know **SQL**.

Instead:

```go
type BookService struct {
	repo *repository.BookRepository
}
```

---

## Constructor

```go
func NewBookService(
	repo *repository.BookRepository,
) *BookService {
	return &BookService{
		repo: repo,
	}
}
```

---

## Create Book

```go
func (s *BookService) CreateBook(
	book model.Book,
) error {

	if book.Title == "" {
		return errors.New("title required")
	}

	if book.Author == "" {
		return errors.New("author required")
	}

	if book.Pages <= 0 {
		return errors.New("pages must be positive")
	}

	return s.repo.Create(book)
}
```

Notice:

- validation in service
    
- SQL in repository
    

Clean separation.

---

# Handler Becomes Tiny

Instead of:

```go
func createBookHandler(...) {
	// validate
	// database
	// business rules
	// response
}
```

You get:

```go
func (h *Handler) CreateBook(
	w http.ResponseWriter,
	r *http.Request,
) {
	var book model.Book

	if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := h.service.CreateBook(book); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
}
```

Much cleaner.

---

# Real Project Layout

A common Go backend structure:

```text
book-api/
├── cmd/
│   └── api/
│       └── main.go
│
├── internal/
│   ├── model/
│   │   └── book.go
│   │
│   ├── repository/
│   │   └── book.go
│   │
│   ├── service/
│   │   └── book.go
│   │
│   └── handler/
│       └── book.go
│
└── go.mod
```

Responsibilities:

```text
model      -> structs
repository -> SQL
service    -> business rules
handler    -> HTTP
main       -> wiring
```

---

# Dependency Injection

In `main.go`:

```go
repo := repository.NewBookRepository(db)

service := service.NewBookService(repo)

handler := handler.NewBookHandler(service)
```

Then:

```go
http.HandleFunc("/books", handler.CreateBook)
```

This is how many Go APIs are assembled.

---

# Your Next Exercise

Create:

```text
internal/service/book.go
```

with:

```go
type BookService struct {
	repo *repository.BookRepository
}
```

and implement:

```go
CreateBook(book model.Book) error
GetAllBooks() ([]model.Book, error)
GetBookByID(id int) (*model.Book, error)
DeleteBook(id int) error
UpdateBook(book model.Book) error
```

For now, most methods can simply call the repository. Only `CreateBook` should perform validation.

This introduces the service layer that sits between HTTP and the database, which is the architecture you'll use in most production Go services.