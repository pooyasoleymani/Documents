---
Created Date: 2026-06-01
tags:
  - golang
  - programming
---
---
# 🧠 Problem in real systems
Without graceful shutdown:
- requests get dropped
- goroutines keep running
- data can be corrupted
- logs get cut
- DB connections stay open

---
# 🚨 Real-world goal
We want this behavior:

```
CTRL + C
↓
stop accepting work
↓
finish in-flight jobs
↓
close channels
↓
exit cleanly
```

# 🔥 Key tool: OS signals
Go provides:

```go
os/signal
```

to detect:

- CTRL+C
- `SIGTERM` (Docker, Kubernetes)
- shutdown signals



# ✅ Full graceful shutdown example

## Step 1: Context + signal handling

```go
package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)
```

## Step 2: Main context with cancel

```go
func main() {
	ctx, cancel := context.WithCancel(context.Background())
	
	// catch CTRL+C / SIGTERM
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
	
	go func() {
		<-sigCh
		fmt.Println("\nShutdown signal receiverd")
		cancel()
	}()
}
```


## Step 3: Channels + workers

```go
jobs := make(chan int)
var wg sync.WaitGroup

for i := 1; i <= 3; i++ {  
	wg.Add(1)  
	go worker(ctx, i, jobs, &wg)  
}
```


## Step 4: Producer (context-aware)

```go
	go func() {		
	defer close(jobs)		
	i := 1		
	for {			
		select {
			case <-ctx.Done():
				fmt.Println("producer stopped")				
				return			
			case jobs <- i:
				i++				
				time.Sleep(500 * time.Millisecond)			
			}		
		}	
	}()
```


## Step 5: Wait for workers

```go
	wg.Wait()	
	fmt.Println("all workers finished")}
```

---

# 🧠 Worker (important pattern)

```go
func worker(ctx context.Context, id int, jobs <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()

	for {
		select {
		case <-ctx.Done():
			fmt.Println("worker", id, "shutdown")
			return

		case job, ok := <-jobs:
			if !ok {
				fmt.Println("worker", id, "jobs closed")
				return
			}

			fmt.Println("worker", id, "processing", job)
			time.Sleep(1 * time.Second) // simulate work
		}
	}
}
```

# 🔥 What happens now?

## Normal run:

```
worker processes jobs
```

---

## CTRL + C:

```
shutdown signal received
↓
context canceled
↓
producer stops
↓
jobs channel closed
↓
workers finish current job
↓
workers exit
↓
program exits cleanly
```


# 🧠 Why this is powerful
This pattern is used in:
- HTTP servers (`http.Server.Shutdown`)
- Kafka consumers
- Redis workers
- Kubernetes pods
- background schedulers