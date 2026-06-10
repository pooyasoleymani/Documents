---
Created Date: 2026-06-10
tags:
  - golang
  - programming
---
---
Perfect. Now we arrive at the topic where interfaces stop being academic and become genuinely useful.

# Interfaces + Dependency Injection + Mocking

Remember when you asked:

> "is Account interface really needed?"

For this:

```go
type BankAccount struct {}
```

the answer was mostly **no**.

But in backend applications, interfaces become very valuable.

---

# The Problem

Suppose your service looks like:

```go
type BookService struct {
	repo *repository.BookRepository
}
```

And:

```go
func (s *BookService) GetBookByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {

	return s.repo.GetByID(ctx, id)
}
```

Looks fine.

---

# Testing Problem

To test the service:

```go
repo := repository.NewBookRepository(db)
```

You now need:

- MySQL
    
- Docker
    
- schema
    
- test data
    

for every service test.

That's annoying.

---

# Introduce an Interface

Define what the service needs:

```go
type BookRepository interface {
	GetByID(
		ctx context.Context,
		id int,
	) (*model.Book, error)

	Create(
		ctx context.Context,
		book model.Book,
	) error
}
```

Notice:

```text
interface = behavior
```

not implementation.

---

# Service Depends on Interface

```go
type BookService struct {
	repo BookRepository
}
```

Constructor:

```go
func NewBookService(
	repo BookRepository,
) *BookService {

	return &BookService{
		repo: repo,
	}
}
```

Now the service doesn't care whether the repository is:

```text
MySQL
PostgreSQL
Mock
Fake
```

---

# Real Repository

Your real repository already satisfies it:

```go
type BookRepository struct {
	db *sql.DB
}
```

Because it has:

```go
GetByID(...)
Create(...)
```

Go interfaces are satisfied automatically.

No:

```go
implements
extends
```

needed.

---

# Fake Repository

For tests:

```go
type FakeBookRepo struct{}
```

Implement methods:

```go
func (f FakeBookRepo) GetByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {

	return &model.Book{
		ID: id,
		Title: "Test Book",
	}, nil
}
```

---

# Testing Service

```go
func TestGetBook(t *testing.T) {

	repo := FakeBookRepo{}

	service := NewBookService(repo)

	book, err := service.GetBookByID(
		context.Background(),
		1,
	)

	if err != nil {
		t.Fatal(err)
	}

	if book.Title != "Test Book" {
		t.Fatal("wrong title")
	}
}
```

No database.

No Docker.

Runs instantly.

---

# Fake Error Repository

You can test failures too.

```go
type ErrorBookRepo struct{}
```

```go
func (e ErrorBookRepo) GetByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {

	return nil, errors.New("db failure")
}
```

Test:

```go
func TestGetBook_DBError(
	t *testing.T,
) {

	repo := ErrorBookRepo{}

	service := NewBookService(repo)

	_, err := service.GetBookByID(
		context.Background(),
		1,
	)

	if err == nil {
		t.Fatal("expected error")
	}
}
```

---

# Why Dependency Injection?

Instead of:

```go
service := &BookService{
	repo: repository.NewBookRepository(db),
}
```

inside the service,

we inject dependencies:

```go
repo := repository.NewBookRepository(db)

service := NewBookService(repo)
```

Benefits:

- easier testing
    
- looser coupling
    
- easier replacement
    

---

# Common Go Rule

Define interfaces where they are consumed.

Bad:

```go
repository/
  repository.go

type Repository interface {}
```

Good:

```go
service/
  book.go

type BookRepository interface {}
```

The service defines what it needs.

---

# When NOT to Use Interfaces

Don't do this:

```go
type UserService interface {
	CreateUser(...)
}
```

when there is only one implementation and no testing need.

A lot of beginners create interfaces everywhere.

That adds complexity.

---

# Real Rule

Use interfaces when:

✅ multiple implementations

```text
MySQL
PostgreSQL
Redis
```

or

✅ testing/mocking

```text
RealRepo
FakeRepo
```

Avoid them when there is only one implementation and no benefit.

