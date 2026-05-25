---
Created Date: 2026-05-25
tags:
  - golang
  - programming
---
---
## Finding Duplicate Lines
You will learn:
- maps
- scanners
- reading `stdin`
- file processing
- error handling
- `make`
- counting patterns


---
## Maps in Go
Like` unordered_map` in C++.
Order is *Random*.
```go
map[keyType]valueType
//
map[string]int // map string to value
// 
make(map[string]int) // create empty map
```

- If key not exist in **map** we haven't *exception* like python and *undefined behavior* in C++
```go
counts["hello"] // --> 0
```

### Why is powerful
Because you can do this *WITHOUT* checking *existence* first.:
```go
counts[word]++
```


### Count word frequencies using:
- `strings.Fields`
- **map**


## `bufio.Scanner` 
This is your first real *streaming input* tool in Go.
```go
input := bufio.NewScanner(os.Sdtin)
```

## What is `Scanner`
A `Scanner` reads data piece-by-piece.
- line by line 
- word by word

## Why is this important?
Because real programs often process:
- files
- logs
- terminal input
- network streams
**WITHOUT** loading everything into *memory*.