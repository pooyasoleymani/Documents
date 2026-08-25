---
Created Date: 2026-06-28
tags:
  - telecom
  - golang
  - NATS
Next: "[[Installing NATS JetStream]]"
---
---
# Session 1 — Understanding NATS

## What is NATS?

NATS is a lightweight, high-performance messaging system.

Think of it as a central communication bus.

Instead of services calling each other directly:

```
Appointment Service
        │
        │ HTTP
        ▼
 SMS Service
```

everything communicates through NATS:

```
                    NATS
                      │
        ┌─────────────┼─────────────┐
        │             │             │
 Appointment     SMS Worker    Telecom Worker
        │             │             │
        └─────────────┼─────────────┘
```

No service knows where another service is running.

---

# Why Telecom Companies Like Messaging

Imagine your system receives:

- 20,000 SMS requests
    
- 10,000 Location Updates
    
- 5,000 Appointment Events
    

If every request is HTTP:

```
API
 │
 ├── HTTP
 ├── HTTP
 ├── HTTP
 ├── HTTP
 └── HTTP
```

Your API waits for every worker.

Workers become overloaded.

Failures cascade.

Instead:

```
API

Publish

↓

NATS

↓

Workers process independently
```

The API finishes quickly.

Workers process at their own pace.

---

# Core Concepts

NATS has only a few concepts.

## 1. Connection

Every application connects to the NATS server.

```
API --------\
SMS --------- > NATS Server
Worker -----/
```

---

## 2. Subject

A subject is similar to a routing key or topic.

Example:

```
sms.send

appointment.created

subscriber.location.update

billing.invoice.created
```

Subjects are hierarchical.

```
telecom.sms.send

telecom.sms.delivered

telecom.sms.failed
```

---

## 3. Publisher

A publisher sends messages.

```
Publish

Subject

↓

sms.send
```

Message

```
protobuf bytes
```

That's all.

---

## 4. Subscriber

Subscriber listens.

```
Subscribe

↓

sms.send
```

Whenever a message arrives

↓

Process it.

---

# Request / Reply

NATS has built-in Request/Reply.

Instead of creating a response queue manually:

```
API

↓

Request()

↓

NATS

↓

Worker

↓

Reply()
```

The Go client creates an internal reply subject automatically.

Example:

```
Request

↓

sms.send

↓

Worker

↓

Reply

↓

API
```

This is much simpler than implementing a request-response pattern yourself.

However, for **long-running telecom operations** (for example, waiting for an external SMSC acknowledgment or an HLR query), it's often better to publish a completion event rather than keep a request waiting.

---

# Queue Groups

Suppose you have three SMS workers.

```
SMS Worker 1

SMS Worker 2

SMS Worker 3
```

All subscribe to:

```
sms.send
```

Without queue groups:

```
Message

↓

Worker1

Worker2

Worker3
```

All receive the same message.

With a queue group:

```
Message

↓

Worker2
```

Only one worker processes it.

This is how you scale horizontally.

---

# Wildcards

Suppose you subscribe to:

```
telecom.*
```

You receive

```
telecom.sms

telecom.hlr

telecom.msc
```

Another wildcard:

```
telecom.>
```

Receives

```
telecom.sms.send

telecom.sms.delivered

telecom.sms.failed

telecom.hlr.query

telecom.location.update
```

This is useful for monitoring or logging services.

---

# Core NATS vs JetStream

This is one of the most important topics.

## Core NATS

```
Publisher

↓

NATS

↓

Subscriber
```

If nobody is listening

↓

Message disappears.

Advantages:

- Extremely fast
- Very low latency
- Minimal resource usage

Disadvantages:

- No persistence
- No replay
- No redelivery

Good for:

- Live notifications
- Cache invalidation
- Presence updates

---

## JetStream

```
Publisher

↓

Stream (Disk)

↓

Consumer
```

Messages are stored.

If a worker crashes

↓

The message remains.

When the worker comes back

↓

It processes the pending message.

Advantages:

- Persistence
- Acknowledgments
- Replay
- Durable consumers
- At-least-once delivery

For appointment processing and telecom events, this is the appropriate choice.

---

# Stream

A stream stores messages.

```
Subject

↓

appointment.*
```

Stored in

```
APPOINTMENT_STREAM
```

Another stream:

```
telecom.*
```

Stored in

```
TELECOM_STREAM
```

---

# Consumer

A consumer reads messages from a stream.

```
APPOINTMENT_STREAM

↓

Consumer

↓

Worker
```

Multiple consumers can read the same stream independently.

---

# Durable Consumer

Without durability:

Worker crashes.

Consumer position is lost.

With a durable consumer:

```
Message 1

Message 2

Message 3

Crash

Restart

Continue from Message 4
```

This is essential for production services.

---

# Acknowledgment (ACK)

After processing:

```
Receive Message

↓

Process

↓

Ack()
```

JetStream removes the message from the consumer's pending set.

If the worker dies before acknowledging:

```
Receive

↓

Crash
```

No ACK.

JetStream waits.

Then redelivers the message to another worker or when the worker reconnects.

---

# Recommended Subject Naming

I recommend following a consistent convention:

```
appointment.created

appointment.updated

appointment.completed

sms.send

sms.sent

sms.failed

telecom.location.update

telecom.hlr.query

telecom.hlr.response

notification.email.send

notification.sms.send
```

Avoid names like:

```
event1

task

work

message
```

Descriptive subjects make the system much easier to understand and maintain.

---

# Architecture for Our Project

```
               HTTP API
                   │
          Publish Event
                   │
                   ▼
              NATS JetStream
                   │
      ┌────────────┼─────────────┐
      │            │             │
 SMS Worker   Telecom Worker   Notification Worker
      │            │             │
      └────────────┼─────────────┘
                   │
         Publish Completion Events
                   │
                   ▼
             API / Other Services
```

This architecture is scalable, resilient, and fits both your appointment application and telecom integrations.