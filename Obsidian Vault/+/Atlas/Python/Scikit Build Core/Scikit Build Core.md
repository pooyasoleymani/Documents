**Scikit-build-core** is a complete ground-up rewrite of **scikit-build** on top of *modern packaging APIs*. It provides a bridge between *CMake* and the *Python build system*, allowing you to make *Python modules* with *CMake*.



## Features 
**Scikit-build-core** is a *build backend* for *Python* that uses *CMake* to *build extension modules*. It has a simple yet powerful *static configuration system* in **pyproject.toml**, and supports almost unlimited flexibility via *CMake*.

-  Great support for or by *most OSs*, *compilers, IDEs*, and *libraries*
- Support for *C++ features* and other languages like *Fortran*
- Support for *multithreaded builds*
-  Simple *CMakeLists.txt* files instead of up to thousands of lines of fragile *setuptools/distutils* code.
- *Cross-compile* support for *Apple Silicon* and *Windows ARM*
- Better **warnings**, **errors**, and **logging**
- No **warning** about **unused variables**
- Automatically adds **Ninja** and/or **CMake** only as required
- No dependency on **setuptools**, **distutils**, or **wheel**
- Powerful *config system*, including config options support
- *Automatic* inclusion of *site-packages* in `CMAKE_PREFIX_PATH`
- **FindPython** is backported if running on *CMake < 3.26.1 (configurable),* supports PyPY SOABI & Limited *API / Stable ABI*
- Limited *API / Stable ABI* and *pythonless* tags supported via config option
- No slow generator search, *ninja/make or MSVC* used by default, respects `CMAKE_GENERATOR`
- *SDists* are reproducible by default (UNIX, Python 3.9+, uncompressed comparison recommended)
- Support for *caching* between builds (opt-in by setting `build-dir`)
- Support for writing out to *extra wheel folders* (*scripts*, *headers*, *data*)
- Support for selecting install components and build targets
- Dedicated *entrypoints* for module and prefix directories
- Several *integrated dynamic metadata plugins* (proposing standardized support soon)
- Experimental editable mode support, with optional experimental auto rebuilds on import and optional in-place mode
- Supports *WebAssembly* (Emscripten/Pyodide).
- Supports *free-threaded Python 3.13+.*

### Example 
o use *scikit-build-core*, add it to your `build-system.requires`and specify the `scikit_build_core.build` builder as your `build-system.build-backend`. You do _not_ need to specify `cmake` or `ninja`; *scikit-build-core* will require them automatically if the system versions are not sufficient.

```toml
[build-system]
requiers = ["scikit-build-core"]
build-backend = "scikit_build_core.build"

[project]
name = "scikit_build_simplest"
version = "0.0.1"
```

`CMakeLists.txt`:
```cmake
cmake_minimum_reqired(VERSION 3.15...3.30)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(Python COMPONENTS Interpereter Development.Module REQUIRED)

Python_add_library(_module MODULE stc/module.c WITH_SOABI)
install(TARGETS _module DESTINATION ${SKBUILD_PROJECT_NAME})
```





### Configuration 
All configuration options can be placed in `pyproject.toml`, passed via `-C`/`--config-setting` in build or `-C`/`--config-settings` in `pip` , or set as environment variables. `tool.scikit-build` is used in toml, `skbuild.` for `-C` options, or `SKBUILD_*` for environment variables.

```toml
[tool.scikit-build]
# The versions of CMake to allow as a python-compatible specifier.
cmake.version = ""

# A list of args to pass to CMake when configuring the project.
cmake.args = []

# A table of defines to pass to CMake when configuring the project. Additive.
cmake.define = {}

# The build type to use when building the project.
cmake.build-type = "Release"

# The source directory to use when building the project.
cmake.source-dir = "."

# Do not pass the current environment's python hints such as ``Python_EXECUTABLE``.
cmake.python-hints = true

# The versions of Ninja to allow.
ninja.version = ">=1.5"

# Use Make as a fallback if a suitable Ninja executable is not found.
ninja.make-fallback = true

# The logging level to display.
logging.level = "WARNING"

# Files to include in the SDist even if they are skipped by default. Supports gitignore syntax.
sdist.include = []

# Files to exclude from the SDist even if they are included by default. Supports gitignore syntax.
sdist.exclude = []

# Try to build a reproducible distribution.
sdist.reproducible = true

# If set to True, CMake will be run before building the SDist.
sdist.cmake = false

# A list of packages to auto-copy into the wheel.
wheel.packages = ["src/<package>", "python/<package>", "<package>"]

# The Python version tag used in the wheel file.
wheel.py-api = ""

# Fill out extra tags that are not required.
wheel.expand-macos-universal-tags = false

# The CMake install prefix relative to the platlib wheel path.
wheel.install-dir = ""

# A list of license files to include in the wheel. Supports glob patterns.
wheel.license-files = ""

# Run CMake as part of building the wheel.
wheel.cmake = true

# Target the platlib or the purelib.
wheel.platlib = ""

# A set of patterns to exclude from the wheel.
wheel.exclude = []

# The build tag to use for the wheel. If empty, no build tag is used.
wheel.build-tag = ""

# If CMake is less than this value, backport a copy of FindPython.
backport.find-python = "3.26.1"

# Select the editable mode to use. Can be "redirect" (default) or "inplace".
editable.mode = "redirect"

# Turn on verbose output for the editable mode rebuilds.
editable.verbose = true

# Rebuild the project when the package is imported.
editable.rebuild = false

# Extra args to pass directly to the builder in the build step.
build.tool-args = []

# The build targets to use when building the project.
build.targets = []

# Verbose printout when building.
build.verbose = false

# Additional ``build-system.requires``.
build.requires = []

# The components to install.
install.components = []

# Whether to strip the binaries.
install.strip = true

# The path (relative to platlib) for the file to generate.
generate[].path = ""

# The template string to use for the file.
generate[].template = ""

# The path to the template file. If empty, a template must be set.
generate[].template-path = ""

# The place to put the generated file.
generate[].location = "install"

# A message to print after a build failure.
messages.after-failure = ""

# A message to print after a successful build.
messages.after-success = ""

# Add the python build environment site_packages folder to the CMake prefix paths.
search.site-packages = true

# List dynamic metadata fields and hook locations in this table.
metadata = {}

# Strictly check all config options.
strict-config = true

# Enable early previews of features not finalized yet.
experimental = false

# If set, this will provide a method for backward compatibility.
minimum-version = "0.11"  # current version

# The CMake build directory. Defaults to a unique temporary directory.
build-dir = ""
```