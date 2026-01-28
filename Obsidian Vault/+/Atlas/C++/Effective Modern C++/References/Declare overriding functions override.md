---
Created Date: 2026-01-26
tags:
  - cpp
  - programming
Up: "[[Prefer deleted functions to private undefinedones]]"
Next: "[[Prefer const_iterators to iterators]]"
Home: "[[Effective Modern C++17]]"
---
---


- *virtual function* **overriding** is what makes it possible to *invoke* a *derived class function* through a *base class interface*:
```cpp
class Base {
	public:
		virtual viod DoWok();
		...
};

class Derived: public Base {
	public:
		viod DoWork() override {
			...
		}
};

std::unique_ptr<Base> ipb = std::make_unique<Derived>();

upb->DoWork();
```




##### For **overriding** to occur, several *requirements* must be met:
 1. The *base class function* must be **virtual**.
 2. The *base* and *derived function* names must be *identical* (except in the case of *destructors*).
 3. The *parameter types* of the *base* and *derived functions* must be *identical*.
 4. The **constness** of the *base* and *derived functions* must be *identical*.
 5. The *return types* and *exception* specifications of the *base* and *derived functions* must be *compatible*.
 6. The **functions’ reference** qualifiers must be *identical*

```cpp
class Widget {
public:
...
void doWork() &; // this version of doWork applies only when *this is an lvalue
void doWork() &&; // this version of doWork applies only when *this is an rvalue
};

Widget makeWidget(); // factory function (returns rvalue)
Widget w; // normal object (an lvalue)
...
w.doWork(); // calls Widget::doWork for lvalues (i.e., Widget::doWork &)
makeWidget().doWork(); // calls Widget::doWork for rvalues (i.e., Widget::doWork &&)
```



>[!NOTE]
>if a *virtual function* in a *base class* has a *reference qualifier*, *derived class* **overrides** of that *function* must have exactly the same **reference qualifier**. If they don’t, the declared functions will still exist in the *derived class*, but they won’t *override* anything in the *base class*.



##### Code containing **overriding** *errors* is typically *valid*, but its meaning isn’t what you intended. You therefore can’t rely on *compilers* notifying you if you do something *wrong*.



>[!IMPORTANT]
>Applying **final** to a **virtual function** *prevents* the *function* from being *overridden* in *derived classes*. **final** may also be applied to a *class*, in which case the *class* is prohibited from being used as a *base class*.




- What’s needed is a way to *specify* that when **data** is *invoked* on an **rvalue** Widget, the result should also be an **rvalue**. Using *reference qualifiers* to *overload* data for **lvalue** and **rvalue** Widgets makes that possible:

```cpp
class Widget {
public:
using DataType = std::vector<double>;

DataType& data() & // for lvalue Widgets,
{ return values; } // return lvalue

DataType data() && // for rvalue Widgets,
{ return std::move(values); } // return rvalue

private:
DataType values;
};

// calls lvalue overload for
// Widget::data, copy-constructs vals1
auto vals1 = w.data(); 

// calls rvalue overload for
// Widget::data, move-constructs vals2
auto vals2 = makeWidget().data(); 

```



---

>[!IPORTANT] **Things to Remember**
>- Declare *overriding* functions *override*.
>- Member *function* *reference qualifiers* make it possible to treat *lvalue* and *rvalue* objects (*this*) differently.

