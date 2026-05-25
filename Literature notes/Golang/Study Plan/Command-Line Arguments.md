---
Created Date: 2026-05-25
tags:
  - golang
  - programming
---
---
## `os.Args`
is a **slice** of **strings**.
It contains *command-line arguments*.

```go
func main() {
	var s, sep string

	for i := 1; i < len(os.Args);i++ {
		s += sep + os.Args[i]
		sep = " "
	}
}
```

## Slices
This is one of the most important Go concepts.
```go
[]string // slice of strings like os.Args
```

```python
list[str]
```

```cpp
vector<string>
```


### String Concatenation
```go
var s, sep string
s += sep + os.Args[i]
```


## Important Go Design Choice
Strings in Go are *immutable*.
Every *concatenation* creates *new data*.
The book later explains why `strings.Join` is more *efficient*.


## Why `range` Is Important
- safer
- cleaner
- less bug-prone