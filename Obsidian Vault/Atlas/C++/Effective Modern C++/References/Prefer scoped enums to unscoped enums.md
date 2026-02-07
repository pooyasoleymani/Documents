---
Created Date: 2026-01-24
tags:
  - cpp
  - programming
Up: "[[Prefer alias declarations to typedefs]]"
Next: "[[Prefer deleted functions to private undefinedones]]"
---
---

- The names of such *enumerators* belong to the *scope* containing the **enum**,  that means  nothing else in that *scope* may have the same name:
```c++
enum Color {black, white, red} 
auto white = false // error! whit already declared in this scope
```



- Their new *C++11* counterparts, *scoped* **enums**, don’t leak names in this way:
```cpp
enum class Color { black, white, red }; // black, white, red // are scoped to Color
auto white = false; // fine, no other

Color c = white; // error! no enumerator named // "white" is in this scope
Color c = Color::white; // fine
auto c = Color::white; // also fine (and in accord // with Item 5's advice)
```


- *Enumerators* for **unscoped enums** *implicitly* convert to *integral types*:
```cpp
enum Color { black, white, red }; // unscoped enum

std::vector<std::size_t> primeFactors(std::size_t x); // prime factors of x

Color c = red;

if (c < 14.5) { // compare Color to double (!)
	auto factors = primeFactors(c);// compute prime factors // of a Color (!)
}
```




- There are no *implicit* *conversions* from *enumerators* in a **scoped enum** to any other type:
```cpp
enum class Color { black, white, red }; // enum is now scoped
Color c = Color::red; // as before, but // with scope qualifier

if (static_cast<double>(c) < 14.5) 
	{ // odd code, but it's valid 
		auto factors = primeFactors(static_cast<std::size_t>(c)); 
		// suspect, but it compiles
	}
```



- **scoped enums** may be *forward-declared*:
```cpp
enum Color; // error!

enum class Color; // fine
```



>[!NOTE] 
>The work grows out of the fact that every enum in *C++* has an **integral underlying type** that is determined by *compilers*.
>To make *efficient* use of *memory*, *compilers* often want to choose the **smallest underlying type** for an *enum* that’s sufficient to represent its range of *enumerator* values.


```cpp
enum Color {black, white, red} // compiler choose char as the underlying type

enum Status { good = 0,
	failed = 1,
	incomplete = 100,
	corrupt = 200,
	indeterminate = 0xFFFFFFFF // 8 byte
};  // compiler choose an Inegral type lager than char
```


- By default the *underlying type* for **scoped enum** in *int*:
```cpp
enum class Status; // underlying type is int 

enum class Status: std::uint32_t;
enum class Color: std::uint8_t;
```


- You can *get* value of **unscoped enum** like *tuples*:
```cpp
enum UserInfoFields { uiName, uiEmail, uiReputation };
UserInfo uInfo; // as before

auto val = std::get<uiEmail>(uInfo); // ah, get value of email field

// The corresponding code with scoped enums is substantially more verbose:

enum class UserInfoFields { uiName, uiEmail, uiReputation };
UserInfo uInfo; // as before

auto val = std::get<static_cast<std::size_t>(UserInfoFields::uiEmail)>(uInfo);
```




- Rather than returning *std::size_t*, we’ll return the **enum’s underlying type**. It’s available via the **std::underlying_type** type trait. we’ll declare it **noexcept**, because we know it will never yield an *exception*:
```cpp
// C++11

template<typename E>
constexpr typename std::underlying_type<E>::type toUType(E enumerator) noexcept
{
 return static_cast<typename std::underlying_type<E>::type>(enumerator);
}

// C++14

template<typename E> 
constexpr std::underlying_type_t<E> toUType(E enumerator) noexcept
{
 return static_cast<std::underlying_type_t<E>>(enumerator);
}

// C++14

template<typename E>
constexpr auto toUType(E enumerator) noexcept
{
 return static_cast<std::underlying_type_t<E>>(enumerator);
}

// Regardless of how it’s written, toUType permits us to access a field of the 
// tuple like this:

auto val = std::get<toUType(UserInfoFields::uiEmail)>(uInfo);
```



---


>[!IMPORTANT]  **Things to Remember**
>-  *C++98-style enums* are now known as *unscoped enums*.
>-  *Enumerators* of *scoped enums* are **visible** only within the *enum*. They convert to other types only with a *cast*.
>-  Both *scoped and unscoped enums* support specification of the *underlying type*. The default *underlying type* for scoped *enums* is **int**. *Unscoped enums* have no default *underlying type*.
>-  *Scoped enums* may always be *forward-declared*. *Unscoped enums* may be *forward-declared* only if their declaration specifies an *underlying type*.


