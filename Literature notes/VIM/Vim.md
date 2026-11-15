---
Created Date: 2026-06-24
tags:
  - vim
---
---
As your mentor, I'd first challenge one assumption:

> Don't spend weeks customizing Vim before becoming productive.

Many developers fall into the "editor optimization trap"—they spend 20 hours tweaking Vim and save 5 minutes per week. Since you're learning **C++, Go, Linux, networking, SCTP, databases, and system programming**, focus on a setup that makes you productive immediately.

My recommendation:

1. Learn Vim motions deeply.
2. Learn tmux deeply.
3. Add only essential plugins.
4. Learn debugger integration.
5. Customize gradually.    

---

# 1. Vim Setup for Professional Development

For modern development I recommend:

- Neovim instead of Vim
    
- tmux
- LSP
- Treesitter
- Telescope    
- Git integration
    
Minimal plugin set:

| Plugin         | Purpose               |
| -------------- | --------------------- |
| lazy.nvim      | plugin manager        |
| nvim-lspconfig | Language Server       |
| nvim-cmp       | Autocomplete          |
| Treesitter     | Better syntax parsing |
| Telescope      | File finder           |
| gitsigns       | Git changes           |
| which-key      | Show shortcuts        |
| vim-fugitive   | Git commands          |

For Go:

- gopls
    
- delve
    

For C++:

- clangd
    
- codelldb
    

For Python:

- pyright
    
- debugpy
    

---

# 2. Most Important Vim Shortcuts

Forget 500 shortcuts.

Master these first.

## Navigation

### Word movement

```vim
w
```

next word

```vim
b
```

previous word

```vim
e
```

end of word

---

### Line movement

```vim
0
```

beginning

```vim
^
```

first non-space

```vim
$
```

end of line

---

### File movement

```vim
gg
```

top

```vim
G
```

bottom

```vim
50G
```

line 50

---

## Editing

Delete word

```vim
dw
```

Delete line

```vim
dd
```

Delete until end

```vim
D
```

Copy line

```vim
yy
```

Paste

```vim
p
```

Paste before

```vim
P
```

Undo

```vim
u
```

Redo

```vim
Ctrl+r
```

---

## Search

```vim
/text
```

search

```vim
n
```

next

```vim
N
```

previous

---

## Replace

Current line:

```vim
:s/foo/bar/g
```

Whole file:

```vim
:%s/foo/bar/g
```

Confirm:

```vim
:%s/foo/bar/gc
```

---

## Visual Mode

Character:

```vim
v
```

Line:

```vim
V
```

Block:

```vim
Ctrl+v
```

Block mode is extremely useful.

Example:

```go
a := 1
a := 2
a := 3
```

Use:

```vim
Ctrl+v
Shift+i
```

Edit all lines simultaneously.

---

## The 10 motions professionals use daily

```vim
w
b
0
$
gg
G
dd
yy
p
u
```

Master these before learning anything else.

---

# 3. Vim Features You Should Learn Next

## Text Objects

Delete inside quotes:

```vim
di"
```

Delete inside brackets:

```vim
di(
```

Delete inside block:

```vim
di{
```

Change inside quotes:

```vim
ci"
```

Change inside function:

```vim
ci{
```

These are productivity multipliers.

---

## Jump Back

```vim
Ctrl+o
```

Go back.

```vim
Ctrl+i
```

Go forward.

Very useful when navigating large Go projects.

---

## Multiple Files

```vim
:bn
```

next buffer

```vim
:bp
```

previous

```vim
:ls
```

list buffers

---

# 4. Debugging

Most beginners print logs everywhere.

Professional workflow:

## Go

Debugger:

```bash
dlv
```

Install:

```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

Debug:

```bash
dlv debug
```

Commands:

```text
b main.main
c
n
s
p variable
bt
```

Meaning:

```text
b  breakpoint
c  continue
n  next
s  step into
bt stack trace
```

---

## C++

Use:

```bash
gdb
```

or

```bash
lldb
```

Compile:

```bash
g++ -g main.cpp
```

Debug:

```bash
gdb ./a.out
```

Commands:

```text
break
run
next
step
print
backtrace
```

---

## Python

```bash
python -m pdb app.py
```

or

```python
breakpoint()
```

inside code.

---

# 5. Tmux (Most Important Skill After Vim)

Many senior Linux developers spend more time in tmux than in Vim.

Think of tmux as:

```text
One SSH Session
 ├─ Vim
 ├─ Logs
 ├─ Database
 ├─ Tests
 ├─ Build Output
 └─ Monitoring
```

all inside one terminal.

---

## Basic Structure

```text
Server
 └ Session
    └ Window
       └ Pane
```

---

# Essential Commands

Prefix:

```text
Ctrl+b
```

---

## New Window

```text
Ctrl+b c
```

---

## Next Window

```text
Ctrl+b n
```

---

## Previous Window

```text
Ctrl+b p
```

---

## Rename Window

```text
Ctrl+b ,
```

---

## Split Vertical

```text
Ctrl+b %
```

---

## Split Horizontal

```text
Ctrl+b "
```

---

## Move Between Panes

```text
Ctrl+b arrow
```

---

## Kill Pane

```text
Ctrl+b x
```

---

# Professional Go Workflow

Window 1

```text
vim
```

Window 2

```text
go test ./...
```

Window 3

```text
air
```

(live reload)

Window 4

```text
tail -f app.log
```

Window 5

```text
psql
```

or

```text
mysql
```

---

# Tmux Best Practices

## Enable mouse

```tmux
set -g mouse on
```

---

## Vim-like pane movement

```tmux
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
```

---

## Use session per project

Example:

```bash
tmux new -s telecom
```

```bash
tmux new -s golang
```

```bash
tmux new -s cpp
```

---

## Detach

```text
Ctrl+b d
```

Session keeps running.

---

## Reattach

```bash
tmux attach -t telecom
```
---

# If I were mentoring you for the next 6 months

I would make you learn in this order:

1. Linux shell
    
2. tmux
    
3. Vim motions
    
4. Git
    
5. Go debugging (dlv)
    
6. GDB/LLDB
    
7. LSP + Treesitter
    
8. Advanced Vim text objects
    
9. Macros
    
10. Custom plugins
    

Most developers try to learn #10 first. The biggest productivity gains actually come from #2, #3, and #5.

For your current work (Go backend, Linux, SCTP, telecom protocols), becoming excellent at **tmux + Vim motions + Delve + GDB** will give you far more value than any fancy Vim theme or plugin.