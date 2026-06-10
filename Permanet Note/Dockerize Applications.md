---
Created Date: 2026-06-10
tags:
  - docker
---
---
For a Go project, I recommend using:

- **Multi-stage Docker build** (small production image)
- **`.env` file** for configuration
- **Docker Compose** for running your app and dependencies
- **Non-root user** inside the container
- **Health checks**
- **Separate development and production configs**

---

# Example Project Structure

```text
myapp/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
├── .env
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── go.sum
└── config/
    └── config.go
```

---

# Step 1: Configuration

Your Go config:

```go
package config

import "os"

type Config struct {
	DBUser     string
	DBPassword string
	DBHost     string
	DBName     string
	Port       string
}

func Load() *Config {
	return &Config{
		DBUser:     os.Getenv("DB_USER"),
		DBPassword: os.Getenv("DB_PASSWORD"),
		DBHost:     os.Getenv("DB_HOST"),
		DBName:     os.Getenv("DB_NAME"),
		Port:       os.Getenv("PORT"),
	}
}
```

---

# Step 2: .env

```env
PORT=8080

DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=mysql:3306
DB_NAME=mydb
```

### Why?

Instead of hardcoding values:

```go
db, _ := sql.Open(...)
```

you read from environment variables:

```go
cfg := config.Load()
```

This makes the application portable.

---

# Step 3: Dockerfile

A production-ready Dockerfile.

```dockerfile
# Build Stage
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w" \
    -o app \
    ./cmd/server

# Runtime Stage
FROM alpine:latest

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/app .

USER appuser

EXPOSE 8080

CMD ["./app"]
```

---

# What happens here?

### Stage 1

```dockerfile
FROM golang:1.25-alpine AS builder
```

Builds the binary.

---

### Download dependencies

```dockerfile
COPY go.mod go.sum ./
RUN go mod download
```

Docker caches modules.

If code changes but dependencies don't:

```bash
docker build
```

will be much faster.

---

### Build binary

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o app
```

Creates a Linux executable.

---

### Stage 2

```dockerfile
FROM alpine:latest
```

Only contains:

- Linux
    
- Your binary
    

No Go compiler.

Result:

```text
Builder Image  : ~900MB
Runtime Image  : ~20MB
```

---

# Step 4: Docker Compose

Example with MySQL.

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: go-app

    ports:
      - "8080:8080"

    env_file:
      - .env

    depends_on:
      - mysql

    restart: unless-stopped

  mysql:
    image: mysql:8.4

    container_name: mysql-db

    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mydb
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword

    ports:
      - "3306:3306"

    volumes:
      - mysql_data:/var/lib/mysql

    restart: unless-stopped

volumes:
  mysql_data:
```

---

# How networking works

Inside Docker:

```text
app
 |
 +---- mysql
```

Docker creates a network automatically.

Your Go app can connect using:

```env
DB_HOST=mysql:3306
```

not:

```env
DB_HOST=localhost:3306
```

because:

```text
localhost = current container
```

and MySQL is in another container.

---

# Connection String Example

For MySQL:

```go
dsn := fmt.Sprintf(
    "%s:%s@tcp(%s)/%s?parseTime=true",
    cfg.DBUser,
    cfg.DBPassword,
    cfg.DBHost,
    cfg.DBName,
)
```

If compose runs:

```env
DB_HOST=mysql:3306
```

then Go connects automatically.

---

# Step 5: Running

Build and start:

```bash
docker compose up --build
```

Background:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

Remove volumes:

```bash
docker compose down -v
```

---

# Health Check (Recommended)

Add to your app service:

```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://localhost:8080/health"]
  interval: 30s
  timeout: 5s
  retries: 3
```

Then implement:

```go
func Health(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
}
```

---

# Development Dockerfile

