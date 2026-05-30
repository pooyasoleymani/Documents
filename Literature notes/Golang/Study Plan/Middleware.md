---
Created Date: 2026-05-30
tags:
  - golang
  - programming
---
----
# What is Middleware?
**Middleware** is:
> a *function* that *wraps* another *handler*

When we don't want to repeat something:
- *logging*
- *authentication*
- *method checks*
- *request timing*
- *rate limiting*
in every **handler**.
**Middleware** solves this.


```
Request
   ↓
Logging Middleware
   ↓
Authentication Middleware
   ↓
Handler
   ↓
Response
```

