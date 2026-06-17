---
Created Date: 2026-06-17
tags:
  - golang
  - programming
---
---
# Database Migrations (Production-Grade Schema Management)

Right now you are probably doing this manually:

```sql
CREATE TABLE books (...)
```

That works only at the beginning. But in real systems you will need to:

- change tables over time
- add/remove columns
- deploy safely across environments
- rollback changes

Doing this manually is dangerous.

---

# Problem Without Migrations

Imagine production has:

```text
books table (version 1)
```

You update code and add:

```text
ALTER TABLE books ADD COLUMN price INT;
```

Now:

- your laptop works
- staging works
- production crashes (if not applied)

This is chaos without migration tracking.

---

# What Migrations Solve

Migrations give you:

```text
1. versioned SQL changes
2. repeatable deployments
3. rollback support
4. team consistency
```

---

# Common Migration Tools in Go

Most popular:

- golang-migrate (standard choice)
- goose
- atlas (modern)

We’ll use:

👉 [golang-migrate](https://github.com/golang-migrate/migrate?utm_source=chatgpt.com)

---

# Step 1: Install CLI

```bash
go install -tags 'mysql' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
```

Check:

```bash
migrate -version
```

---

# Step 2: Create Migration Folder

```text
migrations/
```

---

# Step 3: Create First Migration

```bash
migrate create -ext sql -dir migrations -seq create_books
```

This generates:

```text
000001_create_books.up.sql
000001_create_books.down.sql
```

---

# Step 4: Write UP migration

```sql
-- 000001_create_books.up.sql

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    pages INT NOT NULL
);
```

---

# Step 5: Write DOWN migration

Rollback:

```sql
-- 000001_create_books.down.sql

DROP TABLE books;
```

---

# Step 6: Run Migrations

Run against MySQL Docker:

```bash
migrate -path ./migrations \
-database "mysql://root:rootpass@tcp(localhost:3306)/booksdb" up
```

Now table is created automatically.

---

# Step 7: Add New Change (Example)

Later you want to add price:

```bash
migrate create -ext sql -dir migrations -seq add_price_to_books
```

---

UP:

```sql
ALTER TABLE books ADD COLUMN price INT;
```

DOWN:

```sql
ALTER TABLE books DROP COLUMN price;
```

---

# Why This Is Important

Now your workflow becomes:

```text
code change
   ↓
new migration file
   ↓
run migrate up
   ↓
deploy safely
```

No manual SQL in production.

---

# How Migration Fits Into Your Architecture

```text
main
 ├── config
 ├── db
 ├── migrations  ← NEW
 ├── repository
 ├── service
 └── handler
```

---

# Production Best Practice

Never:

```text
run migrations manually on production
```

Instead:

- CI/CD runs migrations automatically
    
- or deployment scripts run `migrate up`
    

---

# Common Mistakes

### ❌ Editing old migration files

Never change:

```text
000001_create_books.up.sql
```

Once released → treat as immutable.

---

### ❌ No down migrations

If something breaks:

```text
you cannot rollback schema
```

Always create `.down.sql`

---

### ❌ Mixing schema and data logic in code

Bad:

```go
db.Exec("CREATE TABLE ...")
```

Good:

```text
migrations only
```
