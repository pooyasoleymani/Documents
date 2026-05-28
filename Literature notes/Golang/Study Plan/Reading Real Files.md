---
Created Date: 2026-05-27
tags:
  - golang
  - programming
---
---
## Go pattern
`value, err := ` is most important pattern in go:

```go 
f, err := os.Open(filename)
```

### Use struct vs map
- *Safer*
- Faster
- Cleaner
- More Maintainable

```go
package main  
  
import (  
	"bufio"  
	"fmt"  
	"os"  
	"strings"  
)  
  
type Stats struct {  
	TotalLines int  
	UniqueLines int  
	DuplicateLines int  
}  
  
func main() {  
	counter := make(map[string]int)  
	scanner := bufio.NewScanner(os.Stdin)  
  
	for scanner.Scan() {  
	line := strings.TrimSpace(scanner.Text())  
	  
	if line == "" {  
		continue  
	}  
	counter[strings.ToLower(line)]++  
	}  
	if err := scanner.Err(); err != nil {  
		fmt.Fprintln(os.Stderr, err)  
	}  
	  
		stats := lineDetails(counter)  
		printStats(stats)  
	}  
	  
	func isDuplicate(count int) bool {  
		return count > 1  
	}  
	  
	func lineDetails(m map[string]int) Stats {  
		var stats Stats  
	  
		for _, value := range m {  
			stats.TotalLines += value  
		  
		if isDuplicate(value) {  
			stats.DuplicateLines++  
		} else {  
			stats.UniqueLines++  
			}  
		}  
	  
		return stats  
	}  
	  
	func printStats(stats Stats) {  
		fmt.Println("Total lines:", stats.TotalLines)  
		fmt.Println("Unique lines:", stats.UniqueLines)  
		fmt.Println("Duplicate lines:", stats.DuplicateLines)  
}
```


---
## VERY Important Go Philosophy
Go prefers:
- *explicit* *error handling*
- *simple* *control flow*

## Problem with open file 
In *Go* error handling is *explicit* so if error occur program exited and file become *open*  solution is `defer` .
`defer` execute later when function exited.

```go
package main

import (
	"fmt"
	"os"
	"bufio"
)

func main() {
	file, err := os.Open("text.txt")
		if err != nil {
			fmt.Println("Error:", err)
			return
	}

	defer file.Close()

	scanner := bufio.NewScanner()
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Scanner Error:", err)
	}
}
```



## Resource pattern in Go

```go 
resource, err := acqure()
if err != nil {
	return err
}
defer resource.Close()
```

You will see this constantly:
- *files*
- *network connections*
- *HTTP* bodies
- *databases*
- *mutexes* sometimes

### `defer` Behavior
1. In *reverse order*
2. When *function* *exits*

```go 
fmt.Println("1")
fmt.Println("2")

// output
2
1
```
