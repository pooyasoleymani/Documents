---
Created Date: 2026-06-14
tags:
  - golang
  - programming
---
---
# Problem Without Transactions

Imagine a bank transfer.

```text
Pooya: 1000
Amir: 500
```

Transfer:

```text
Pooya -> Amir : 100
```

Code:

```go
repo.Withdraw(pooya, 100)
repo.Deposit(amir, 100)
```

What happens if:

```text
Withdraw succeeds
Deposit fails
```

Result:

```text
Pooya: 900
Amir: 500
```

💥 Money disappeared.

---

# Transaction Solution

A transaction makes multiple operations behave as one unit.

```text
All succeed
OR
All fail
```

Properties are known as ACID:

- Atomicity    
- Consistency
- Isolation
- Durability

For now, remember:

```text
Commit = save changes
Rollback = undo changes
```

---

# Starting a Transaction

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
	return err
}
```

Now use `tx`, not `db`.

---

# Commit

```go
err = tx.Commit()
if err != nil {
	return err
}
```

Changes become permanent.

---

# Rollback

```go
err = tx.Rollback()
if err != nil {
	return err
}
```

Everything is undone.

---

# Common Pattern

```go
func Transfer(
	ctx context.Context,
	db *sql.DB,
) error {

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}

	defer tx.Rollback()

	_, err = tx.ExecContext(
		ctx,
		"UPDATE accounts SET balance = balance - 100 WHERE id = 1",
	)
	if err != nil {
		return err
	}

	_, err = tx.ExecContext(
		ctx,
		"UPDATE accounts SET balance = balance + 100 WHERE id = 2",
	)
	if err != nil {
		return err
	}

	return tx.Commit()
}
```

---

# Why defer Rollback?

This confuses many Go developers.

```go
defer tx.Rollback()
```

Even if:

```go
tx.Commit()
```

succeeds, the later rollback is harmless because the transaction is already finished.

This guarantees cleanup on every error path.

---

# Repository Problem

Many beginners write:

```go
repo.Withdraw(...)
repo.Deposit(...)
```

Each method uses:

```go
r.db.Exec(...)
```

Those are separate operations.

No transaction protection.

---

# Better Architecture

Repository:

```go
type AccountRepository struct {
	db *sql.DB
}
```

Service:

```go
func (s *AccountService) Transfer(
	ctx context.Context,
	from int,
	to int,
	amount int,
) error
```

Transaction lives in the service because the service coordinates multiple repository operations.

---

# Transaction-Aware Repository

Instead of:

```go
func (r *Repo) Create(
	ctx context.Context,
	book Book,
) error
```

Use:

```go
func (r *Repo) Create(
	ctx context.Context,
	execer Execer,
	book Book,
) error
```

where:

```go
type Execer interface {
	ExecContext(
		context.Context,
		string,
		...any,
	) (sql.Result, error)
}
```

Both:

```go
*sql.DB
*sql.Tx
```

satisfy this interface.

Then the same repository method can run:

```go
repo.Create(ctx, db, book)
```

or

```go
repo.Create(ctx, tx, book)
```

---

# Example: Create Book + Audit Log

Suppose you have:

```sql
books
audit_logs
```

When creating a book:

```text
Insert book
Insert audit log
```

Both should succeed together.

Service:

```go
tx, err := db.BeginTx(ctx, nil)
```

Repository:

```go
bookRepo.Create(ctx, tx, book)

auditRepo.Create(ctx, tx, log)
```

Then:

```go
tx.Commit()
```

---

# Transaction Mistake #1

Using `db` inside a transaction:

Wrong:

```go
tx, _ := db.BeginTx(...)

repo.Create(ctx, db, book)
```

You just bypassed the transaction.

Must use:

```go
repo.Create(ctx, tx, book)
```

---

# Transaction Mistake #2

Long Transactions

Bad:

```go
tx.Begin()

call external API
sleep 5 seconds
send email

tx.Commit()
```

This keeps locks open and hurts performance.

Transactions should be short.

---

# Transaction Mistake #3

Starting Transactions in Repositories

Usually avoid:

```go
func (r *Repo) CreateBookAndLog(...) {
	tx := db.BeginTx(...)
}
```

Repositories should focus on data access.

Services usually own business workflows and transactions.

---

# Exercise

Create these tables:

```sql
CREATE TABLE books (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255)
);

CREATE TABLE audit_logs (
	id INT AUTO_INCREMENT PRIMARY KEY,
	message VARCHAR(255)
);
```

Implement:

```go
func (s *BookService) CreateBook(
	ctx context.Context,
	book Book,
) error
```

Requirements:

1. Begin transaction.
    
2. Insert book.
    
3. Insert audit log:
    

```text
book created: <title>
```

4. Commit.
    

If either insert fails:

```text
Rollback
```

This is your first real-world transaction workflow.