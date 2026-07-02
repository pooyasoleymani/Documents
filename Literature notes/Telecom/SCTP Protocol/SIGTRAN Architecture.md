---
Created Date: 2026-06-20
tags:
  - architecture
  - SCTP
  - golang
Next: "[[SS7 over SCTP]]"
---
---

# Lesson 3: Why SIGTRAN Exists

Before we talk about M3UA, you need to understand the problem it solves.

---

## Traditional SS7 Stack

Originally telecom networks used dedicated signaling links:

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

Where:

| Layer | Purpose             |
| ----- | ------------------- |
| MTP1  | Physical            |
| MTP2  | Link                |
| MTP3  | Routing             |
| SCCP  | Extended addressing |
| TCAP  | Transactions        |
| MAP   | Mobile roaming      |

---

## Roaming Example

Subscriber from Operator A enters Operator B.

Visited network sends:

```text
UpdateLocation
```

to home HLR.

Message:

```text
MAP UpdateLocation
```

travels through:

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

---

## The Problem

MTP1/MTP2/MTP3 were designed for:

```text
Dedicated telecom networks
```

not:

```text
IP networks
```

When operators started migrating to IP:

```text
Ethernet
IP
Routers
Switches
```

they needed a way to transport SS7 signaling over IP.

---

# SIGTRAN

SIGTRAN means:

```text
Signaling Transport
```

It is a family of protocols standardized by the Internet Engineering Task Force.

Goal:

```text
SS7 Signaling
      ↓
      IP Network
```

---

# Key Idea

Replace:

```text
MTP1
MTP2
MTP3
```

with:

```text
IP
SCTP
SIGTRAN Protocol
```

---

# Most Important SIGTRAN Protocol

For roaming engineers:

```text
M3UA
```

is the most important protocol.

M3UA means:

```text
MTP Level 3 User Adaptation
```

It allows SCCP to think it is still talking to MTP3:

```text
SCCP
 ↓
M3UA
 ↓
SCTP
 ↓
IP
```

instead of:

```text
SCCP
 ↓
MTP3
 ↓
MTP2
 ↓
MTP1
```

---

# New Stack

Modern roaming:

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

This is the stack you'll see in:

- HLR
- STP
- SMSC
- EIR
- Roaming hubs
- SS7 firewalls

---

# Architecture Exercise

Answer these before we continue:

### Q1

Why can't SCCP communicate directly over IP?

---

### Q2

What protocol replaced MTP3 when telecom moved to IP networks?

---

### Q3

In the stack:

```text
MAP
TCAP
SCCP
M3UA
SCTP
IP
```

which protocol directly transports SCCP messages?

---

### Q4

Why is SCTP preferred under M3UA instead of TCP?

Try answering these carefully. Once you get them right, we'll start M3UA internals:

```text
ASP
AS
SG
ASPUP
ASPAC
DATA
```

which are the messages you actually see when bringing up a roaming signaling link.