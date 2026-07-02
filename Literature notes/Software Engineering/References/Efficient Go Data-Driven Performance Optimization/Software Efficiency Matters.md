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

## Efficient code NOT Readable
One of the ultra fast optimization can be *low-level* implementations with a bunch of *byte shifts*, *magic byte* , *padding*, and *unrolled loops*. Or worse, *pure assembly code* linked to your application.
Its make code *unreadable*.

---
