---
Created Date: 2026-06-06
tags:
  - golang
  - programming
---
---
# Configuration Management (Production Style Go)

Right now you likely have something like:

```go
dsn := "root:rootpass@tcp(localhost:3306)/booksdb"
http.ListenAndServe(":8080", nil)
```

This works, but it becomes a problem when you move to:

- staging
- production
- docker
- CI/CD
- cloud environments

Because you would need to change code for every environment.

That is not acceptable in real systems.

---
# Goal

Move all “environment-specific values” out of code.

We want:

```text
CODE  →  CONFIG FILE / ENV VARS
```

---

# Step 1: Environment Variables

Go reads them via:

```go
os.Getenv("KEY")
```

Example:

```go
port := os.Getenv("PORT")
```

---

# Step 2: Create a Config Struct

Instead of random variables everywhere:

```go
type Config struct {
	DBUser     string
	DBPassword string
	DBHost     string
	DBName     string
	Port       string
}
```

---

# Step 3: Load Config

```go
func LoadConfig() Config {
	return Config{
		DBUser:     os.Getenv("DB_USER"),
		DBPassword: os.Getenv("DB_PASSWORD"),
		DBHost:     os.Getenv("DB_HOST"),
		DBName:     os.Getenv("DB_NAME"),
		Port:       os.Getenv("PORT"),
	}
}
```

---

# Step 4: Build DSN safely

Instead of hardcoding:

```go
root:rootpass@tcp(localhost:3306)/booksdb
```

We build it:

```go
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

# Step 5: Use in main.go

```go
func main() {
	cfg := LoadConfig()

	db, err := sql.Open("mysql", cfg.DSN())
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to DB")

	http.ListenAndServe(":"+cfg.Port, nil)
}
```

---

# Step 6: `.env` file (recommended)
Create:

```text
DB_USER=root
DB_PASSWORD=rootpass
DB_HOST=localhost:3306
DB_NAME=booksdb
PORT=8080
```

Then load it using a library:

```bash
go get github.com/joho/godotenv
```

---

# Step 7: Load `.env` automatically

```go
import "github.com/joho/godotenv"

func init() {
	godotenv.Load()
}
```

Now your app works locally without exporting variables manually.

---

# Why this matters
You now can run:

### Local

```text
DB_HOST=localhost
```

### Docker

```text
DB_HOST=mysql-container
```

### Production

```text
DB_HOST=rds.amazonaws.com
```

WITHOUT changing code.

---

# What you just learned (important milestone)

You now understand:

- environment variables    
- configuration struct
- DSN building
- separation of config from code

This is a **real backend architecture skill**, not beginner Go anymore.


