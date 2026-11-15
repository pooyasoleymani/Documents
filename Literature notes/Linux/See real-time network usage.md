---
Created Date: 2026-06-17
tags:
  - linux
---
---

### **`nload` (simple & visual)**

```bash
sudo apt install nload
nload
```

- Shows incoming/outgoing traffic in real time
    
- Very simple interface
    

---

### **`bmon` (more detailed graphs)**

```bash
sudo apt install bmon
bmon
```

- Shows bandwidth per interface
    
- Has nice terminal graphs
    

---

## 2. See which apps are using the network

### **`nethogs` (VERY useful)**

```bash
sudo apt install nethogs
sudo nethogs
```

- Shows per-process usage
    
- Example: Chrome, Firefox, curl, etc.
    
- Great for finding “who is downloading”
    

---

## 3. See active connections (who is connected to what)

### **`ss` (built-in, powerful)**

```bash
ss -tupn
```

- Shows TCP/UDP connections
    
- Shows process ID and program using it
    

Example:

```bash
ss -tupn | grep ESTAB
```

---

## 4. Monitor traffic per interface over time

### **`vnstat` (history-based)**

```bash
sudo apt install vnstat
vnstat
```

Live mode:

```bash
vnstat -l
```

- Tracks daily/monthly usage
    
- Good for “how much data I used”
    

---

## 5. Deep packet inspection (advanced)

### **`iftop` (like top but for network)**

```bash
sudo apt install iftop
sudo iftop
```

- Shows which IPs you are talking to in real time
    

---

### **`tcpdump` (very advanced)**

```bash
sudo tcpdump -i any
```

- Captures raw network packets
    
- Useful for debugging or analysis
    

---

## 6. GUI option (easiest visual)

### Wireshark

```bash
sudo apt install wireshark
```

- Full graphical packet analyzer
    
- Best for deep inspection
    

---

## Recommended setup for you

If you just want “who is downloading what”:

```bash
sudo apt install nethogs nload iftop
```

Then use:

- `nethogs` → per app usage
- `nload` → total speed
- `iftop` → network connections
