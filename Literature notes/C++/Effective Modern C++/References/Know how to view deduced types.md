---
Created Date: 2026-01-11
tags:
  - cpp
Next: "[[auto]]"
---
---

We’ll explore three possibilities: getting type deduction information as you edit your code, getting it during **compilation**, and getting it at **runtime**.

---
## IDE Editors

Code editors in IDEs often show the types of program entities when you do something like hover your cursor over the entity.


> [!NOTE] 
> If that compiler can’t make enough sense of your code to parse it and perform type deduction, it can’t show you what types it deduced.


---
## Compiler Diagnostics

The **error message** reporting the problem is virtually sure to mention the type that’s causing it.

```c++
template<typename T> // declaration only for TD;
class TD; // TD == "Type Displayer"
```

Attempts to instantiate this template will elicit an error message, because there’s no template definition to instantiate.

```c++
TD<decltype(x)> xType; // elicit errors containing
TD<decltype(y)> yType; // x's and y's types
```

```
error: aggregate 'TD<int> xType' has incomplete type and
cannot be defined
error: aggregate 'TD<const int *> yType' has incomplete type
and cannot be defined
```

---

## Runtime Output

“it’s **typeid** and **std::type_info::name** to the rescue.” In our continuing quest to see the types deduced for x and y, you may figure we can write this:

```c++
std::cout << typeid(x).name() << '\n'; // display types for
std::cout << typeid(y).name() << '\n'; // x and y
```

Calls to **std::type_info::name** are not guaranteed to return anything sensible, but implementations try to be helpful.


##### Here’s how our function f can produce accurate type information using **Boost.Type‐Index**:

```c++
#include <boost/type_index.hpp>

template<typename T>
void f(const T& param)
{
using std::cout;
using boost::typeindex::type_id_with_cvr; // show T
cout << "T = " << type_id_with_cvr<T>().pretty_name() << '\n'; // show param's type
cout << "param = " << type_id_with_cvr<decltype(param)>().pretty_name() << '\n';
}
```

---


> [!IMPORTANT] **Things to Remember**
> - Deduced types can often be seen using IDE editors, compiler error messages,
and the **Boost** TypeIndex library.
>- The results of some tools may be neither helpful nor accurate, so an understanding of C++’s type deduction rules remains essential.
