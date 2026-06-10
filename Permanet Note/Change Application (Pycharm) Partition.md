---
Created Date: 2026-06-08
tags:
  - linux
---
---
# Change Application (Pycharm) Partition
If by "change location of PyCharm" you mean moving PyCharm and its files from your `SSD` to another partition (`/dev/sda4`), there are several possibilities depending on what you want to move:

### 1. Check where `/dev/sda4` is mounted

First, verify the mount point:

```bash
lsblk -f
```

Example output:

```text
sda
├─sda1
├─sda2
├─sda3
└─sda4 ext4  data-partition  /mnt/data
```

In this example, `/dev/sda4` is mounted at `/mnt/data`.

---

### 2. Move PyCharm Projects (Recommended)

Usually, the largest files are your projects, virtual environments, caches, and datasets.

Create a directory on `sda4`:

```bash
mkdir -p /mnt/data/projects
```

Move your projects:

```bash
mv ~/Projects/* /mnt/data/projects/
```

Then open the projects from the new location in PyCharm.

---

### 3. Move PyCharm Configuration and Cache

PyCharm stores a lot of data in your home directory.

Check sizes:

```bash
du -sh ~/.cache/JetBrains
du -sh ~/.config/JetBrains
du -sh ~/.local/share/JetBrains
```

Move them:

```bash
mv ~/.cache/JetBrains /mnt/data/JetBrains-cache
mv ~/.config/JetBrains /mnt/data/JetBrains-config
mv ~/.local/share/JetBrains /mnt/data/JetBrains-share
```

Create symbolic links:

```bash
ln -s /mnt/data/JetBrains-cache ~/.cache/JetBrains
ln -s /mnt/data/JetBrains-config ~/.config/JetBrains
ln -s /mnt/data/JetBrains-share ~/.local/share/JetBrains
```

PyCharm will continue to work normally, but the files will reside on `sda4`.

---

### 4. Move Python Virtual Environments

Virtual environments often consume several gigabytes.

Create a directory:

```bash
mkdir -p /mnt/data/venvs
```

Move existing venvs:

```bash
mv ~/venvs/* /mnt/data/venvs/
```

Or create new ones directly there:

```bash
python -m venv /mnt/data/venvs/myproject
```

Then configure the interpreter in PyCharm.

---

### 5. Move the Entire PyCharm Installation

If you installed the tarball version:

```bash
mv ~/pycharm-community-* /mnt/data/
```

or

```bash
mv ~/pycharm-professional-* /mnt/data/
```

Then start it from the new location:

```bash
/mnt/data/pycharm-community-*/bin/pycharm.sh
```

---

### 6. If Installed via Snap

Check:

```bash
snap list | grep pycharm
```

Snap applications keep data under:

```bash
~/snap/pycharm-community/
```

or

```bash
~/snap/pycharm-professional/
```

These can also be moved to `sda4` using symbolic links, similar to the cache/config directories above.

---

Can you show me the output of:

```bash
lsblk -f
df -h
```

and tell me **how PyCharm was installed** (Snap, Toolbox, apt, or tar.gz)? Then I can give exact commands for your setup.