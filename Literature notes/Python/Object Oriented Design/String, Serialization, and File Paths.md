---
Created Date: 2026-05-18
tags:
  - python
  - architecture
  - programming
Next: "[[Iterator Pattern]]"
---
---
## What we Learn
- The *complexities* of *strings*, *bytes*, and *byte arrays*
- The ins and outs of *string* *formatting*
- The *mysterious* **regular expression**
- How to use the `pathlib` *module* to *manage* the `filesystem`
- A few ways to *serialize* data, including *Pickle* and *JSON*


---
## Strings
In python **string** is *immutable* sequence of **Unicode** *characters* (*UTF-8*) 

- **The important rule is this:** we *encode* our *characters* to create *bytes*; we *decode* *bytes* to recover the *characters*.
-  The `b""` *prefix* tell us these are *bytes*

### String manipulation
Like other *sequences*, **strings** can be *iterated* over (character by *character*), *indexed*,
*sliced*, or *concatenated*. The *syntax* is the same as for *lists* and *tuples*.

