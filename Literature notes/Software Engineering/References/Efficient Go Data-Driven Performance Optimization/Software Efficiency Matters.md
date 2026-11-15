---
Created Date: 2026-07-02
tags:
  - golang
  - architecture
Related: "[[Complexity Analysis]]"
---
---
# What is software performance ?
*Software performance* means *“how well software runs”* and consists of
*three* core execution elements you can improve (or sacrifice):
## Accuracy
The number of errors you make while doing the work to accomplish the task. 
This can be measured for software by the number of *wrong results* your application produces. 
**Example:** how many requests finished with non-200 HTTP status codes in a web system.
## Speed
How fast you do the work needed to accomplish the *task*—the timeliness of *execution*.
This can be observed by operation *latency* or *throughput*. 
**Example:**,we can estimate that typical compression of 1 GB of data in memory typically takes around 10 s (latency), allowing approximately 100 MBps throughput.
## Efficiency
The ratio of the useful energy delivered by a *dynamic system* to the energy supplied to it. 
In other words, how much effort we wasted. 
For instance, if our operation of fetching 64 bytes of valuable data from disk allocates 420 bytes on RAM, our memory efficiency would equal 15.23%.
This does not mean our operation is 15.23% efficient in absolute measure.
We did not calculate energy, CPU time, heat, and other efficiencies. 

---
# Calculate performance
`performance = ( accuracy * efficiency * speed )`

---
# Common Efficiency Misconceptions
In *code reviews* or *sprint plannings*, to *ignore* the *efficiency* of the software “for now” is staggering.

## 1. Efficient code NOT Readable
One of the ultra fast optimization can be *low-level* implementations with a bunch of *byte shifts*, *magic byte* , *padding*, and *unrolled loops*. Or worse, *pure assembly code* linked to your application.
Its make code *unreadable*.

### Solution
We can choose a more efficient *algorithm*, *faster data structure*, or a *different system trade-off*. These will likely result in much *cleaner*, *maintainable* code and better *performance* than improving *efficiency* after releasing the software.

>[!NOTE] Readability Is Important!
>It’s easier to optimize readable code than make heavily optimized code readable. This is true for both humans and compilers that might attempt to optimize your code!

#### 1. Code after optimization can be more readable

**Example 1.1** Simple calculation for the ratio of reported errors
```go
type ReportGetter interface {
	Get() []Report
}

func FailureRatio(reports ReportGetter) float64 {
	if len(reports.Get()) == 0 {
		return 0
	}
	var sum float64
	for _, report := range reports.Get() {
		if report.Error() != nil {
			sum++
		}
	}
	return sum / float64(len(reports.Get()))
}
```

**Example 1-2**. Simple, more efficient calculation for the ratio of reported errors.
```go
func FailureRatio(reports ReportGetter) float64 {
	got := reports.Get()
	if len(got) == 0 {
		return 0
	}
	var sum float64
	for _, report := range got {
		if report.Error() != nil {
			sum++
		}
	}
	return sum / float64(len(got))
```


1. **Example 1.2** is *safer* because in **example 1.1** may possible *race condition*
2. **Example 1-2** code is more *readable* By replacing three instances of the `Get()` call with a simple variable, we also minimize the potential *side effects*.



**Example 1-3**. Simple loop without optimization
```go
func createSlice(n int) (slice []string) {
	for i := 0; i < n; i++ {
	slice = append(slice, "I", "am", "going", "to", "take", "some", "space")
	}
	return slice
}
```

**Example 1-4**. Simple loop with pre-allocation optimization. Is this less readable?
```go
func createSlice(n int) []string {
	slice := make([]string, 0, n*7)
	for i := 0; i < n; i++ {
	slice = append(slice, "I", "am", "going", "to", "take", "some", "space")
	}
	return slice
}
```
