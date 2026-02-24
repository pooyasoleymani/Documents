---
Created Date: 2026-02-24
tags:
  - cpp
  - programming
---
---
#### The *I/O* stream library provide formatted and unformatted *buffered I/O*  of test and numeric values.


The operations on `istreams` and `ostreams` are *type safe*, *type-sensitive*, and *extensible* to handle *user-defined* *types* .

These **streams** can be used for *binary I/O*, be used for a variety of *character types*, be locale specific, and use advanced buffering strategies.

The streams can be used for input into and output from *std::strings* , for formatting into *string buffers* , and for file *I/O* .

The *I/O stream* classes all have *destructors* that f*ree all resources* owned (such as buffers and  file handles). That is, they are examples of *"Resource Acquisition Is Initialization"*


### I/O State
An **iostream** has state that we can examine to determine weather an operations succeeded.
**I/O** state hold all the information need to read or write, such as *formatting information*, 
*error state*, *type of buffering*.
```cpp
auto read_int(std::istream& is,const std::string& terminator)
{
	std::vector<int> res;
	for(int i; is >> i;)
	{
		res.push_back(i);
	}
	if(is.eof())
		return res;
	if(is.fail())
	{
		is.clear();
		is.unget();
		std::string s;
		if(is >> s && s==terminator)
			return res;
		is.setstate(std::ios_base::failbit);
	}
	return res;
}
```


###  I/O of User-Defined Types

In addition to the **I/O** of built-in types and standard *strings*, the *iostream* library allows programmers to define **I/O** for their own types. For example, consider a simple type Entry that we might use to represent entries in a telephone book:

```cpp
struct Entry {
	string name;
	int number;
};
```

We can define a simple output operator to write an *Entry* using a *{"name",number}* format similar to the one we use for initialization in code:
```cpp
ostream& operator<<(ostream& os, const Entry& e)

{
	return os << "{\"" << e.name << "\", " << e.number << "}";
}
```

A *user-defined output* operator takes its output stream (by reference) as its first argument and returns it as its result.
The corresponding input operator is more complicated because it has to check for correct for*matting* and deal with errors:

```cpp
istream& operator>>(istream& is, Entry& e)
// read { "name" , number } pair. Note: for matted with { " " , and }
{
	char c, c2;
	if (is>>c && c=='{' && is>>c2 && c2=='"') { // star t with a { "
		string name;
		// the default value of a string is the empty string: ""
		while (is.get(c) && c!='"') // anything before a " is part of the name
			name+=c;
			if (is>>c && c==',') {
				int number = 0;
				if (is>>number>>c && c=='}') { // read the number and a }
				e = {name ,number}; // assign to the entry
				return is;
			}
		}
	}
	is.setstate(ios_base::failbit); // register the failure in the stream
	return is;
}
```

An input operation returns a reference to its istream that can be used to test if the operation succeeded. For example, when used as a condition, *is>>c* means ‘‘Did we succeed at reading a char from is into c?’’

The *is>>c* skips whitespace by default, but **is.get(c)** does not, so this *Entry*-input operator ignores (skips) whitespace outside the name string, but not within it.


### Formatting
