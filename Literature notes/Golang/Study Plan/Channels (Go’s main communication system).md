---
Created Date: 2026-05-29
tags:
  - golang
  - programming
---
---
# Channels
If **goroutines** are “**workers**”, then:
> **channels** are the **pipes** between *workers*

A **channel** is:
> a *typed queue* that *goroutines* can **send/receive** *values* through

# 🧠 Why channels exist
Before channels, we had:
- *shared memory*
- *mutex*
- *race conditions*
Go introduces a different idea:
>  **“Do not share memory — communicate instead”**


## Basic Syntax

```go
ch := make(chan int)

// Sending data
ch <- 42

// Receiving data
value := <-ch
```

### Example

```go
package main

import "fmt"

func main() {
	ch := make(chan int)
	
	go func() {
		ch <- 42
	}()
	
	value := <-ch
	
	fmt.Println(value)
}
```