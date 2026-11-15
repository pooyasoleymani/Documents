---
Created Date: 2026-06-26
tags:
  - telecom
  - protobuf
  - golang
---
---

# Lesson 1 — What is serialization?

Before touching protobuf, you need to understand the problem it solves.

Suppose your Go program has:

```go
type Subscriber struct {
    IMSI   int64
    MSISDN string
}
```

This struct exists **only in your program's memory**.

Imagine memory like this:

```
+------------------------+
| IMSI   = 4321123456789 |
| MSISDN = "989121234567"|
+------------------------+
```

Now you want to:
- send it over TCP,
- write it to a file,
- publish it to Kafka,
- send it to another Go service,
- or send it to a Java service.

You **cannot** send the memory directly. The receiving process has a different memory layout, different addresses, and possibly a different language implementation.

So you first convert the object into a portable sequence of bytes:

```
Go Struct
    │
    ▼
Serialization
    │
    ▼
Byte Stream
    │
    ▼
Network / File / Queue
    │
    ▼
Deserialization
    │
    ▼
Go Struct / Java Object / C++ Object
```

That's serialization.

Different formats solve this problem differently:

| Format   | Human-readable | Compact | Fast | Cross-language |
| -------- | -------------- | ------- | ---- | -------------- |
| JSON     | ✅              | ❌       | ❌    | ✅              |
| XML      | ✅              | ❌       | ❌    | ✅              |
| YAML     | ✅              | ❌       | ❌    | ✅              |
| Gob (Go) | ❌              | ✅       | ✅    | ❌ (Go only)    |
| Protobuf | ❌              | ✅       | ✅    | ✅              |

**Why not just use JSON?**

Suppose your subscriber is:

```json
{
  "imsi": 4321123456789,
  "msisdn": "989121234567"
}
```

The field names `"imsi"` and `"msisdn"` are transmitted every single time. In a telecom system processing **millions of messages per second**, those repeated strings waste bandwidth and CPU.

Protobuf replaces those names with compact numeric field identifiers, making messages much smaller and faster to encode/decode.

---

## Your first assignment

Before we write any `.proto` files, I'd like you to do one exercise.

Write a small Go program that:

```go
type Subscriber struct {
    IMSI   int64
    MSISDN string
}
```

1. Create one `Subscriber`.
2. Serialize it using Go's `encoding/json`.
3. Print:
    - the JSON string,
    - the length of the JSON in bytes (`len(data)`).

For example:

```text
{"IMSI":4321123456789,"MSISDN":"989121234567"}

Size: 46 bytes
```