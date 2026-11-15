---
Created Date: 2026-06-26
tags:
  - telecom
  - protobuf
  - golang
---
---
# Protobuf Roadmap

We'll build a real project as we go.

```
telecom-protobuf/
├── proto/
├── cmd/
├── internal/
├── examples/
└── Makefile
```

---

# Phase 1 — Fundamentals (Today)

Goal:

> Understand exactly what *protobuf* is.

Topics

- What serialization is
- Binary vs Text
- Why protobuf exists
- Wire format (high level)
- Installing protobuf
- `protoc` compiler
- Go plugin
- Your first `.proto` 

No networking yet.

---

# Phase 2 — Writing `.proto` files

Topics

- syntax = `proto3`
- package
- option go_package
- message
- scalar types
- field numbers
- comments
- generated code

Example

```proto
syntax = "proto3";

package telecom;

option go_package = "github.com/pooya/telecom/pb";

message Subscriber {
    int64 imsi = 1;
    string msisdn = 2;
}
```

---

# Phase 3 — Generated Go Code

Understand

```
subscriber.pb.go
```

We'll learn

- generated struct
- reflection
- tags
- `proto.Message`
- why you NEVER edit generated files
    ---

# Phase 4 — Serialization

Learn

```
Go Struct

↓

Marshal

↓

Bytes

↓

Network

↓

Unmarshal

↓

Go Struct
```

We'll inspect bytes.

Not just call Marshal.

We'll understand what those bytes contain.

---

# Phase 5 — Wire Format

This is where many tutorials stop.

We won't.

We'll learn

```
Field Number

Wire Type

Length

Value
```

Example

```
08 96 01
```

We'll decode it by hand.

After this you'll understand Wireshark protobuf packets.

---

# Phase 6 — Complex Messages

Topics

Nested messages

```proto
message Address{}
```

inside

```proto
message User{}
```

Repeated fields

```proto
repeated string apn = 1;
```

Maps

Enums

Bytes

Oneof

Reserved

Optional fields

---

# Phase 7 — Versioning

Most important chapter.

You'll learn

Version 1

```
id
name
```

↓

Version 2

```
id
name
email
```

↓

Version 3

```
phone
email
```

How not to break production.

Exactly how Google evolves APIs.

---

# Phase 8 — Go Best Practices

Project layout

```
proto/

internal/

pkg/

pb/
```

Generate automatically

```
go generate
```

or

```
make proto
```

---

# Phase 9 — Networking

TCP

```
Client

↓

protobuf

↓

TCP

↓

protobuf

↓

Server
```

We'll write everything.

---

# Phase 10 — gRPC

Since gRPC uses protobuf

We'll learn

```
service SMSService {

    rpc SendSMS(...)
}
```

Streaming

Unary

Bidirectional

Everything.

---

# Phase 11 — Telecom Examples

Now the interesting part.

We'll model

Subscriber

```proto
message Subscriber {

    string imsi;

    string msisdn;

}
```

SMS

```proto
message SMS {

    string source;

    string destination;

    bytes tpdu;

}
```

MAP

```proto
message UpdateLocation {}
```

SCCP

```proto
message SccpMessage {}
```

TCAP

```proto
message Begin {}
```

M3UA

```proto
message M3UA {}
```

---

# Phase 12 — Production

Topics

Backward compatibility

Forward compatibility

Schema evolution

Performance

Benchmarks

Memory allocations

Zero-copy concepts

Streaming

Large messages

Compression

---

# Phase 13 — Real Telecom Project

We'll build something like

```
          SCTP Socket
                │
                ▼
          M3UA Decoder
                │
                ▼
          SCCP Decoder
                │
                ▼
          TCAP Decoder
                │
                ▼
          MAP Decoder
                │
                ▼
      Internal Go Struct
                │
                ▼
      protobuf Serializer
                │
        ┌───────┴────────┐
        ▼                ▼
      Kafka            gRPC
        ▼                ▼
 Billing Service   Monitoring
```

This is very close to how telecom companies structure their internal systems.

---

# Our teaching style

For every chapter we'll cover:

1. **Theory** (why it exists)
2. **Simple example**
3. **Go implementation**
4. **Production implementation**
5. **Common mistakes**
6. **Exercises**
7. **Mini project**