---
Created Date: 2026-06-26
tags:
  - telecom
  - protobuf
  - golang
---
---
# Lesson 2 — Installing Protobuf and Creating Your First Message

## Goal

By the end of this lesson you will know:

- What `protoc` is
    
- Why we need code generation
    
- How Go integrates with protobuf
    
- How to create your first `.proto` file
    
- How Go code is generated
    

---

# Step 1: Install `protoc`

There are three different things involved:

```
           protobuf language
                  │
                  ▼
             protoc compiler
                  │
                  ▼
         Go code generator plugin
                  │
                  ▼
           Generated Go code
```

Many beginners confuse these.

They are **three different components**.

---

## Component 1 — `.proto`

This is your schema.

Example

```proto
message Subscriber {
    int64 imsi = 1;
}
```

You write this.

---

## Component 2 — `protoc`

This is the compiler.

```
subscriber.proto

↓

protoc

↓

subscriber.pb.go
```

Think of it like

```
main.go

↓

go build

↓

binary
```

except `protoc` generates source code instead of a binary.

---

## Component 3 — Go plugin

`protoc` itself doesn't know Go.

It asks a plugin:

```
protoc

↓

protoc-gen-go

↓

Go source
```

---

# Install the Go plugins

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

These binaries will be placed in:

```
$HOME/go/bin
```

or

```
$GOPATH/bin
```

Make sure it's in your `PATH`.

Check:

```bash
protoc-gen-go --version
```

---

# Project Structure

Create this:

```
telecom-protobuf/

├── go.mod
├── proto/
│   └── subscriber.proto
├── pb/
├── cmd/
│   └── demo/
│       └── main.go
└── Makefile
```

Why this layout?

- `proto/` → schema files
    
- `pb/` → generated code
    
- `cmd/` → applications
    
- `internal/` → business logic (later)
    

This scales well for large projects.

---

# Writing Your First `.proto`

Create:

```
proto/subscriber.proto
```

```proto
syntax = "proto3";

package telecom;

option go_package = "telecom-protobuf/pb";

message Subscriber {
    int64 imsi = 1;
    string msisdn = 2;
}
```

Let's examine every line.

---

## `syntax = "proto3";`

Always the first line.

```
syntax = "proto3";
```

This selects Protocol Buffers version 3.

Today, nearly all new projects use **proto3**.

---

## `package`

```proto
package telecom;
```

This is the protobuf package.

It is **not** the Go package.

People often confuse them.

---

## `option go_package`

```proto
option go_package = "telecom-protobuf/pb";
```

This tells the Go generator:

> Put generated Go code in this package.

Without it, generation either fails or produces less useful results.

---

## Message

```proto
message Subscriber {

}
```

Think of a message as a Go struct.

```
message

↓

Go struct
```

---

## Fields

```proto
int64 imsi = 1;
```

means

```go
IMSI int64
```

---

```proto
string msisdn = 2;
```

means

```go
MSISDN string
```

---

# Why Field Numbers?

This is the heart of protobuf.

You might think

```proto
int64 imsi;
```

would be enough.

But protobuf needs

```proto
int64 imsi = 1;
```

because **the number is what gets encoded on the wire**.

The name is mainly for humans and generated code.

Imagine the binary message contains:

```
Field #1

↓

432111111111111
```

instead of

```
"imsi"

↓

432111111111111
```

That is one reason protobuf messages are much smaller than JSON.

---

# Generate Go Code

Run:

```bash
protoc \
    --proto_path=proto \
    --go_out=. \
    proto/subscriber.proto
```

You'll get something like:

```
pb/
    subscriber.pb.go
```

---

# What Was Generated?

Open it.

You'll see a lot of code.

Don't panic.

You only need to recognize the important parts.

Generated struct:

```go
type Subscriber struct {
    Imsi   int64
    Msisdn string
}
```

It also contains:

- reflection metadata
    
- descriptor information
    
- marshal support
    
- unmarshal support
    
- size calculation
    
- unknown field handling
    

This is why the file is large.

---

# Never Edit `*.pb.go`

Treat generated files like compiled artifacts.

If you modify:

```
subscriber.pb.go
```

then regenerate it:

```
protoc ...
```

your changes disappear.

Always edit:

```
subscriber.proto
```

and regenerate.

---

# How Generation Works

```
subscriber.proto
       │
       ▼
     protoc
       │
       ▼
protoc-gen-go
       │
       ▼
subscriber.pb.go
       │
       ▼
Your Go program imports it
```

---

# Common Beginner Mistakes

### ❌ Editing `subscriber.pb.go`

Never do it.

---

### ❌ Changing field numbers

Bad:

```proto
imsi = 1
```

↓

Later

```proto
imsi = 5
```

This breaks compatibility with previously serialized data.

---

### ❌ Forgetting `go_package`

Always define it.

---

### ❌ Reusing deleted field numbers

Suppose:

```proto
string name = 2;
```

Later:

```proto
string phone = 2;
```

Very dangerous.

Instead:

```proto
reserved 2;
```

---

# How Big Companies Organize `.proto` Files

Instead of one huge file:

```
everything.proto
```

they use domain-based files:

```
proto/

    subscriber.proto

    sms.proto

    map.proto

    m3ua.proto

    billing.proto

    charging.proto

    fraud.proto
```

Each domain owns its schema.

---

# Telecom Example

Imagine your decoder receives a MAP UpdateLocation.

Internally you convert it to:

```proto
message UpdateLocation {

    string imsi = 1;

    string msc = 2;

    string vlr = 3;

    int64 timestamp = 4;
}
```

Every downstream service—billing, monitoring, analytics—uses the same generated types regardless of language.

---

# Assignment

Create the following project:

```
telecom-protobuf/

├── go.mod
├── proto/
│   └── subscriber.proto
├── pb/
└── cmd/demo/main.go
```

1. Install `protoc`, `protoc-gen-go`, and `protoc-gen-go-grpc` if you haven't already.
    
2. Write `subscriber.proto` exactly as shown.
    
3. Generate `subscriber.pb.go`.
    
4. Open the generated file and identify:
    
    - the generated `Subscriber` struct,
        
    - the `Reset()` method,
        
    - the `String()` method,
        
    - the `ProtoReflect()` method.
        

Don't worry yet about how those methods work. In the next lesson we'll use the generated `Subscriber` type to **marshal and unmarshal binary data**, then inspect the actual bytes to understand protobuf's wire format. That's where protobuf starts to become much more intuitive.