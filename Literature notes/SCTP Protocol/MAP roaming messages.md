---
Created Date: 2026-06-20
tags:
  - architecture
  - SCTP
  - golang
Next: "[[Diameter over SCTP]]"
---
---
# Lesson 5: M3UA States + Failure Signals (Production Reality)

## First Principle

M3UA is not just a protocol — it is a **state machine for signaling availability**.

So instead of thinking:

```text
"Is SCTP up?"
```

you must think:

```text
"Is the M3UA Application Server ACTIVE and ROUTABLE?"
```

---

# M3UA Core State Model

There are 3 critical layers:

```text
1. SCTP State (transport)
2. ASP State (application process)
3. AS State (application server group)
```

---
## 1. SCTP State (Transport Layer)

```text
CLOSED
ESTABLISHED
```

If SCTP is down:

```text
→ Nothing works
```

If SCTP is up:

```text
→ Transport is ready
```

BUT this does NOT mean traffic flows.

---

## 2. ASP State (Application Server Process)

ASP = your signaling endpoint (HLR, STP, MME, etc.)

States:

```text
ASP-DOWN
ASP-INACTIVE
ASP-ACTIVE
```

---

### Transition Flow

```text
ASP-DOWN
   ↓
ASPUP
   ↓
ASP-INACTIVE
   ↓
ASPACTIVE
   ↓
ASP-ACTIVE
```

---
## Key Meaning

### ASPUP

```text
"I'm alive and ready to initialize"
```

### ASPACTIVE

```text
"I can now carry traffic"
```

---

# 3. AS State (Application Server Group)

This is where routing decisions happen.

States:

```text
INACTIVE
ACTIVE
PENDING
```

---

# Full Real Stack View

```text
MAP / ISUP
     ↓
SCCP
     ↓
M3UA (AS / ASP states)
     ↓
SCTP
     ↓
IP
```

---

# Critical Production Messages

Now the important part: real M3UA control messages.

---

# 1. DUNA (Destination Unavailable)

```text
Destination Unavailable
```

Meaning:

```text
The remote SS7 point code is not reachable
```

Example:

```text
HLR is DOWN → SG sends DUNA
```

---

# 2. DAVA (Destination Available)

```text
Destination Available
```

Meaning:

```text
The SS7 destination is reachable again
```

---
# 3. DAUD (Destination Audit)
Used when system wants to check:

```text
"Are you alive?"
```

---
# 4. SCON (Signaling Congestion)
This is VERY important in roaming systems.

```text
Signaling Congestion
```

Meaning:

```text
Network is overloaded, slow down traffic
```

---

# Real Roaming Failure Example

Let’s simulate a real operator issue.

---

## Scenario

Subscriber roams into visited network:

```text
VLR/MME → sends UpdateLocation → HLR
```

But it fails.

---

## Debug Flow

### Step 1: SCTP check

```text
Is SCTP up?
→ YES
```

---

### Step 2: M3UA check

```text
Is ASP ACTIVE?
→ NO
```

---

### Step 3: Why?

Logs show:

```text
ASPUP received
ASPACTIVE missing
```

---

### Root Cause

```text
Application never transitioned to ACTIVE state
```

So:

```text
SCTP UP ≠ traffic flows
M3UA ACTIVE is required
```

---

# Mental Model (VERY IMPORTANT)

Think like this:

```text
SCTP = wire
M3UA = traffic controller
SS7 = vehicles
```

Even if wire is fine:

```text
traffic may still be blocked
```

---

# Go Engineering Perspective

In production systems you should model states explicitly:

```go
type ASPState string

const (
    ASPDown     ASPState = "DOWN"
    ASPInactive ASPState = "INACTIVE"
    ASPActive   ASPState = "ACTIVE"
)
```

---

## State Machine Pattern (Best Practice)

```go
type ASP struct {
    state ASPState
}

func (a *ASP) HandleASPUP() {
    a.state = ASPInactive
}

func (a *ASP) HandleASPACTIVE() {
    a.state = ASPActive
}
```

---

## Anti-pattern (avoid this)

```go
if sctpConnected {
    sendTraffic()
}
```

❌ WRONG because SCTP alone is not enough.

---

## Correct pattern

```go
if asp.state == ASPActive {
    sendTraffic()
}
```

---

# Common Production Issues

### 1. SCTP up, no traffic

Cause:

```text
AS not ACTIVE
```

---

### 2. ASP keeps flapping

Cause:

```text
heartbeat failure / routing instability
```

---

### 3. DUNA flood

Cause:

```text
HLR unreachable or overloaded
```

---

### 4. Silent failure

Cause:

```text
AS not activated but SCTP is up
```

---

# Key Insight (VERY IMPORTANT)

```text
SCTP tells you:
    "I can talk"

M3UA tells you:
    "You are allowed to talk"
```

---

# Exercise (Real Engineer Level)

Answer these:

### Q1

If SCTP is ESTABLISHED but ASP is INACTIVE, can MAP messages flow?

---

### Q2

What does DUNA indicate in roaming systems?

---

### Q3

Why is ASPACTIVE important?

---

### Q4

What is the real difference between SCTP state and M3UA state?
