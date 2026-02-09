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
4. **Circular dependencies**: 
5. Packet manager dependencies
6.  Diamond dependencies


## Solution



See also: [[Packet manager]], [[code refactoring]], 