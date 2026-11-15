---
Created Date: 2026-06-10
tags:
  - golang
  - programming
---
---
# 1. Unit Tests (No Database)

Most common and fastest.

You replace the repository with a fake/mock.

Example:

```go
type BookRepository interface {
	GetByID(ctx context.Context, id int) (*model.Book, error)
}
```

Fake repository:

```go
type FakeBookRepo struct{}

func (f FakeBookRepo) GetByID(
	ctx context.Context,
	id int,
) (*model.Book, error) {
	return &model.Book{
		ID:    id,
		Title: "Test Book",
	}, nil
}
```

Test the service without MySQL running.

Advantages:
- Fast
- Deterministic
- Easy

---

# 2. Integration Tests (Real Database)

This is where you test actual SQL.

For example:

```go
func TestCreateBook(t *testing.T) {
	db := setupTestDB()

	repo := repository.NewBookRepository(db)

	book := model.Book{
		Title: "Go",
		Author: "Alan",
		Pages: 300,
	}

	err := repo.Create(context.Background(), book)
	if err != nil {
		t.Fatal(err)
	}
}
```

This actually inserts into MySQL.

---

# Best Practice: Use Docker

Create a test database:

```yaml
services:
  mysql-test:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: testdb
    ports:
      - "3307:3306"
```

Run:

```bash
docker compose up -d
```

Use:

```go
root:root@tcp(localhost:3307)/testdb
```

for tests.

Never test against production data.

---

# Clean Database Before Each Test

Common pattern:

```go
func cleanDB(db *sql.DB) {
	db.Exec("DELETE FROM books")
}
```

Usage:

```go
func TestCreateBook(t *testing.T) {

	db := setupTestDB()

	cleanDB(db)

	...
}
```

Each test starts fresh.

---

# 3. HTTP Integration Tests

Test the whole stack:

```text
Handler
 ↓
Service
 ↓
Repository
 ↓
MySQL
```

Example:

```go
func TestCreateBookAPI(t *testing.T) {

	body := strings.NewReader(`
	{
		"title":"Go",
		"author":"Alan",
		"pages":300
	}`)

	req := httptest.NewRequest(
		http.MethodPost,
		"/books",
		body,
	)

	rec := httptest.NewRecorder()

	handler.Create(rec, req)

	if rec.Code != http.StatusCreated {
		t.Fatal("expected 201")
	}
}
```

This tests the entire application flow.

---

# Professional Approach

Most companies use:

```text
70% Unit Tests
20% Integration Tests
10% End-to-End Tests
```

Because:
- Unit tests are fast.
- Integration tests verify SQL.
- End-to-end tests are slower and more expensive.

---

# A Very Useful Tool: testcontainers-go

Instead of manually starting Docker:

```bash
docker compose up
```

Go can start a temporary MySQL container automatically.

Project: [testcontainers-go](https://testcontainers.com/guides/getting-started-with-testcontainers-for-go/?utm_source=chatgpt.com)

Example idea:

```go
container := mysql.RunContainer(...)
defer container.Terminate(...)
```

Test starts:

```text
MySQL Container
 ↓
Run Test
 ↓
Destroy Container
```

Very clean for CI/CD.

---

# What I Recommend For You Right Now

Since you're learning:
1. Keep your current repository.
2. Start a MySQL Docker container.
3. Create a separate `testdb`.
4. Write repository tests for:
    - `Create`
    - `GetByID`
    - `GetAll`
    - `Update`
    - `DeleteByID`
5. Before each test:

```go
DELETE FROM books;
```

6. Verify data using real SQL queries.
