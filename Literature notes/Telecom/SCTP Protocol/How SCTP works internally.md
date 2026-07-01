---
Created Date: 2026-06-20
tags:
  - architecture
  - SCTP
  - golang
Next: "[[SIGTRAN Architecture]]"
---
---

Most engineers know:

```text
TCP -> SYN, SYN-ACK, ACK
```

But telecom engineers must understand:

```text
SCTP -> INIT, INIT-ACK, COOKIE-ECHO, COOKIE-ACK
```

because you'll see these packets in *Wireshark* when troubleshooting roaming and signaling links.

---

# Lesson 2: SCTP Internals

## First Principle: What is an Association?

TCP creates a **connection**.

```text
Client ---------------- Server
        Connection
```

SCTP creates an **association**.

```text
Client ---------------- Server
        Association
```

Why a different term?

Because an SCTP association can contain:

```text
Multiple IPs
Multiple Streams
Multiple Paths
```

A TCP connection is simply:

```text
1 Source IP
1 Destination IP
1 Source Port
1 Destination Port
```

An SCTP association may be:

```text
10.1.1.1
10.1.1.2
      |
      |
      V
20.1.1.1
20.1.1.2
```

all inside one association.

---

# Association Establishment

TCP:

```text
Client                  Server

SYN -------------------->

     <---------------- SYN-ACK

ACK -------------------->
```

Problem:

The server **allocates** resources immediately.

Attack:

```text
Fake SYN
Fake SYN
Fake SYN
Fake SYN
```

Server memory fills up.

This is a [[SYN flood attack]].

---

# SCTP Handshake

SCTP uses four steps:

```text
Client                  Server

INIT -------------------->

     <--------------- INIT-ACK

COOKIE-ECHO ------------->

     <--------------- COOKIE-ACK
```

---

## Why Cookies?

The server does not immediately allocate state.

Instead:

```text
INIT
```

contains:

```text
Capabilities
Streams
Verification Tag
```

Server responds:

```text
INIT-ACK
```

with a *cryptographic* cookie.

The client must return:

```text
COOKIE-ECHO
```

Only then does the server create the association.

Benefit:

```text
Much more resistant
to resource exhaustion attacks.
```

---

# SCTP Packet Structure

TCP:

```text
TCP Header
Data
```

SCTP:

```text
Common Header
+
Chunks
```

Think of chunks as mini-messages inside the packet.

Example:

```text
+----------------+
| SCTP Header    |
+----------------+
| DATA Chunk     |
+----------------+
| DATA Chunk     |
+----------------+
| SACK Chunk     |
+----------------+
```

One SCTP packet can contain multiple chunks.

This is called:

```text
Bundling
```

---

# Important Chunk Types

## INIT

Starts an association.

```text
Client -> Server
```

---

## INIT-ACK

Returns association parameters.

```text
Server -> Client
```

---

## COOKIE-ECHO

Returns the server cookie.

```text
Client -> Server
```

---

## COOKIE-ACK

Association established.

```text
Server -> Client
```

---

## DATA

Carries user payload.

Example:

```text
M3UA
Diameter
```

messages.

---

## SACK

Selective Acknowledgment.

Equivalent to TCP ACK but more powerful.

---

## HEARTBEAT

Used to verify path health.

Critical for roaming systems.

---

## SHUTDOWN

Graceful close.

---

## ABORT

Immediate termination.

---

# Reliability

TCP uses:

```text
Sequence Number
```

SCTP uses:

```text
TSN
Transmission Sequence Number
```

---

Example

Sender:

```text
TSN 100
TSN 101
TSN 102
TSN 103
```

Receiver gets:

```text
100
101
103
```

Missing:

```text
102
```

Receiver sends:

```text
SACK
Missing TSN 102
```

Sender retransmits:

```text
TSN 102
```

---

# What is SACK?

SACK means:

```text
Selective ACK
```

Instead of:

```text
I received up to 101
```

the receiver can say:

```text
Received:
100
101
103

Missing:
102
```

This improves recovery efficiency.

---

# Multi-Streaming Deep Dive

This is one of SCTP's superpowers.

Imagine:

```text
Association
```

contains:

```text
Stream 0
Stream 1
Stream 2
```

---

Without Streams (TCP)

```text
Packet 1
Packet 2
Packet 3
```

Lose packet 2:

```text
Packet 3 blocked
```

This is:

```text
Head Of Line Blocking
```

---

With SCTP Streams

```text
Stream 0
  Packet A

Stream 1
  Packet B

Stream 2
  Packet C
```

If:

```text
Packet A lost
```

then:

```text
Packet B continues
Packet C continues
```

Only Stream 0 waits.

---

# Multi-Homing Deep Dive

Suppose:

```text
MME

10.1.1.1
10.1.1.2
```

and

```text
HSS

20.1.1.1
20.1.1.2
```

Association:

