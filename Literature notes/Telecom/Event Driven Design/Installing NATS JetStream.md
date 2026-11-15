---
Created Date: 2026-06-28
tags:
  - telecom
  - golang
  - NATS
Next: "[[Building the Broker Package]]"
---
---
# Session 2 — Installing NATS JetStream

## Goal

By the end of this session you will have:

- A NATS server running
- JetStream enabled
- Data persisted
- Monitoring enabled
- A Go project connected to NATS

---

# Why Docker?

Never develop directly against a manually installed server.

With Docker you get:

- Easy upgrades
- Easy cleanup
- Easy CI/CD
- Same environment for everyone

---

# Project Layout

Let's create a new project.

```
appointment-system/

├── docker-compose.yml
├── .env
├── Makefile
├── proto/
├── cmd/
├── internal/
└── scripts/
```

---

# docker-compose.yml

```yaml
version: "3.9"

services:

  nats:
    image: nats:2.11

    container_name: nats

    ports:
      - "4222:4222"
      - "8222:8222"

    command:
      - "-js"
      - "-sd"
      - "/data"

    volumes:
      - ./data/nats:/data

    restart: unless-stopped
```

Run it:

```bash
docker compose up -d
```

---

## Verify

```bash
docker ps
```

Expected:

```
CONTAINER ID

nats

Up
```

---

# Test

Install the NATS CLI.

## Linux

```bash
curl -sf https://binaries.nats.dev/nats-io/natscli/nats@latest | sh
```

Move it:

```bash
sudo mv nats /usr/local/bin/
```

Verify:

```bash
nats --version
```

---

# Check Server

```bash
nats server check
```

Expected:

```
OK
```

---

# Server Info

```bash
nats server report jetstream
```

Initially you'll see:

```
Streams

0

Consumers

0
```

---

# Monitoring

Open:

```
http://localhost:8222
```

Useful endpoints:

```
/varz

/jsz

/connz

/routez

/subsz
```

For example:

```
http://localhost:8222/jsz
```

returns JetStream statistics in JSON.

---

# Understanding the Ports

```
4222
```

Client connections.

Your Go application connects here.

---

```
8222
```

HTTP monitoring endpoint.

Never expose it publicly without proper access control.

---

# Create a Stream

We need a stream before storing messages.

```
nats stream add APPOINTMENT
```

The CLI asks questions.

Answer like this:

```
Subjects

appointment.>
```

Storage

```
File
```

Retention

```
Limits
```

Discard

```
Old
```

Max Age

```
0
```

Unlimited.

Replication

```
1
```

Development only.

---

Verify:

```
nats stream ls
```

Expected:

```
APPOINTMENT
```

---

# Stream Info

```
nats stream info APPOINTMENT
```

Initially:

```
Messages

0

Consumers

0
```

---

# Publish a Test Message

```
nats pub appointment.created "hello"
```

Now:

```
nats stream info APPOINTMENT
```

```
Messages

1
```

The message is persisted.

---

# Read Messages

Create a consumer:

```
nats consumer add APPOINTMENT worker
```

Choose:

```
Pull Consumer
```

Then consume:

```
nats consumer next APPOINTMENT worker
```

Output:

```
hello
```

---

# Our Future Subjects

We'll use a clear naming scheme.

```
appointment.created

appointment.updated

appointment.cancelled

appointment.completed

sms.send

sms.sent

sms.failed

telecom.location.update

telecom.location.updated

telecom.hlr.query

telecom.hlr.response
```

---

# Stream Strategy

Instead of putting everything into one stream:

```
ALL_EVENTS
```

I recommend separating domains:

```
APPOINTMENT
```

Subjects:

```
appointment.>
```

---

```
SMS
```

Subjects:

```
sms.>
```

---

```
TELECOM
```

Subjects:

```
telecom.>
```

Benefits:

- Easier permissions
- Better retention policies
- Easier monitoring
- Independent scaling

---

# Production Configuration

For production, don't use the minimal `-js` command. Use a configuration file.

Example:

```hcl
server_name: appointment-prod

jetstream {

    store_dir: "/data"

    max_mem_store: 8GB

    max_file_store: 200GB
}

http: 8222

port: 4222

pid_file: "/var/run/nats.pid"
```

Later we'll also add:

- Authentication
- TLS
- Clustering
- Leaf nodes
- Monitoring
- Prometheus metrics

---

# Before Writing Go Code

Many developers immediately start writing publishers and subscribers. That often leads to tightly coupled code.

Instead, we'll first design a small abstraction layer.

We want our application code to look like this:

```go
event := events.NewSMSSend(phone, text)

broker.Publish(ctx, event)
```

or

```go
broker.Subscribe("sms.send", smsHandler)
```

Notice that the business logic doesn't know anything about:

- NATS
- JetStream
- Subjects
- Serialization
- Acknowledgments

Only the broker package deals with messaging. This separation makes it much easier to test and maintain.

---

## Assignment

Before the next session, set up the following:

1. Run the NATS container with JetStream enabled.
2. Install the `nats` CLI.
3. Create three streams:
    - `APPOINTMENT` → `appointment.>`
    - `SMS` → `sms.>`
    - `TELECOM` → `telecom.>`
4. Publish a few test messages with the CLI.
5. Verify they are stored using `nats stream info`.
