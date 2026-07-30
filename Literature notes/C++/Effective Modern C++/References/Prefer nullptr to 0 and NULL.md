---
Created Date: 2026-01-20
tags:
  - cpp
  - programming
Next: "[[Prefer alias declarations to typedefs]]"
---
---

- Passing 0 or **NULL** to such **overloads** never called a **pointer overload**:
```c++
void f(int);
void f(bool);
void f(void*);

f(0); // call f(int) not f(void*)
f(NULL) // might not compile, but typically calls f(int). Never calls f(void*)
```



### What is nullptr?
**nullptr**’s advantage is that it *doesn’t have an integral type*. To be honest, it doesn’t have a pointer type, either, but you can think of it as a pointer of all types. nullptr’s actual type is **std::nullptr_t**, and, in a wonderfully circular definition, **std::nullptr_t** is defined to be the type of **nullptr**. The type **std::nullptr_t** implicitly converts to all *raw pointer* types, and that’s what makes **nullptr** act as if it were a pointer of *all types*.
```c++
f(nullptr) // call f(void*) overload
```


>**nullptr**’s advantage is that it doesn’t have an **integral type**.


- **nullptr** shines especially brightly when **templates** enter the picture:

```c++
int f1(std::shared_ptr<Widget> spw); // call these only when
double f2(std::unique_ptr<Widget> upw); // the appropriate
bool f3(Widget* pw); // mutex is locked

std::mutex f1m, f2m, f3m; // mutexes for f1, f2, and f3

using MuxGuard = // C++11 typedef; see Item 9
std::lock_guard<std::mutex>;
{

MuxGuard g(f1m); // lock mutex for f1
auto result = f1(0); // pass 0 as null ptr to f1
} // unlock mutex
 ...
{
MuxGuard g(f2m); // lock mutex for f2
auto result = f2(NULL); // pass NULL as null ptr to f2
} // unlock mutex
 ...
{
MuxGuard g(f3m); // lock mutex for f3
auto result = f3(nullptr); // pass nullptr as null ptr to f3
} // unlock mutex


/**
* The failure to use nullptr in the first two calls in this code is sad, but the 
* code works, and that counts for something.
* let’s templatize the pattern:
*/
template<typename FuncType , typename MutexType, typename PtrType>
auto LockAndCall(FuncType func, MutexType& mutex, PtrType ptr) -> decltype(func(ptr))
{
	MuXGuard g(mutex);
	retrn func(ptr);
}

// Given the LockAndCall template (either version), callers can write code like 
// this:

auto result1 = LockAndCall(f1, f1m, 0); // error!
auto result1 = LockAndCall(f1, f1m, NULL); // error!
auto result1 = LockAndCall(f1, f1m, nullptr); // fine
```

---


>[!IMPORTANT] **Things to Remember**
>• Prefer **nullptr** to 0 and NULL.
• Avoid **overloading** on **integral** and **pointer** types.
