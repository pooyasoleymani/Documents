---
tags:
  - build-tools
---
---
When Software or Program have dependency to several shared packages that not incompatible.

## Problems
Dependency hell takes several forms:
1. **Many dependencies**: application depend on many libraries
2. **Long chain of dependencies**: app depend on liba, and liba depend on libb and ... depend on libz
3. **Conflicting dependencies**:if app1 depend on libfoo 1.2 and app2 depend on libfoo 2.0 we can't install both of this library simultaneous.
4. **Circular dependencies**:  when application A depend on specific version of application B and application B depend on specific version of A 
5. **Packet manager dependencies**: it possible dependency hell to result from installing a prepared package via a packet manager . 
6.  **Diamond dependencies**: When library A depend on B, C, and D and and B need D.1 and C need D.2 


## Solution
1. **Removing dependencies**: 
2. **Version numbering**
3. **Private per application versions**
4. **Side-by-side installation of multiple versions**
5. **Smart package management**
6. **Installer options**
7. **Easy adaptability in programming**
8. **Strict compatibility requirement in code development and maintenance**
9. **Software appliances**
10. **Portable applications**

See also: [[Packet manager]], [[code refactoring]], [[Circular dependency]], [[Software appliance]],[[Configuration management]],[[Coupling]]