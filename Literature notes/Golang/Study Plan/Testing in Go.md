---
Created Date: 2026-05-30
tags:
  - golang
  - programming
---
---
# What We need?
We don't install anythings
just use :
```sh
go test
```


## First Test

Create:
```
main.go
main_test.go
```

```go
// main.go
package main

func Add(a, b int) int {
	return a + b
}

// main_test.go
package main

import "testting"

func TestAdd(t *testing.T) {
	got := Add(2, 3)
	want := 5
	if got != want {
		t.Errorf(
			"got %d want %d\n",
			got,
			want
		)
	}
}

```

Run:
```badh
go test // output -> PASS
```


# Understanding `*testing.T`

```go
func TestAdd(t *testing.T)
```

`t` is your testing *helper*.

Common methods:
```go
t.Error(...)
t.Errorf(...)
t.Fatal(...)
t.Fatalf(...)
```


## Error

```go
t.Error("failed")
```

Marks test as *failed* but *continues*.

---

## Fatal

```go
t.Fatal("failed")
```

Marks *failed* and *immediately stops* the **test**.


# Table-Driven Tests
You'll see this style everywhere in Go **code-bases**.

Instead of:
```go
func TestAdd1(t *testing.T)
func TestAdd2(t *testing.T)
func TestAdd3(t *testing.T)
```

Write:
```go
func TestAdd(t *testing.T) {
	tests := []struct {
		a, b int
		want int
	}{
		{1, 2, 3},
		{10, 20, 30},
		{-1, 1, 0},
	}

	for _, tt := range tests {
		got := Add(tt.a, tt.b)

		if got != tt.want {
			t.Errorf(
				"Add(%d,%d)=%d want %d",
				tt.a,
				tt.b,
				got,
				tt.want,
			)
		}
	}
}
```


# Why Table Tests?
Easy to *add cases*:

```go
{100, 200, 300}
```

**No** *new test function* needed.
This is the idiomatic Go style.


# Subtests
Even better:

```go
for _, tt := range tests {
	t.Run(		
		fmt.Sprintf("%d+%d", tt.a, tt.b),		
		func(t *testing.T) {			
			got := Add(tt.a, tt.b)			
			if got != tt.want {				
				t.Errorf(...)			
			}		
		},	
	)
}
```

Now test output shows which case failed.


# Testing Errors

```go 
func Divide(a, b int) (int, error)
```

Implementation:
```go
func Divide(a, b int) (int, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}

	return a / b, nil
}
```

Test:
```go
func TestDivideByZero(t *testing.T) {
	_, err := Divide(10, 0)
	if err == nil {
		t.Fatal("expected error)
	}
}
```

Test HTTP Server:
```go
package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)
  
func TestRootHandler(t *testing.T) {
	req := httptest.NewRequest(
		http.MethodGet,
		"/",
		nil,
	)

	rec := httptest.NewRecorder()
	
	rootHandler(rec, req)

	resp := rec.Result()

	if resp.StatusCode != http.StatusOK {
		t.Errorf(
			"got %d want %d",
			resp.StatusCode,
			http.StatusOK,
		)
	}
}

  

func TestGreetHandlerWithAuth_Success(t *testing.T) {
	req := httptest.NewRequest(
		http.MethodGet,
		"/greet?name=Pooya",
		nil,
	)

	req.Header.Set("X-API-Key", "secret")

	rec := httptest.NewRecorder()
	handler := auth(http.HandlerFunc(greetHandler))
	handler.ServeHTTP(rec, req)
	resp := rec.Result()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("got %d want %d", resp.StatusCode, http.StatusOK)
	}

	body := rec.Body.String()
	expected := "Welcom Pooya\n"
	if body != expected {
		t.Errorf("body = %q; want %q", body, expected)
	}
}

  

func TestGreetHandlerWithAuth_Unauthorized(t *testing.T) {
	req := httptest.NewRequest(
		http.MethodGet,
		"/greet?name=Pooya",
		nil,
	)

	// no API key set
	rec := httptest.NewRecorder()
	handler := auth(http.HandlerFunc(greetHandler))
	handler.ServeHTTP(rec, req)
	resp := rec.Result()
	
	if resp.StatusCode != http.StatusUnauthorized {
		t.Fatalf("got %d want %d", resp.StatusCode, http.StatusUnauthorized)
	}
}
```

# Benchmarking
You already wrote timing *functions* manually.
Go has built-in benchmarks.

---

Example:
```go
func BenchmarkAdd(b *testing.B) {
	for i := 0; i < b.N; i++ {
			Add(1, 2)	
		}
	}
```

Run:
```BASH
go test -bench=.
```

Output:
```
BenchmarkAdd-8    1000000000    0.3 ns/op
```



# Coverage
Go can show test coverage.

Run:
```sh
go test -cover
```

Example:
```
coverage: 87.5% of statements
```

---

# Common Testing Conventions
Test files:
```
xxx_test.go
```

Test functions:
```
func TestXxx(...)
```

Benchmarks:
```
func BenchmarkXxx(...)
```

Examples:
```
func ExampleXxx(...)
```