```text
Primary:
10.1.1.1 <-> 20.1.1.1

Backup:
10.1.1.2 <-> 20.1.1.2
```

---

# How Failover Works

SCTP periodically sends:

```text
HEARTBEAT
```

Example:

```text
HEARTBEAT
```

No response.

Again:

```text
HEARTBEAT
```

No response.

After a configured threshold:

```text
Path marked inactive
```

Traffic moves:

```text
Primary -> Backup
```

Association remains alive.

This behavior is one of the main reasons telecom systems achieve very high availability.

---

# SCTP State Machine

You'll often see states like:

```text
CLOSED

COOKIE-WAIT

COOKIE-ECHOED

ESTABLISHED

SHUTDOWN-PENDING

SHUTDOWN-SENT

SHUTDOWN-ACK-SENT
```

For troubleshooting, the most important state is:

```text
ESTABLISHED
```

because that's when M3UA or Diameter traffic can flow.

---

# Mapping to Mobile Roaming

When a roaming signaling link comes up:

```text
	HLR/HSS
      |
      |
    SCTP
      |
      |
	STP/MME
```

the first packets are:

```text
INIT
INIT-ACK
COOKIE-ECHO
COOKIE-ACK
```

Then:

```text
M3UA ASPUP
M3UA ASPUP ACK

M3UA ASPACTIVE
M3UA ASPACTIVE ACK
```

Then:

```text
MAP messages
```

or

```text
Diameter messages
```

depending on the network.

This layering is important:

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
```

SCTP must be established before M3UA can become active.

---

# Go Architecture (Transport Layer)

Avoid this:

```go
func HandleUpdateLocation() {
    conn.Write(...)
}
```

Business logic directly manipulating SCTP.

This couples your domain to transport.

---

Prefer:

```go
type SignalingTransport interface {
    Send([]byte) error
    Receive() ([]byte, error)
}
```

Domain layer:

```go
type RoamingService struct {
    transport SignalingTransport
}
```

Implementation:

```go
type SCTPTransport struct {
    conn *sctp.SCTPConn
}
```

Benefits:

```text
Domain independent of SCTP
Easy testing
Easy simulation
Clean Architecture
```

---

# Common Telecom Troubleshooting Cases

### INIT sent, no INIT-ACK

Usually:

```text
Firewall
Routing
Wrong IP
```

---

### COOKIE-ECHO sent, no COOKIE-ACK

Often:

```text
Cookie mismatch
Association timeout
```

---

### SCTP established but no MAP traffic

Usually:

```text
M3UA not active
```

---

### Frequent path switching

Often:

```text
Packet loss
Bad network
Heartbeat failures
```

---

# Exercise

Answer these questions:

### Question 1

Why does SCTP use:

```text
INIT
INIT-ACK
COOKIE-ECHO
COOKIE-ACK
```

instead of TCP's 3-way handshake?

---

### Question 2

What problem does multi-streaming solve?

---

### Question 3

In this stack:

```text
MAP
TCAP
SCCP
M3UA
SCTP
IP
```

which layer directly uses SCTP?

---

### Question 4

If the primary path fails, does the SCTP association necessarily need to be re-established?

---
# Q1 Review
A slightly more complete answer:

```
INIT    ↓Server generates cookie    ↓No association state stored yet    ↓Client proves it received cookie    ↓Server creates association
```

The key principle is:

```
Don't trust the client until it provesit can receive packets at its claimed address.
```

This makes SCTP more resistant to resource exhaustion attacks than classic TCP.


# Q2 Review
```
Packet loss in one streamdoes not block deliveryin other streams.
```

Important distinction:

Many beginners incorrectly think:

```
Packet loss anywhere=No blocking at all
```

Not true.

Example:

```
Association├─ Stream 0├─ Stream 1└─ Stream 2
```

If Stream 0 loses TSN 100:

```
Stream 0 waits
```

But:

```
Stream 1 continuesStream 2 continues
```

Only cross-stream blocking is removed.

---

# Q3 Review

The question was:

```
MAP
TCAP
SCCP
M3UA
SCTP
IP
```

Which layer directly uses SCTP?

Correct answer:

```
M3UA
```

Because:

```
MAP 
↓
TCAP 
↓
SCCP 
↓
M3UA 
↓
SCTP
```

M3UA is the SCTP user.

Think of it like:

```
HTTP uses TCP
M3UA uses SCTP
```

The relationship is:

```
Application Layer        
↓      
M3UA        
↓      
SCTP
```

This distinction becomes extremely important when troubleshooting roaming systems.

---

# Q4 Review

Your answer:

> NO if heartbeats doesn't response use backup path

✅ Correct.

More complete version:

```
Primary Path      
↓
Heartbeat failure      
↓
Path marked inactive      
↓
Traffic moves to backup path      
↓
Association remains established
```

This is one of the biggest reasons SCTP became popular in telecom.