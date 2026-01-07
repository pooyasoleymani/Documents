
**advanced multi-language C++ ecosystem**, the kind used in telecom, data pipelines, plugin engines, micro-kernel architectures, and DevOps-heavy environments.

🚀 **Advanced CMake Study + Build Plan (21 Days)**


#### Final Monorepo Structure

```
NebulaEngine/
│
├── cmake/                      # CMake modules, scripts, codegen configs
├── scripts/                    # Python + shell scripts
│   ├── codegen/
│   ├── linters/
│   ├── build/
│   └── packaging/
│
├── engine/                     # Core C++ modules
│   ├── core/                   # Core static lib
│   ├── runtime/                # App runtime executable
│   ├── plugins/                # Loadable plugins
│   │   ├── plugin_a/
│   │   └── plugin_b/
│   ├── interfaces/             # Shared interface headers
│   └── utils/
│
├── bindings/                   # Python bindings
│   ├── pynebula/
│   └── CMakeLists.txt
│
├── tests/                      # C++ + Python tests
├── third_party/                # Conan or vcpkg dependencies (optional)
│
├── CMakeLists.txt              # root
├── CMakePresets.json          
└── pyproject.toml              # For Python CLI tools

```

---


### 🟦 DAY 1: Create Project Structure

Today you will create the **root project**, **core library**, **runtime executable**, and learn **proper target-based CMake**.


```
NebulaEngine/
│
├── engine/
│   ├── core/
│   │   ├── include/
│   │   │   └── nebula/
│   │   │       └── core.hpp
│   │   └── src/
│   │       └── core.cpp
│   │   └── CMakeLists.txt
│   │
│   ├── runtime/
│   │   ├── src/
│   │   │   └── main.cpp
│   │   └── CMakeLists.txt
│   │
│   └── CMakeLists.txt
│
├── cmake/
│   └── Modules/   # will contain helpers later
│
└── CMakeLists.txt   # root

```


#### 🟦 Root `CMakeLists.txt`


create **NebulaEngine/CMakeLists.txt**:
[[Commands.canvas|Commands]]

```cmake
cmake_minimum_required(VERSION 3.27)

project(NebulaEngine
    VERSION 0.1.0
    LANGUAGES CXX
)

# --- Global settings ---
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Better warnings (cross-platform)
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Enable folders in IDEs
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Add engine modules
add_subdirectory(engine)

```


#### 🟦 engine/CMakeLists.txt

```cmake

add_subdirectory(core)
add_subdirectory(runtime)

```


#### 🟦 **DAY 1 — Core Library (`engine/core/CMakeLists.txt`)**

```cmake

add_library(nebula_core STATIC
    src/core.cpp
)

target_include_directories(nebula_core
    PUBLIC
        include
)

# Enable PCH for core library
target_precompile_headers(nebula_core
    PUBLIC
        include/nebula/core.hpp
)


```

#### 🟩 **DAY 1 — Core Header (`core/include/nebula/core.hpp`)**


```c++

#include "nebula/core.hpp"
#include <iostream>

int main() {
    nebula::Core core;

    std::cout << "Runtime started\n";
    std::cout << "Core version: " << core.version() << "\n";

    return 0;
}

```


#### 🚀 **DAY 1 — Build the Project**

```sh
cmake -B build -S .
cmake --build build -j

```

```sh
./build/engine/runtime/nebula_runtime

```

```yaml
Runtime started
Core version: Nebula Core 0.1.0

```


#### # 🧪 **DAY 1 Verification**

Please send me:

✔ Your folder tree  
✔ Build output log  
✔ Runtime output

---

