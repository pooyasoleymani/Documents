---
Created Date: 2026-06-06
tags:
  - golang
  - programming
---
---
# Full Go Project Wiring (Real Architecture)

We’ll connect everything properly:

```text
config → db → repository → service → handler → server
```

No globals, no random wiring in handlers.

---

# 1. Final Project Structure

We will organize like this:

```text
book-api/
├── cmd/
│   └── api/
│       └── main.go
│
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── db/
│   │   └── db.go
│   ├── model/
│   │   └── book.go
│   ├── repository/
│   │   └── book.go
│   ├── service/
│   │   └── book.go
│   └── handler/
│       └── book.go
│
├── go.mod
└── .env
```

---

# 2. Config Layer

```go
package config

import (
	"fmt"
	"os"
)

type Config struct {
	DBUser     string
	DBPassword string
	DBHost     string
	DBName     string
	Port       string
}

func Load() Config {
	return Config{
		DBUser:     os.Getenv("DB_USER"),
		DBPassword: os.Getenv("DB_PASSWORD"),
		DBHost:     os.Getenv("DB_HOST"),
		DBName:     os.Getenv("DB_NAME"),
		Port:       os.Getenv("PORT"),
	}
}

func (c Config) DSN() string {
	return fmt.Sprintf(
		"%s:%s@tcp(%s)/%s",
		c.DBUser,
		c.DBPassword,
		c.DBHost,
		c.DBName,
	)
}
```

---

# 3. Database Layer

```go
package db

import (
	"database/sql"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

func New(dsn string) *sql.DB {
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}

	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	return db
}
```

---

# 4. Model

```go
package model

type Book struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
	Pages  int    `json:"pages"`
}
```

---

# 5. Repository

```go
package repository

import (
	"context"
	"database/sql"
	"book-api/internal/model"
)

type BookRepository struct {
	db *sql.DB
}

func NewBookRepository(db *sql.DB) *BookRepository {
	return &BookRepository{db: db}
}
```

(You already implemented CRUD — keep them here with `Context` versions.)

---

# 6. Service Layer

```go
package service

import (
	"context"
	"errors"

	"book-api/internal/model"
	"book-api/internal/repository"
)

type BookService struct {
	repo *repository.BookRepository
}

func NewBookService(repo *repository.BookRepository) *BookService {
	return &BookService{repo: repo}
}

func (s *BookService) Create(ctx context.Context, book model.Book) error {

	if book.Title == "" {
		return errors.New("title required")
	}

	if book.Pages <= 0 {
		return errors.New("pages must be positive")
	}

	return s.repo.Create(ctx, book)
}
```

---

# 7. Handler Layer

```go
package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"book-api/internal/model"
	"book-api/internal/service"
)

type BookHandler struct {
	service *service.BookService
}

func NewBookHandler(s *service.BookService) *BookHandler {
	return &BookHandler{service: s}
}
```

---

## Create Handler

```go
func (h *BookHandler) Create(w http.ResponseWriter, r *http.Request) {

	var book model.Book

	if err := json.NewDecoder(r.Body).Decode(&book); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if err := h.service.Create(r.Context(), book); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
}
```

---

## Get All Handler

```go
func (h *BookHandler) GetAll(w http.ResponseWriter, r *http.Request) {

	books, err := h.service.repo.GetAll(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(books)
}
```

---

# 8. Main (Wiring Everything)

```go
package main

import (
	"net/http"

	"book-api/internal/config"
	"book-api/internal/db"
	"book-api/internal/handler"
	"book-api/internal/repository"
	"book-api/internal/service"

	"github.com/joho/godotenv"
)

func main() {

	godotenv.Load()

	cfg := config.Load()

	database := db.New(cfg.DSN())

	repo := repository.NewBookRepository(database)

	svc := service.NewBookService(repo)

	h := handler.NewBookHandler(svc)

	http.HandleFunc("/books", h.Create)
	http.HandleFunc("/books/all", h.GetAll)

	http.ListenAndServe(":"+cfg.Port, nil)
}
```

---

# What You Just Built
This is now a real backend system:

```text
HTTP → Handler → Service → Repository → MySQL
```

Each layer has ONE responsibility.

---

# Why This Architecture Matters
You now have:

### 1. Replaceable database
Swap MySQL → PostgreSQL easily.

### 2. Testable logic
Service can be tested without HTTP or DB.

### 3. Clean separation
No SQL in handlers.

### 4. Production structure
This is how Go services are built in real companies.
