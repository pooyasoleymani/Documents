---
Created Date: 2026-03-08
tags:
  - cpp
  - programming
---
---
- You can *concatenate* a **string**, a **string literal**, a **C-style string**, or a character to a string. The standard string has a *move constructor*, so returning even long **strings** by value is efficient .
```cpp 
string Compose(const string& name, const string& domain)
{
	return name + '@' domain;
}
```

- **string** is *mutable* . and support `=` , `+=` and `[]` or `at()` operations.
```cpp
string name = "Niels Strouptrup";

void m3() {
	string s = name.substr(6, 10);
	name.replace(0, 5. "nicholas");
	name[0] = toupper(name[0]);
};
```

- **string** can be compare with other (`==`, `!=`, `>=`, `<=`, `>`, `<`)
```cpp
string incantation;

void respond(const string& answer)
{
	if (answer==incantation)
		// ...
	else if (answer=="yes")
		// ...
}
```


- If need *C-Style* string (*zero terminated array* of `char`) you can use `c_str()` method.

- **string** is implemented using the *short-string* optimization *(about 14 character)* .
```cpp
string s1{"Annemaire"}; // short string
string s2{"Annemaire Stroustrup"}; // long string
```



>[!IMPORTANT]
>The actual *performance* of **strings** can depend critically on the *run-time* *environment*. In particular, in *multi-threaded* implementations, *memory allocation* can be relatively *costly*. Also, when lots of **strings** of differing *lengths* are used, *memory fragmentation* can result.


