---
Created Date: 2026-06-17
tags:
  - golang
  - programming
---
---
# Typical CI/CD Flow

When you deploy a new version:

```text
Git Push
   ↓
CI (build + test)
   ↓
Build Docker Image
   ↓
Run Database Migrations
   ↓
Deploy Application
```

Important:

```text
Migration BEFORE application startup
```

because the new application code may expect new columns/tables.

---

# Option 1: Migration Step in Pipeline (Most Common)

Example:

```yaml
Build
Test
Migrate DB
Deploy
```

Pseudo pipeline:

```bash
go test ./...

docker build -t myapp .

migrate up

kubectl apply ...
```

This is the most common approach.

---

# GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run migrations
        run: |
          migrate \
            -path migrations \
            -database "${{ secrets.DB_DSN }}" \
            up

      - name: Deploy
        run: |
          docker build -t myapp .
```

Notice the database password comes from secrets.

Never commit:

```yaml
DB_PASSWORD=rootpass
```

to Git.

---

# Option 2: Migration Container (Docker)

Many teams build a dedicated migration image.

Example:

```dockerfile
FROM migrate/migrate

COPY migrations /migrations
```

Run:

```bash
docker run \
  --network app-network \
  migration-image \
  -path=/migrations \
  -database="$DB_DSN" \
  up
```

Advantages:

- same version everywhere
    
- easy rollback
    
- works well in Kubernetes
    

---

# Option 3: Kubernetes Job (Very Common)

Before deploying:

```yaml
apiVersion: batch/v1
kind: Job
```

Job executes:

```bash
migrate up
```

Then exits.

Flow:

```text
Migration Job
      ↓
Success
      ↓
Deploy New Pods
```

Very common in cloud environments.

---

# What About Running Migrations in main.go?

Many beginners do:

```go
func main() {
	runMigrations()

	startServer()
}
```

I do NOT recommend this for production.

Why?

Imagine:

```text
10 replicas start
```

All try:

```text
ALTER TABLE books ...
```

at the same time.

Potential problems:

- locks
    
- startup failures
    
- deployment race conditions
    

Better:

```text
Migration Step
      ↓
Application Start
```

Separate responsibilities.

---

# Handling Failed Migrations

Suppose:

Migration 12:

```sql
ALTER TABLE books ADD COLUMN price INT;
```

fails.

Pipeline:

```text
Build  ✅
Test   ✅
Migration ❌
Deploy skipped
```

This is good.

You never deploy incompatible code.

---

# Rollbacks

Suppose migration 15 is bad.

Rollback:

```bash
migrate down 1
```

or

```bash
migrate goto 14
```

depending on tooling/version.

Then redeploy previous app version.

---

# My Recommendation for Your Learning Project

Since you're using:
- Go
- Docker
- MySQL

Create:

```text
docker-compose.yml
```

with:

```text
app
mysql
```

Then create a simple `Taskfile`.

Example:

```yaml
version: "3"

tasks:
  migrate-up:
    cmds:
      - migrate -path migrations -database "$DB_DSN" up

  migrate-down:
    cmds:
      - migrate -path migrations -database "$DB_DSN" down 1

  run:
    cmds:
      - go run ./cmd/api
```

You were already learning `Taskfile`, so this fits nicely into your workflow.

---

# Production Rule

A good deployment pipeline is:

```text
1. Build
2. Unit Tests
3. Integration Tests
4. Migration
5. Deploy
6. Health Check
```

If any step fails:

```text
STOP DEPLOYMENT
```
