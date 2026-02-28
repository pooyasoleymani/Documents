---
Created Date: 2026-02-26
tags:
  - socket
  - OS
---
---
## What are Sockets
At its core, a **socket** is an *endpoint* for *sending* or *receiving* data across a computer *network*. Think of it as a specialized *file descriptor* or handle that the *operating system* provides to applications for *network* communication. When you establish a *network connection*, you’re essentially creating two **sockets**: one on the *client* machine and one on the *server* machine.


### Key Components of a Socket Address:
- **IP Address:** Identifies the specific device on the network.
- **Port Number:** Identifies a specific application or service running on that device. Ports range from 0 to 65535. Well-known ports (0-1023) are typically reserved for standard services (e.g., 80 for HTTP, 443 for HTTPS, 22 for SSH).