---
Created Date: 2026-01-25
tags:
  - cpp
  - programming
Next: "[[Declare overriding functions override]]"
---
---

- The situation arises only for the **“special member functions,”** i.e., the **member functions** that *C++* *automatically generates* when they’re *needed*.

- To render **istream** and **ostream** *classes* *uncopyable*, **basic_ios** is specified in *C++98* as follows (including the comments):

```cpp
template<class CharT, class traits = char_traits<CharT>>
class basic_ios: public ios_base {
	public: 
		...
	private:
		basic_ios(const basic_ios&); // not define
		basic_ios& operator=(const basic_ios&); // not define
}
```



- Declaring these *functions* **private** prevents clients from calling them. Deliberately failing to define them means that if *code* that still has *access* to them (i.e., *member functions* or *friends of the class*) uses them, *linking* will fail due to missing *function* *definitions*.

- use **“= delete”** to mark the *copy constructor* and the *copy assignment* operator as *deleted* *functions*.
```cpp
template <class charT, class traits = char_traits<charT> >
class basic_ios : public ios_base {
	public:
		 ...
		basic_ios(const basic_ios& ) = delete;
		basic_ios& operator=(const basic_ios&) = delete;
		 ...
};
```



>[!NOTE]
>*Deleted functions* may *not be used* in any way, so even code that’s in *member and friend functions* will *fail* to *compile* if it tries to *copy* **basic_ios** objects.



- When *client code* tries to use a *deleted private* *function*, some *compilers* complain only about the *function* being *private*, even though the function’s accessibility doesn’t really affect whether it can be used.



- An important advantage of *deleted functions* is that any *function* may be *deleted*, while only *member functions* may be *private*, we can *delete* *overloads* for the types we want to *filter out*:

```cpp
bool isLucky(int number); // orginal function

bool isLucky(char) = delete; // reject chars
bool isLucky(bool) = delete; // reject bools
bool isLucky(double) = delete; // reject doubles and floats

if (isLucky('a')) … // error! call to deleted function
```



- Another trick that *deleted* *functions* can perform (and that private member functions can’t) is to *prevent* use of *template instantiations* that should be *disabled*:

```cpp
template<typename T>
void processPointer(T* ptr);

template<>
void processPointer<void>(void*) = delete;

template<>
void processPointer<char>(char*) = delete;

template<>
void processPointer<const void>(const void*) = delete;

template<>
void processPointer<const char>(const char*) = delete;

//you’ll also delete the const volatile void* and const volatile char* overloads,
```




>[!IMPORTANT] 
>if you have a *function template* inside a *class*, and you’d like to *disable* some *instantiations* by declaring them *private* (à la classic C++98 convention), you can’t, because it’s not possible to give a *member function template specialization* a *different access level* from that of the *main* *template*.
>```cpp
>class Widget {
public:
…
template<typename T>
void processPointer(T* ptr)
{ … }
private:
template<> // error!
void processPointer<void>(void*);
};
>```





- The problem is that *template specializations* must be written at *namespace scope*, not *class scope*. This issue doesn’t arise for *deleted functions*, because they *don’t* need a different *access level*.
```cpp
class Widget {
public:
…
template<typename T>
void processPointer(T* ptr)
{ … }

};
template<> // still public,but deleted
void Widget::processPointer<void>(void*) = delete; 
```


---


>[!IMPORTANT] **Things to Remember**
>- Prefer **deleted** **functions** to *private undefined ones*.
>-  Any *function* may be *deleted*, including *non-member functions* and *template instantiations*.

