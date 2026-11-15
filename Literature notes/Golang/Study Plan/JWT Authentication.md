---
Created Date: 2026-07-27
tags:
  - golang
  - programming
---
---
# What Problem Does JWT Solve?

Without authentication:

```text
POST /books
DELETE /books/1
```

Anyone can call your API.

We need to know:

```text
Who is the user?
Are they logged in?
```

---

# Traditional Session Authentication

Old web applications:

```text
Login
  ↓
Server creates session
  ↓
Session stored in DB/Redis
  ↓
Cookie sent to browser
```

Works well, but requires server-side session storage.

---

# JWT Authentication

JWT = JSON Web Token

Flow:

```text
Login
  ↓
Server verifies username/password
  ↓
Server generates JWT
  ↓
Client stores JWT
  ↓
Client sends JWT on every request
```

Example request:

```http
Authorization: Bearer eyJhbGciOi...
```

---

# JWT Structure

A JWT has three parts:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example:

```text
eyJhbGciOiJIUzI1NiJ9
.
eyJ1c2VyX2lkIjoxfQ
.
abc123signature
```

You normally don't parse this manually.

---

# Install JWT Library

A popular library is:

[golang-jwt/jwt](https://github.com/golang-jwt/jwt?utm_source=chatgpt.com)

Install:

```bash
go get github.com/golang-jwt/jwt/v5
```

---

# Creating a Token

Example:

```go
func GenerateToken(userID int) (string, error) {

	token := jwt.NewWithClaims(
		jwt.SigningMethodHS256,
		jwt.MapClaims{
			"user_id": userID,
			"exp":     time.Now().Add(24 * time.Hour).Unix(),
		},
	)

	return token.SignedString(
		[]byte("super-secret-key"),
	)
}
```

---

# Login Handler

Imagine:

```json
{
  "username": "pooya",
  "password": "1234"
}
```

After verifying credentials:

```go
token, err := GenerateToken(user.ID)
```

Return:

```json
{
  "token": "eyJhbGc..."
}
```

---

# Validating Tokens

Middleware:

```go
func Auth(next http.HandlerFunc) http.HandlerFunc {

	return func(
		w http.ResponseWriter,
		r *http.Request,
	) {

		tokenString := strings.TrimPrefix(
			r.Header.Get("Authorization"),
			"Bearer ",
		)

		token, err := jwt.Parse(
			tokenString,
			func(token *jwt.Token) (any, error) {
				return []byte("super-secret-key"), nil
			},
		)

		if err != nil || !token.Valid {
			http.Error(
				w,
				"unauthorized",
				http.StatusUnauthorized,
			)
			return
		}

		next(w, r)
	}
}
```

---

# Extracting User ID

After validation:

```go
claims := token.Claims.(jwt.MapClaims)

userID := int(
	claims["user_id"].(float64),
)
```

Now you know who made the request.

---

# Store User ID in Context

Instead of reparsing later:

```go
ctx := context.WithValue(
	r.Context(),
	"user_id",
	userID,
)

next(w, r.WithContext(ctx))
```

Handler:

```go
userID := r.Context().Value("user_id")
```

---

# Better Context Keys

Avoid:

```go
"user_id"
```

Use:

```go
type contextKey string

const UserIDKey contextKey = "user_id"
```

Prevents collisions.

---

# Token Expiration

JWTs should expire:

```go
"exp": time.Now().
	Add(24*time.Hour).
	Unix()
```

After expiration:

```text
401 Unauthorized
```

---

# Secret Management

Never:

```go
[]byte("super-secret-key")
```

in production.

Store in:

```env
JWT_SECRET=my-secret
```

Load via config.

---

# Password Storage

Never store:

```text
password = "1234"
```

Use hashing.

Go standard choice:

```go
golang.org/x/crypto/bcrypt
```

Hash:

```go
hash, err := bcrypt.GenerateFromPassword(
	[]byte(password),
	bcrypt.DefaultCost,
)
```

Verify:

```go
bcrypt.CompareHashAndPassword(
	[]byte(hash),
	[]byte(password),
)
```

---

# Typical Architecture

```text
POST /login
        ↓
UserService
        ↓
Verify Password
        ↓
Generate JWT
        ↓
Return Token
```

Protected route:

```text
JWT Middleware
        ↓
Validate Token
        ↓
Store UserID in Context
        ↓
Handler
```

---

# Common Beginner Mistakes

### ❌ Store plain passwords

Bad:

```sql
password = "1234"
```

---

### ❌ Long-lived tokens

Bad:

```text
exp = 365 days
```

Use hours or days.

---

### ❌ Put sensitive data in JWT

Bad:

```json
{
  "password": "1234"
}
```

JWT payloads are readable.

---

### ❌ Trust JWT without signature verification

Always verify:

```go
token.Valid
```

---

# Exercise

Build:

```text
POST /register
POST /login
GET  /profile
```

Requirements:

### Register

- hash password
    
- save user
    

### Login

- verify password
    
- generate JWT
    

### Profile

- protected by JWT middleware
    
- return current user ID
    

This is your first real authentication system and is the foundation for most production APIs.

After JWT, the next backend topic I'd recommend is **structured logging (`log/slog`) and graceful shutdown**, because those are things every production service should have before going live.