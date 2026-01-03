---
IPP: ipp
tags:
  - programming
  - need-work
---
---
## 🧰 Step 1 — Download & Install oneAPI Base Toolkit
### 🪟 On **Windows**

1. Go to the official download page:  
	👉 [https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit.html)
2. Choose **“Offline Installer”** (recommended).
3. During installation, make sure **Intel® Integrated Performance Primitives (IPP)** is checked.
4. After installation, open a **“Intel oneAPI Command Prompt for Visual Studio”** (you’ll see it in Start Menu).  This sets up all compiler and environment variables for IPP automatically

### 🐧 On **Linux (Ubuntu / WSL / other distros)**

1. Download:
```bash
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18914/l_BaseKit_p_2025.0.0.100_offline.sh

```
(Version numbers may differ slightly — use the latest link from Intel’s page.)

2. Make executable & run:
```bash
chmod +x l_BaseKit_p_2025.0.0.100_offline.sh
sudo ./l_BaseKit_p_2025.0.0.100_offline.sh

```

3. When prompted, select:
    
    - ✅ “Intel® C++ Compiler (icx/icpx)”
        
    - ✅ “Intel® Integrated Performance Primitives (IPP)”
        
    - ✅ “Intel® Threading Building Blocks (TBB)” (useful later)
        
4. Add environment setup to your shell:
```bahs
source /opt/intel/oneapi/setvars.sh
```

5. Test:
```bash
echo $LD_LIBRARY_PATH
```

should show paths like `/opt/intel/oneapi/ipp/latest/lib/intel64`

## 🧩 Step 2 — Verify Installation

Check that IPP is accessible:

### On Windows (in the oneAPI Command Prompt):
```cmd
where ippcore.h

```

### On Linux

```bash
find /opt/intel/oneapi/ipp -name ippcore.h

```


## 🧮 Step 3 — “Hello IPP” Test Program

main.cpp
```cpp
#include <iostream>
#include <ippcore.h>

int main() {
    const IppLibraryVersion* ver = ippGetLibVersion();
    std::cout << "Intel IPP Version: " << ver->Version << std::endl;
    std::cout << "Name: " << ver->Name << std::endl;
    return 0;
}

```

## ⚙️ Step 4 — Build it

#### On Windows
```cmd
cl main.cpp /I"%ONEAPI_ROOT%\ipp\latest\include" /link /LIBPATH:"%ONEAPI_ROOT%\ipp\latest\lib\intel64" ippcore.lib
```

#### On Linux
```bash
icpx main.cpp -I${ONEAPI_ROOT}/ipp/latest/include -L${ONEAPI_ROOT}/ipp/latest/lib/intel64 -lippcore -o ipp_hello
./ipp_hello
```

#### output
```yml
Intel IPP Version: 2021.10 (r12345)
Name: ippcore
```


---

## Part 2: Memory Management & Data Layouts

Intel IPP functions require data that is **aligned and contiguous** in memory for [[SIMD]] acceleration.  
For that, IPP provides its own memory allocators and utility routines.


####  🧠 Key concepts

|Concept|Function|Purpose|
|---|---|---|
|Memory allocation|`ippMalloc(size)`|Allocates 32-byte aligned memory (AVX-friendly).|
|Memory free|`ippFree(ptr)`|Frees memory allocated with `ippMalloc`.|
|Set / Copy|`ippsSet_32f(value, pDst, len)`|Fills a float array with a constant.|
|Vector add|`ippsAdd_32f(a, b, dst, len)`|Adds two float arrays.|

#### 🧪 Mini Hands-On: Vector Addition Benchmark
1. Allocates three aligned float arrays (`a`, `b`, `c`)
2. Fills them with values
3. Adds them using IPP and compares to plain C++

🧱 Code: `ipp_vector_add.cpp`

```C++
#include <iostream>
#include <chrono>
#include <ipp.h>

int main() {
    const int N = 10'000'000;

    // --- Allocate aligned memory for IPP ---
    Ipp32f* a = ippsMalloc_32f(N);
    Ipp32f* b = ippsMalloc_32f(N);
    Ipp32f* c = ippsMalloc_32f(N);

    // --- Initialize vectors ---
    ippsSet_32f(1.0f, a, N);
    ippsSet_32f(2.0f, b, N);

    // --- Time IPP addition ---
    auto t1 = std::chrono::high_resolution_clock::now();
    ippsAdd_32f(a, b, c, N);
    auto t2 = std::chrono::high_resolution_clock::now();

    std::cout << "IPP Add first 5: ";
    for (int i = 0; i < 5; i++) std::cout << c[i] << " ";
    std::cout << "\nIPP time: "
              << std::chrono::duration<double, std::milli>(t2 - t1).count()
              << " ms\n";

    // --- Compare to plain C++ ---
    auto t3 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i)
        c[i] = a[i] + b[i];
    auto t4 = std::chrono::high_resolution_clock::now();

    std::cout << "C++ time: "
              << std::chrono::duration<double, std::milli>(t4 - t3).count()
              << " ms\n";

    ippFree(a);
    ippFree(b);
    ippFree(c);
}
```

## 📘 You Just Learned

✅ How to use **`ippMalloc`** and **`ippFree`**  
✅ How to fill arrays efficiently with **`ippsSet_32f`**  
✅ How to perform **vectorized arithmetic** (`ippsAdd_32f`)  
✅ How to benchmark and compare IPP vs plain C++

---

## Part 3: First Signal Processing Exercise (RMS computation)



---
Reference: ... 