---
tags:
  - "#inbox"
---
---
Static is member of class (variable , function) that only one shared copy of this member exist for all object of this class it declared inside a class with the _static_ keyword.

## Key Points
1. Single Copy
2. Definition Outside Class 
3. Access Without Object
4. Lifetime: Exist for entire program duration
5. Access Control: public, private, protected

## Use Case
1. Tracking Object Count
2. Global Configuration
3. Shared Resources
4. Singleton Pattern
5. Global Counters

## Example

```cpp
class Config {
public:
   static inline int maxUsers = 100; // Inline definition
};
```