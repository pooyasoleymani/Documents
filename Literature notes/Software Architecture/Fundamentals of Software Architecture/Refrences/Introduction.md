---
Created Date: 2026-02-01
tags:
  - architecture
Next: "[[Architectural Thinking]]"
---
---
# What software architecture really is?

## The idea first (short and sharp)
*Software architecture* is **not** the code, and it’s not the *diagrams*.
It is the **set of decisions that are hard to change later** and that **shape the system’s behavior and evolution**.  
Everything else is just details orbiting those decisions.

## Core definition (from the book, unpacked)
The book defines software architecture as:

> The structure of the system, its components, their relationships, and the principles guiding its design and evolution.

Let’s translate that into plain language:
- **Structure**: how parts are arranged
- **Components**: the major building blocks (not classes)
- **Relationships**: how those blocks communicate and depend on each other    
- **Principles**: rules that *survive* refactoring and rewrites

If it can be changed in an afternoon without consequences, it’s probably _not_ architecture.

## The two laws of software architecture


### First law
Everything in *software architecture* is a *trade-off*.
