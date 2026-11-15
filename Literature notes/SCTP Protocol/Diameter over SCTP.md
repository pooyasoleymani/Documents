---
Created Date: 2026-06-20
tags:
  - architecture
  - SCTP
  - golang
Next: "[[Go implementation]]"
---
---
# Lesson 6: M3UA Control Messages & Failure Handling (Production Reality)

## First Principle

M3UA is not just “startup messages”.

It continuously controls:

```text
availability
reachability
congestion
routing state
```

So even after traffic starts, M3UA is constantly “alive”.

---

# 1. ASPDN (Application Server Process Down)

## What it means

```text
"I am shutting down gracefully"
```

Sent by ASP → SG.

---

## Flow

```text
ASP ACTIVE
   ↓
ASPDN
   ↓
ASP INACTIVE
   ↓
No traffic
```

---

## Production use case

```text
Maintenance / restart / deployment
```

---

## Important detail

Unlike SCTP:

```text
ASPDN does NOT close SCTP
```

So:

```text
Transport stays up
Signaling stops
```

---

# 2. DUNA / DAVA (Destination Control)

This is where roaming systems often break.

---

## DUNA (Destination Unavailable)

```text
"That SS7 destination is unreachable"
```

Example:

```text
HLR down → SG sends DUNA
```

---

## DAVA (Destination Available)

```text
"Destination is reachable again"
```

---

## Important propagation rule

```text
DUNA/DAVA affects routing decisions globally
```

Meaning:

```text
Not just one connection — whole SS7 route state changes
```

---

# 3. DAUD (Destination Audit)

## What it is

```text
"Are you really available?"
```

Used when:

- network recovers
- state is uncertain
- SG wants to verify routes

---

## Think of it like:

```text
health check for SS7 routing tables
```

---

# 4. SCON (Signaling Congestion)

This is EXTREMELY important in real roaming networks.

---

## Meaning

```text
Network is overloaded → slow down traffic
```

---

## Why it happens

```text
HLR / STP / SMSC overloaded
```

---

## Behavior

Instead of failing traffic:

```text
M3UA tells sender:
    reduce rate
```

---

## Analogy

```text
SCON = "traffic jam warning"
```

---

# 5. Real Roaming Failure Scenario (VERY IMPORTANT)

Let’s simulate a real operator issue.

---

## Step 1: Subscriber roams

```text
VLR/MME → UpdateLocation → HLR
```

---

## Step 2: SCTP is fine

```text
SCTP = ESTABLISHED
```

---

## Step 3: M3UA state issue

```text
ASP = INACTIVE
```

---

## Result

```text
MAP request never forwarded
```

---

## Logs you would see

```text
No ASPACTIVE received
Traffic blocked at M3UA layer
```

---

# Key Insight

```text
Most “roaming failures” are NOT SS7 failures.

They are M3UA state mismatches.
```

---

# M3UA Full State Model (IMPORTANT)

```text
SCTP:
  DOWN / UP

M3UA:
  ASP-DOWN
  ASP-INACTIVE
  ASP-ACTIVE

AS:
  INACTIVE
  ACTIVE
  PENDING
```

---

# Architecture View (Production Mental Model)

```text
MAP / ISUP
     ↓
   SCCP
     ↓
   M3UA   ← controls traffic state
     ↓
   SCTP   ← transport only
     ↓
    IP
```

---

# Go Engineering Perspective (VERY IMPORTANT)

Now we model real systems.

---

## 1. SCTP layer (dumb transport)

```go
type SCTPTransport interface {
    Send([]byte) error
    Receive() ([]byte, error)
}
```

---

## 2. M3UA state machine

```go
type ASPState string

const (
    ASPDown     ASPState = "DOWN"
    ASPInactive ASPState = "INACTIVE"
    ASPActive   ASPState = "ACTIVE"
)
```

---

## 3. Correct traffic gate

```go
func (a *ASP) CanSend() bool {
    return a.state == ASPActive
}
```

---

## Anti-pattern (VERY IMPORTANT)

```go
if sctpConnected {
    sendMAP()
}
```

❌ Wrong — causes silent production failures

---

## Correct pattern

```go
if asp.CanSend() {
    sendMAP()
}
```

---

# Troubleshooting Cheat Sheet

## Case 1: SCTP UP but no traffic

```text
Cause: ASP not ACTIVE
```

---

## Case 2: Traffic stops suddenly

```text
Cause: ASPDN or DUNA received
```

---

## Case 3: Slow signaling

```text
Cause: SCON congestion control active
```

---

## Case 4: Routing failure

```text
Cause: DUNA state in SG routing table
```

---

# Mental Model (VERY IMPORTANT)

```text
SCTP = road

M3UA = traffic controller

SS7 messages = cars
```

Even if:

```text
road is open → cars may still be blocked
```

---

# Exercise (Engineer Level)

Answer these:

### Q1

If ASPDN is received, does SCTP close?

---

### Q2

What does SCON actually control?

---

### Q3

Why can DUNA affect multiple connections?

---

### Q4

What is the most common reason for “SCTP UP but no roaming traffic”?

