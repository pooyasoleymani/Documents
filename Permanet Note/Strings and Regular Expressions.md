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


- **string** is an alias for general template **basic_string** with character type *char*:
```cpp
template<typename Char>
class basic_string {
	// string of character
};

using string = basic_string<char>;
```



### string_view
**string_view** is pair of pointer, length and *read-only* view of character.
Behavior of *out-of-range* access to **string_view** is undefined, for range check consider *at()*  or use `gsl::span` or `gsl::string_span`:

```
string_view: {begin(), size()}
```

```cpp
using std::literals::string_view_literals;

string cat(string_view sv1, string_view sv2)
{
	string res(sv1.length() + sv2.length());
	char* p = &res[0];
	for (char c: sv1) // one way
		*p++ = c;
	copy(sv2.begin(), sv2.end(), p); // another way
	return res;
};

string king = "Harold"
auto s1 = cat(king , "Wilam"); // string and const char*
auto s2 = cat(king, king); // string and string
auto s3 = cat("Edward", "stephen"sv) // const char* and string_view
auto s4 = cat({&king[0], 2}, "Henry"sv);
```


### Regular Expressions
**Raw String Literal:** string that start with *R"(*  and terminated with *)"*  