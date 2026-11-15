---
Created Date: 2026-06-28
tags:
  - telecom
  - golang
  - NATS
Next: "[[Event Envelope Design]]"
---
---
# Session 3 — Building the Broker Package

## Final Goal

Eventually, your business code should look like this:

```go
err := broker.Publish(ctx, event)
```

and

```go
broker.Subscribe(
    ctx,
    "sms.send",
    smsHandler,
)
```

Notice there is **no NATS code** in the business layer.

---

# Step 1 — Project Layout

```
appointment-system/

internal/

    broker/
        broker.go
        connection.go
        publisher.go
        subscriber.go
        stream.go
        consumer.go

    events/

    config/

    handlers/

    proto/
```

The broker package is the only package that imports the `NATS` client.

---

# Step 2 — Install Dependencies

```bash
go get github.com/nats-io/nats.go
```

For `protobuf`:

```bash
go get google.golang.org/protobuf
```

---

# Step 3 — Broker Interface

The rest of your application should depend on an interface, not a concrete implementation.

```go
type Broker interface {
    Publish(context.Context, Event) error

    Subscribe(
        context.Context,
        string,
        Handler,
    ) error

    Close() error
}
```

Why?

Tomorrow you might replace NATS with Kafka or RabbitMQ.

Nothing outside the broker changes.

---

# Step 4 — Connection

Create

```
internal/broker/connection.go
```

```go
type Config struct {
    URL string
}
```

Broker implementation

```go
type broker struct {
    conn *nats.Conn
    js   jetstream.JetStream
}
```

Notice something important.

We keep both

```
Conn
```

and

```
JetStream
```

because:

- Conn manages the TCP connection.
- JetStream manages streams and consumers.

---

# Step 5 — Constructor

I recommend using a constructor.

```go
func New(cfg Config) (*broker, error)
```

Responsibilities:

```
Connect

↓

Ping server

↓

Create JetStream context

↓

Return broker
```

Nothing more.

Don't create streams here.

Don't subscribe here.

Don't publish here.

A constructor should only initialize the object.

---

# Step 6 — Why Not Global Variables?

Avoid this pattern:

```go
var nc *nats.Conn
```

Everywhere in your code:

```go
nc.Publish(...)
```

Problems:

- Difficult to test
    
- Hard to mock
    
- Hidden dependencies
    
- Multiple packages share mutable state
    

Instead:

```go
broker.Publish(...)
```

Everything is explicit.

---

# Step 7 — Event Interface

Business code shouldn't care that protobuf is used internally.

Define an interface:

```go
type Event interface {
    Subject() string
    Marshal() ([]byte, error)
}
```

Every event implements it.

Example:

```go
type SendSMS struct {
    Phone string
    Text  string
}
```

```go
func (e SendSMS) Subject() string {
    return "sms.send"
}
```

```go
func (e SendSMS) Marshal() ([]byte, error)
```

returns protobuf bytes.

Notice the broker doesn't know about SMS.

---

# Step 8 — Publish

The publish function becomes tiny.

```
Receive Event

↓

Marshal

↓

Publish

↓

Return
```

No switch statements.

No event-specific logic.

---

# Step 9 — Handler

Consumers need handlers.

```go
type Handler interface {
    Handle(
        context.Context,
        []byte,
    ) error
}
```

SMS worker:

```go
type SMSHandler struct{}
```

implements

```go
Handle(...)
```

Telecom worker:

```go
type TelecomHandler struct{}
```

implements the same interface.

The broker never knows which one it is calling.

---

# Step 10 — Subscribe

The API should look like this:

```go
broker.Subscribe(
    ctx,
    "sms.send",
    smsHandler,
)
```

Internally:

```
Create Consumer

↓

Receive Message

↓

Call Handler

↓

ACK

↓

Wait Next
```

---

# Step 11 — Message Flow

```
Publish()

↓

JetStream Stream

↓

Consumer

↓

Handler

↓

ACK
```

Notice

The broker owns everything except

```
Handler
```

This separation is extremely important.

---

# Step 12 — Why ACK After the Handler?

Wrong:

```
Receive

↓

ACK

↓

Handler
```

If the worker crashes:

```
ACK already sent

↓

Message lost
```

Correct:

```
Receive

↓

Handler

↓

ACK
```

If the handler crashes:

```
No ACK

↓

JetStream redelivers
```

Exactly what we want.

---

# Step 13 — Context

Every public method should receive a context.

Instead of

```go
Publish(event)
```

always use

```go
Publish(
    ctx,
    event,
)
```

Benefits:

- cancellation
- deadlines
- tracing
- logging
- request propagation

In Go, `context.Context` is the standard way to carry request-scoped information.

---

# Step 14 — Error Handling

Never ignore publish failures.

```
Marshal

↓

Publish

↓

Error?

↓

Return
```

Don't log and continue.

The caller decides how to handle the error.

---

# Step 15 — Logging

Avoid logging inside the broker package unless it's about the broker itself (connection established, reconnect, disconnected, etc.).

Instead:

```
API

↓

Publish()

↓

Error

↓

API logs
```

This keeps the broker reusable and avoids duplicate logs.

---

# Final Architecture

```
                 Business Layer

      SMS Service      Appointment Service

               │

               ▼

           Broker Interface

               │

               ▼

         NATS Implementation

               │

               ▼

          NATS JetStream
```

The business layer never imports `github.com/nats-io/nats.go`.

Only the broker package does.

---

# One Design Change I'd Make

Earlier, we defined:

```go
type Event interface {
    Subject() string
    Marshal() ([]byte, error)
}
```

As the project grows, especially with Protocol Buffers, I would refine this to separate the transport envelope from the domain payload.

Instead of every event implementing `Marshal`, I'd define:

```go
type Event interface {
    Subject() string
    ProtoMessage() proto.Message
}
```

Then the broker is responsible for protobuf serialization:

```go
data, err := proto.Marshal(event.ProtoMessage())
```

This has several advantages:

- Domain events remain plain Go types that expose their protobuf message.
    
- Serialization is centralized in one place.
    
- Changing the serialization format in the future (e.g., adding compression or encryption) only affects the broker.
    

This is a pattern commonly used in production systems because it keeps domain code independent of transport details.

---

## Next Session

In the next session we'll implement:

- A reusable `EventEnvelope` protobuf message.
    
- Correlation IDs.
    
- Event versioning.
    
- Metadata (timestamps, producer, trace ID).
    
- Generic publish and consume functions using that envelope.
    

That envelope will become the wire format for every event in your appointment and telecom platform.