---
Created Date: 2026-06-01
tags:
  - golang
  - programming
---
---
# 🧠 Problem we solve
- job queues
- background processing
- pipelines
- rate-controlled concurrency

Instead of:
```go
go job()
go job()
go job()
...
```

We want:
> A **fixed number of workers** processing **many jobs**

# 🏗 Architecture

```
jobs channel
producer ─────────────► worker pool ─────► results                                                               ↑ ↑ ↑                        
							workers
```

# 🧪 Full Example
We will:
- create 100 jobs
- use 5 workers
- safely count results


```go
package main

import (
	"fmt"
	"sync"
)

func worker(id int, jobs <- chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for job := range jobs {
		fmt.Println("Worker:", id, "Processing job:", job)
		results <- job * job
	}
}

func main() {  
	jobs := make(chan int, 100)  
	results := make(chan int, 100)  
  
	var wg sync.WaitGroup  
  
	// start workers  
	for i := 1; i <= 5; i++ {  
		wg.Add(1)  
		go worker(i, jobs, results, &wg)  
	}  
  
	// send jobs  
	for i := 1; i <= 10; i++ {  
		jobs <- i  
	}  
  
	close(jobs)  
  
// wait for workers to finish  
	go func() {  
		wg.Wait()  
		close(results)  
	}()  
  
	// collect results  
	sum := 0  
	for r := range results {  
		sum += r  
	}  
  
	fmt.Println("sum:", sum)  
}
```

# 🧠 What is happening

## Step 1: Jobs created

```
jobs = [1..10]
```

---

## Step 2: Workers start

```
worker 1
worker 2
worker 3
worker 4
worker 5
```

All waiting:

```
jobs channel
```

---

## Step 3: Work distribution
Go automatically distributes:

```
worker 1 → job 1
worker 2 → job 2
worker 3 → job 3
...
```

---

## Step 4: Closing jobs channel

```
close(jobs)
```

Meaning:

> **no more work coming**

*Workers exit loop*:

```
for job := range jobs
```

---

## Step 5: WaitGroup ensures cleanup

```
wg.Wait()
```

ensures:

> **all workers finished** before **closing results**

---

## Step 6: Results collected safely

```
sum of squares
```

---

# 💡 Why this pattern is powerful

## Without worker pool:

```
1000 goroutines → memory spike → crash risk
```

## With worker pool:

```
5 goroutines → stable → controlled performance
```

---

# ⚠️ Important rules

## 1. Never forget to close jobs

```
close(jobs)
```

Otherwise workers will **hang forever**.


## 2. Never close from worker
Only **producer** closes **channels**.

## 3. Always wait before closing results

```
wg.Wait()
close(results)
```

Otherwise *panic*:

```
send on closed channel
```


# 🧠 Mental model
Think:

```
Producer → Job queue → Workers → Result queue
```

Like a **factory**:
- jobs = raw materials
- workers = machines
- results = finished products

---

# 🚀 Real-world usage
This pattern is used in:
- HTTP request processing
- background job systems
- crawling systems
- image processing pipelines
- Kafka-like consumers

---

# 🔥 Important insight
Go concurrency is NOT:

```
"create infinite goroutines"
```

It is:

```
"control concurrency with bounded workers"
```

---

# 🧪 Your exercise (very important)
Modify this:
- increase workers to 3
- increase jobs to 20
- track how many jobs each worker processes

Add:
```go
map[int]int // workerID -> count
```
Protect it with *mutex*.