For local development you may want hot reload using [Air](https://github.com/air-verse/air?utm_source=chatgpt.com).

```dockerfile
FROM golang:1.25

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go install github.com/air-verse/air@latest

CMD ["air"]
```

Development:

```bash
docker compose up
```

Every file change rebuilds automatically.

---

# Best Practices

### 1. Use .dockerignore

Create:

```text
.git
.idea
.vscode
tmp
vendor
bin
*.log
.env
```

Why?

Without it Docker sends everything to the build context.

---

### 2. Never hardcode secrets

Bad:

```go
password := "123456"
```

Good:

```go
os.Getenv("DB_PASSWORD")
```

---

### 3. Run as non-root

Bad:

```dockerfile
USER root
```

Good:

```dockerfile
USER appuser
```

---

### 4. Use multi-stage builds

Bad:

```dockerfile
FROM golang:1.25
```

Production image may be > 1GB.

Good:

```dockerfile
FROM golang:1.25-alpine AS builder
FROM alpine
```

---

### 5. Add graceful shutdown

```go
ctx, stop := signal.NotifyContext(
    context.Background(),
    os.Interrupt,
    syscall.SIGTERM,
)
defer stop()
```

Docker sends `SIGTERM` when stopping containers.

---

### 6. Don't use localhost between containers

Wrong:

```env
DB_HOST=localhost:3306
```

Correct:

```env
DB_HOST=mysql:3306
```

where `mysql` is the Compose service name.

---

# For your Oracle setup

Since your previous messages showed you're using Oracle (`go-ora` and port `1521`), your `.env` would look more like:

```env
DB_USER=CLIF_SERVER_T2
DB_PASSWORD=CLIF_SERVER_T2

DB_HOST=10.10.10.19
DB_PORT=1521

DB_SERVICE=shpd

PORT=8080
```

and Compose only needs to run your Go application if Oracle is already installed on another server.

```yaml
services:
  app:
    build: .
    env_file:
      - .env
    ports:
      - "8080:8080"
```

In that case the container reaches Oracle through:

```text
10.10.10.19:1521
```

just like your host machine does.

For your project (Go API + Oracle + repository pattern), I would also add:
- `Makefile`
- separate `docker-compose.dev.yml`
- structured configuration loading
- health checks for both HTTP and Oracle connectivity

# Production-Ready Structure

```text
myapp/
├── cmd/
│   └── server/
│       └── main.go
│
├── internal/
│   ├── config/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   ├── middleware/
│   └── model/
│
├── deployments/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env
├── .env.production
├── .dockerignore
├── Makefile
├── go.mod
└── go.sum
```

---

# Docker Build Optimization

Many beginners write:

```dockerfile
COPY . .
RUN go build
```

This causes Docker to rebuild everything whenever a file changes.

Instead:

```dockerfile
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN go build -o server ./cmd/server
```

### Why?

Docker layers:

```text
Layer 1 -> go.mod
Layer 2 -> go.sum
Layer 3 -> go mod download
Layer 4 -> source code
Layer 5 -> build
```

If only source changes:

```text
Layer 1 cached
Layer 2 cached
Layer 3 cached
Layer 4 rebuild
Layer 5 rebuild
```

Much faster.

---

# Distroless Images

Instead of Alpine:

```dockerfile
FROM gcr.io/distroless/static-debian12
```

Advantages:

- Smaller image
    
- No shell
    
- Better security
    
- Less attack surface
    

Example:

```dockerfile
FROM golang:1.25 AS builder

WORKDIR /app

COPY . .

RUN CGO_ENABLED=0 GOOS=linux \
    go build -o server ./cmd/server

FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/server /

ENTRYPOINT ["/server"]
```

Image size:

```text
golang image      ~900 MB
alpine runtime    ~20 MB
distroless        ~10 MB
```

---

# Health Endpoint

Create:

```go
package handler

import "net/http"

func Health(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ok"))
}
```

Register:

```go
mux.HandleFunc("/health", handler.Health)
```

---

# Healthcheck In Compose

```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://localhost:8080/health"]
  interval: 10s
  timeout: 3s
  retries: 3
```

Docker now knows if your application is healthy.

Check:

```bash
docker ps
```

Output:

```text
healthy
```

instead of

```text
starting
```

---

# Graceful Shutdown

Many Go applications lose requests during deployment.

Bad:

```go
http.ListenAndServe(":8080", nil)
```

Better:

```go
srv := &http.Server{
	Addr: ":8080",
	Handler: mux,
}

go func() {
	srv.ListenAndServe()
}()

<-ctx.Done()

srv.Shutdown(context.Background())
```

When Docker sends:

```text
SIGTERM
```

your application finishes current requests.

---

# Environment Configuration

Instead of:

```go
os.Getenv("DB_USER")
os.Getenv("DB_PASSWORD")
os.Getenv("DB_HOST")
```

Create:

```go
type Config struct {
	Port string

	DB struct {
		User string
		Password string
		Host string
		Service string
	}
}
```

Loader:

```go
func Load() *Config {
	return &Config{
		Port: getEnv("PORT", "8080"),
	}
}
```

Helper:

```go
func getEnv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
```

Now your app starts even if variables are missing.

---

# Oracle Example

Since you're using `go-ora`:

```env
DB_USER=CLIF_SERVER_T2
DB_PASSWORD=CLIF_SERVER_T2

DB_HOST=10.10.10.19
DB_PORT=1521

DB_SERVICE=shpd
```

DSN:

```go
dsn := fmt.Sprintf(
    "oracle://%s:%s@%s:%s/%s",
    cfg.DBUser,
    cfg.DBPassword,
    cfg.DBHost,
    cfg.DBPort,
    cfg.DBService,
)
```

---

# Logging Best Practice

Don't use:

```go
log.Println("error")
```

everywhere.

Create:

```go
type Logger struct {
	*log.Logger
}
```

Initialize:

```go
logger := log.New(
	os.Stdout,
	"",
	log.LstdFlags|log.Lshortfile,
)
```

Usage:

```go
logger.Println("database connected")
```

---

# Docker Secrets (Production)

Avoid:

```env
DB_PASSWORD=123456
```

inside Git.

Instead:

```yaml
services:
  app:
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Read:

```go
content, _ := os.ReadFile("/run/secrets/db_password")
password := strings.TrimSpace(string(content))
```

---

# Makefile

Instead of remembering commands:

```makefile
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart
```

Usage:

```bash
make build
make up
make logs
```

---

# Development vs Production

Development:

```yaml
volumes:
  - .:/app
```

Advantages:

- Live code changes
    
- Air hot reload
    

Production:

```yaml
volumes: []
```

Advantages:

- Immutable container
    
- More secure
    
- Faster startup
    

---

# What happens when you run `docker compose up`

```text
1. Read docker-compose.yml

2. Build Dockerfile

3. Create network

4. Create volumes

5. Start containers

6. Inject environment variables

7. Run your Go binary

8. Expose ports
```

Example:

```text
Browser
   │
localhost:8080
   │
Docker Host
   │
Container: app
   │
Oracle Server
10.10.10.19:1521
```

This is the architecture I'd use for your current project:

```text
Client
  │
HTTP API (Go)
  │
Service Layer
  │
Repository Layer
  │
Oracle Database
```

The next logical step is learning **how to debug containers**, **view logs**, **attach a shell**, **inspect networks**, and **troubleshoot database connectivity** because those are the skills you'll use daily when running Go services in Docker.