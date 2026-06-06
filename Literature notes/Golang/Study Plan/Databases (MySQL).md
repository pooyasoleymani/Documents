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
-e MY_ROOT_PASWORD=password \
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