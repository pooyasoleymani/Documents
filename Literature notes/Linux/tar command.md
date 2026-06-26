---
Created Date: 2026-06-15
tags:
  - linux
---
---
# Linux `tar` Command — Summary & Best Practices

`tar` (Tape Archive) is the standard Linux tool for creating, extracting, compressing, and managing archive files.

---

# Basic Syntax

```bash
tar [OPTIONS] ARCHIVE FILES...
```

Examples:

```bash
tar -cf backup.tar mydir/
tar -xf backup.tar
```

---

# Most Common Options

| Option                 | Meaning                                        |
| ---------------------- | ---------------------------------------------- |
| `-c`                   | Create archive                                 |
| `-x`                   | Extract archive                                |
| `-f`                   | Archive filename                               |
| `-t`                   | List contents                                  |
| `-v`                   | Verbose output                                 |
| `-z`                   | Use gzip (`.tar.gz`)                           |
| `-j`                   | Use bzip2 (`.tar.bz2`)                         |
| `-J`                   | Use xz (`.tar.xz`)                             |
| `--zstd`               | Use zstd (`.tar.zst`)                          |
| `-C`                   | Change directory before operation              |
| `--exclude`            | Skip files/directories                         |
| `--strip-components=N` | Remove leading path components when extracting |

---

# Create Archives

## Plain tar

```bash
tar -cf backup.tar project/
```

---

## Gzip Compression

Most common.

```bash
tar -czf backup.tar.gz project/
```

---

## XZ Compression

Smaller size, slower.

```bash
tar -cJf backup.tar.xz project/
```

---

## `ZSTD` Compression

Modern choice.

```bash
tar --zstd -cf backup.tar.zst project/
```

---

# Extract Archives

## Extract in Current Directory

```bash
tar -xf backup.tar
```

---

## Extract Gzip Archive

```bash
tar -xzf backup.tar.gz
```

---

## Extract to Specific Directory

```bash
tar -xf backup.tar -C /tmp/output
```

---

# List Archive Contents

```bash
tar -tf backup.tar
```

Verbose:

```bash
tar -tvf backup.tar
```

---

# Add Files

Technically possible:

```bash
tar -rf backup.tar newfile.txt
```

But:

- Works only on uncompressed archives.
    
- Rarely used in production.
    

---

# Extract Single File

```bash
tar -xf backup.tar path/to/file.txt
```

---

# Exclude Files

```bash
tar -czf backup.tar.gz project \
    --exclude="*.log" \
    --exclude="tmp/"
```

---

# Remove Leading Directories

Archive:

```
project/src/main.go
```

Extract only:

```
src/main.go
```

```bash
tar -xf backup.tar --strip-components=1
```

---

# View Archive Size

```bash
tar -tvf backup.tar
```

Or:

```bash
du -sh backup.tar
```

---

# Useful Real-World Examples

## Backup Application

```bash
tar -czf app-$(date +%F).tar.gz app/
```

Example:

```bash
app-2026-06-15.tar.gz
```

---

## Backup and Exclude Logs

```bash
tar -czf backup.tar.gz \
    --exclude=logs \
    --exclude=*.tmp \
    project/
```

---

## Backup Multiple Directories

```bash
tar -czf backup.tar.gz \
    app/ \
    config/ \
    scripts/
```

---

## Archive Contents Without Parent Directory

Instead of:

```
project/
 ├── main.go
```

Do:

```bash
tar -czf project.tar.gz -C project .
```

Result:

```
main.go
```

not

```
project/main.go
```

---

# Best Practices

## 1. Always Use Explicit Compression

Prefer:

```bash
tar -czf backup.tar.gz data/
```

or

```bash
tar --zstd -cf backup.tar.zst data/
```

instead of uncompressed archives.

---

## 2. Verify Before Extracting

List contents first:

```bash
tar -tf archive.tar.gz
```

Useful when downloading archives from the internet.

---

## 3. Extract Into a Dedicated Directory

Avoid polluting current directory:

```bash
mkdir extract
tar -xf archive.tar.gz -C extract
```

---

## 4. Use `-C` Instead of Complex Paths

Bad:

```bash
tar -czf backup.tar.gz /opt/app/config
```

Better:

```bash
tar -czf backup.tar.gz -C /opt/app config
```

Produces cleaner archives.

---

## 5. Preserve Permissions

Tar preserves:

- file permissions
    
- ownership (when possible)
    
- timestamps
    

For system backups:

```bash
sudo tar -czpf backup.tar.gz /etc
```

`-p` preserves permissions during extraction.

---

## 6. Protect Against Path Traversal

Before extracting unknown archives:

```bash
tar -tf suspicious.tar
```

Look for entries like:

```text
../../etc/passwd
```

Never blindly extract archives from untrusted sources.

---

## 7. Use ZSTD for Large Backups

Modern Linux distributions support:

```bash
tar --zstd -cf backup.tar.zst project/
```

Advantages:

- Faster than gzip
    
- Better compression ratio
    
- Excellent for CI/CD and Docker build artifacts
    

---

## 8. Verify Archive Integrity

For gzip archives:

```bash
gzip -t backup.tar.gz
```

For tar structure:

```bash
tar -tf backup.tar.gz > /dev/null
```

---

# Compression Comparison

|Format|Extension|Speed|Size|
|---|---|---|---|
|None|`.tar`|Fastest|Largest|
|Gzip|`.tar.gz`|Fast|Good|
|Bzip2|`.tar.bz2`|Slow|Better|
|XZ|`.tar.xz`|Very Slow|Excellent|
|ZSTD|`.tar.zst`|Very Fast|Excellent|

For most modern systems:

- **General use:** `tar -czf` (gzip)
    
- **Large backups:** `tar --zstd`
    
- **Maximum compression:** `tar -cJf` (xz)
    

# Commands You'll Use Most

```bash
# Create
tar -czf backup.tar.gz folder/

# Extract
tar -xzf backup.tar.gz

# List
tar -tf backup.tar.gz

# Extract elsewhere
tar -xzf backup.tar.gz -C /tmp

# Exclude files
tar -czf backup.tar.gz folder --exclude="*.log"

# Modern compression
tar --zstd -cf backup.tar.zst folder/
```

If you're working as a Go/Linux backend developer, the 90% commands are:

```bash
tar -czf app.tar.gz app/
tar -xzf app.tar.gz
tar -tf app.tar.gz
tar -xzf app.tar.gz -C /opt/app
```

Master those four first.