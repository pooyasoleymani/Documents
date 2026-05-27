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