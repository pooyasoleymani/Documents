---
Created Date: 2026-02-24
tags:
  - cpp
  - programming
---
---
**Stream Buffer** is memory area that *temporarily* hold data being transferred between a program and input/output (I/O) devises.
it smooths out the differences speed between fast components (like CPU) and slower ones (like Files, Network, or terminal).

### Type of Buffering
**Fully Buffered:** writes occur when buffer is full.
**Line Buffered:** flushes at newline (console output)
**Unbuffered:** immediate I/O (slow but deterministic)


---
Reff: [[Input and Output]], [[streambuf]]