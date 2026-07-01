---
Created Date: 2026-06-19
tags:
  - architecture
  - SCTP
  - golang
Next: "[[How SCTP works internally]]"
---
---

The signaling network used dedicated telecom links.
Examples:

- SMS routing
- Location updates
- Roaming
- Authentication

All used SS7.

---
## Problem

Operators wanted to move to IP networks.

Question:

```text
Can we replace SS7 links with TCP/IP?
```

At first glance:

```text
Application
    ↓
	TCP
    ↓
	IP
```

seems enough.

But telecom networks have requirements that normal web applications don't.

---

# Requirement 1: High Availability
Suppose an [[HLR(Home location register)]] communicates with an [[STP(Signal transfer point)]].

`TCP`:

```text
HLR -------- TCP -------- STP
```

Link failure:

```text
HLR ----X---- TCP ----X---- STP
```

- TCP connection dies.
- Reconnection needed.
- Telecom operators hate this.

Because:

```text
Lost signaling = Lost subscribers = Lost revenue
```

---

# Requirement 2: Multiple Network Paths

Telecom equipment usually has multiple interfaces.

Example:

```text
HLR

10.1.1.1
10.1.1.2
```

and

```text
STP

20.1.1.1
20.1.1.2
```

TCP:

```text
10.1.1.1 <-> 20.1.1.1
```

Only one path.

If it fails:

```text
disconnect
reconnect
```

Not ideal.

---

# Requirement 3: Message Boundaries

Telecom signaling is message-based.

Example:

```text
UpdateLocation
```

is one message.

```text
SendRoutingInfo
```

is another message.

TCP is a byte stream.

Example:

Sender:

```text
MessageA
MessageB
```

Receiver may get:

```text
Mes
sageAMessage
B
```

TCP doesn't preserve message boundaries.

You must build framing.

---

# Requirement 4: Head-of-Line Blocking

Suppose we send:

```text
Message1
Message2
Message3
```

Packet 2 lost.

TCP behavior:

```text
1 delivered
2 missing
3 waiting
```

Everything waits.

This is called:

```text
Head Of Line Blocking
```

Bad for signaling.

---

# SCTP Solution

SCTP was designed specifically for telecom signaling.

```text
Application
     ↓
   SCTP
     ↓
    IP
```

Features:

```text
Reliable
Message Oriented
Multi-Homed
Multi-Streamed
```

---

# Architecture View

Think of SCTP as:

```text
TCP
+
UDP
+
Telecom Redundancy
```

combined.

---

# Multi-Homing

Most important telecom feature.

Association:

```text
HLR
 ├── 10.1.1.1
 └── 10.1.1.2

STP
 ├── 20.1.1.1
 └── 20.1.1.2
```

One SCTP association:

```text
Association
```

contains all addresses.

```text
          Primary Path
10.1.1.1 <----------> 20.1.1.1

          Backup Path
10.1.1.2 <----------> 20.1.1.2
```

Failure:

```text
Primary Down
```

SCTP automatically switches.

No reconnect.

This is why telecom vendors adopted SCTP.

---

# Multi-Streaming

Inside one association:

```text
Association
    |
    +-- Stream 0
    +-- Stream 1
    +-- Stream 2
```

Imagine:

```text
Stream 0 = Authentication
Stream 1 = Location Update
Stream 2 = SMS
```

Packet loss in Stream 0:

```text
Authentication waits
```

but:

```text
SMS continues
Location Update continues
```

Huge improvement over TCP.

---

# Real Roaming Example

Suppose a subscriber travels:

```text
Home Network (Iran)

      ↓

Visited Network (Turkey)
```

Phone powers on.

Visited network sends:

```text
UpdateLocation
```

toward Home HLR.

Stack:

```text
MAP
 ↓
TCAP
 ↓
SCCP
 ↓
M3UA
 ↓
SCTP
 ↓
IP
```

Notice:

```text
MAP does NOT talk directly to SCTP
```

Many engineers initially misunderstand this.

---

# Complete Roaming Stack

Traditional:

```text
MAP
 ↓
TCAP
 ↓
SCCP
 ↓
MTP3
 ↓
MTP2
 ↓
MTP1
```

SIGTRAN version:

```text
MAP
 ↓
TCAP
 ↓
SCCP
 ↓
M3UA
 ↓
SCTP
 ↓
IP
```

SCTP replaces lower SS7 transport layers.

---

# How Go Fits

As a Go engineer you usually build:

```text
SMS Router
STP Simulator
M3UA Gateway
Diameter Router
Roaming Monitor
Signaling Probe
```

Not SCTP itself.

Linux kernel already implements SCTP.

Your Go code uses:

```go
github.com/ishidawataru/sctp
```

which talks to the kernel SCTP stack.

Architecture:

```text
Your Go App
      ↓
 SCTP Library
      ↓
 Linux SCTP
      ↓
 Network
```

Best practice:

```text
 Business Logic
      ↓
 Signaling Layer
      ↓
 SCTP Transport
```

Avoid:

```text
 Business Logic
      ↓
 Raw SCTP Calls Everywhere
```

This creates tight coupling and becomes difficult to test.

---

# Architecture Principle

A production roaming system should follow:

```text
domain/
    roaming.go

transport/
    sctp/

protocol/
    m3ua/
    diameter/
    map/

cmd/
```

Dependency direction:

```text
Domain
 ↑
Protocol
 ↑
Transport
```

Domain must not know SCTP details.

This follows:

- Clean Architecture
- Dependency Inversion Principle
- Separation of Concerns

---

# Common Beginner Mistakes

### Mistake 1

Thinking SCTP replaces SS7.

Wrong:

```text
SS7 Application
    ↓
SCTP
```

Correct:

```text
SS7 Application
 ↓
M3UA
 ↓
SCTP
```

---

### Mistake 2

Learning SCTP sockets before understanding signaling.

Result:

```text
Can code SCTP
Cannot understand roaming traces
```

---

### Mistake 3

Ignoring multi-homing.

In telecom this is often the primary reason SCTP was selected.

---

### Mistake 4

Treating SCTP like TCP.

SCTP is:

```text
Message-oriented
```

not:

```text
Byte-stream oriented
```

---

# Exercise

Draw the signaling path for this scenario:

```text
Subscriber from Operator A

travels to

Operator B
```

and identify:

1. Where MAP is used.
2. Where M3UA is used.
3. Where SCTP is used.
4. Which network element receives `UpdateLocation`.

Try answering that, and in the next lesson we'll move to **SCTP internals**:

- Associations
- INIT / INIT-ACK
- COOKIE-ECHO
- TSN
- SACK
- Heartbeats
- Failover algorithms
- Multi-homing implementation details

Those concepts are essential before writing any Go SCTP code.