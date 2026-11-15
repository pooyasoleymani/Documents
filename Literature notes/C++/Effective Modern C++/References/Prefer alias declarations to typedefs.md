---
Created Date: 2026-01-21
tags:
  - cpp
  - programming
Next: "[[Prefer scoped enums to unscoped enums]]"
---
---

- Given that the **typedef** and the **alias** declaration do exactly the same thing:
```cpp
typedef std::unique_ptr<std::unordered_map<std::string, std::string>> UPtrMapSS;

using UPtrMapSS = std::unique_ptr<std::unordered_map<std::string, std::string>>;
```



- **alias** declaration easier to swallow when dealing with types involving **function** **pointers**:
```cpp
// FP is a synonym for a pointer to a function taking an int and
// a const std::string& and returning nothing
typedef void (*FP)(int,const std::string&);

// same meaning a above 
using FP = void (*)(int, const std::string&);
```


- **typedef** templatized vs **alias** templatized :
```cpp
template<typename T>
using MyAllocList = std::list<T, MyAlloc<T>>;

MyAllocList<Widget> lw; // client code 

template<typename T>
struct MyAllocList {
	typedef std::list<T, MyAlloc<T>> type;
};

MyAllocList<Widget>::type lw; // client code

```



- If you want to use the **typedef** inside a **template** for the purpose of creating a linked list holding objects of a type specified by a **template** parameter, you have to precede the **typedef** name with **typename**:
```cpp
template<typename T>
class Widget {
	private:
		typename MyAllocList<T>::type list;
}
```


>[!NOTE] **dependent type**
>`MyAllocList<T>::type` refers to a type that’s dependent on a **template** **type**
>parameter **(T)**. `MyAllocList<T>::type` is thus a dependent type, and one of C++’s
many endearing rules is that the names of dependent types must be preceded by type
name.



- If MyAllocList is defined as an **alias** **template**, this need for **typename** vanishes (as does the cumbersome **“::type”** suffix):
```cpp
template<typename T>
using MyAllocList = std::list<T, MyAlloc<T>>; // as before

template<typename T>
class Widget {
private:
MyAllocList<T> list; // no "typename" no "::type"
...
};
```



>[!NOTE] **non-dependent type**
>When compilers process the Widget template and
encounter the use of `MyAllocList<T>` (i.e., use of the **alias template**), they know that`MyAllocList<T>` is the name of a type, because MyAllocList is an **alias template**: it
must name a **type**.` MyAllocList<T>` is thus a **non-dependent type**, and a **typename**
specifier is neither required nor permitted.



- There might be a **specialization** of **MyAllocList** that they haven’t yet seen where `MyAllocList<T>::type` refers to something *other* *than* *a* *type*:
```cpp
class Wine { ... };

template<> // MyAllocList specialization
class MyAllocList<Wine> { // for when T is Wine
	private:
		enum class WineType // see Item 10 for info on
		{ White, Red, Rose }; // "enum class"
	WineType type; // in this class, type is a data member!
};
```




>[!IMPORTANT]
>*C++11* gives you the tools to perform these kinds of *transformations* in the form of
*type traits*, an assortment of *templates* inside the *header* **<type_traits>**.



- Given a type *T* to which you’d like to apply a *transformation*, the resulting type is `std::transformation <T>::type`. For example:
```cpp
#include <type_traits>

std::remove_const<T>::type // yield T from const T
std::remove_refrence<T>::type // yield T from T&
std::add_lvalue_refrence<T>::type // yield T& from T

// C++14 alias template 

std::remove_const_t<T> // C++14 equivalent
std::remove_reference_t<T> // C++14 equivalent
std::add_lvalue_reference_t<T> // C++14 equivalent
```



>[!IMPORTANT] **Things to Remember**
>- *typedefs* don’t support *templatization*, but *alias declarations* do.
>-  Alias *templates* avoid the *“::type”* *suffix* and, in templates, the *“typename”* *prefix* often required to refer to *typedefs*.
>-  *C++14* offers alias templates for all the *C++11* type traits *transformations*.