---
Created Date: 2026-05-18
tags:
  - python
  - architecture
  - programming
Next: "[[Iterator Pattern]]"
---
---
## What we Learn
- The *complexities* of *strings*, *bytes*, and *byte arrays*
- The ins and outs of *string* *formatting*
- The *mysterious* **regular expression**
- How to use the `pathlib` *module* to *manage* the `filesystem`
- A few ways to *serialize* data, including *Pickle* and *JSON*


---
## Strings
In python **string** is *immutable* sequence of **Unicode** *characters* (*UTF-8*) 

- **The important rule is this:** we *encode* our *characters* to create *bytes*; we *decode* *bytes* to recover the *characters*.
-  The `b""` *prefix* tell us these are *bytes*

---
### String manipulation
Like other *sequences*, **strings** can be *iterated* over (character by *character*), *indexed*,
*sliced*, or *concatenated*. The *syntax* is the same as for *lists* and *tuples*.

Be careful with the `isdigit()`, `isdecimal()`, and `isnumeric()` methods, as they are more nuanced than we would expect.

```python
s = "hello world"
s1 = s.split(" ") # ["hello", "world"]
s2 = "#".join(s1) # "hello#world"
```

---
### String formatting
Python has powerful *string* *formatting* and *templating*  *mechanisms*   , `f""` prefix one of them that called *f-string*.

---
### Escape braces
When we want to use `{` or `}` in *f-string* must use double braces .
```python
template = f"public class {classnema} {{...}}"
```

---
### Making it look right
we can format output string with `:` after name or content in *braces* 
```python
speed = 5
name = "Test Distance"
fuel_per_hr = 2.2
d = 4
print(f"{'leg':16s} {'dist':5s} {'time':4s} {'fuel':4s}")
print(f"{name:16s} {d:5.2f} {d/speed:4.1f} {d/speed*fuel_per_hr:4.0f}") 
```

---
### Custom formatters
we can use the specifiers used in the `datetime.strftime()` function, as follows:
```python 
import datetime
important = datetime.datetime(2019, 10, 26, 13, 14)
print(f"{important:%Y-%m-%d %I:%M%p}") # 2019-10-26 01:14PM
```


---
### Strings are Unicode
If you get a *string* of *bytes* from a *file* or a *socket*, for example, they won't be in *Unicode*. They will, in fact, be the built-in type *bytes*. *Bytes* are *immutable* *sequences* of...well, *bytes*. *Bytes* are the basic *storage* *format* in *computing*. They represent *8 bits*, usually described as an *integer* between *0* and *255*, or a *hexadecimal* equivalent between `0x00` and `0xFF`. *Bytes* don't represent *anything* specific; a *sequence* of *bytes* may *store* *characters* of an *encoded* *string*, or *pixels* in an *image*, or represent an *integer*, or part of a *floating-point* value.

```python
print(list(map(hex, b'abc'))) # ['0x61', '0x62', '0x63']
print(list(map(bin, b'abd'))) # ['0b1100001', '0b1100010', '0b1100011']
```


>[!NOTE]
>Many *I/O* operations only know how to deal with *bytes*, even if the *bytes* *object* is the *encoding* of *textual* data. It is therefore vital to know how to *convert* between *bytes* values and *Unicode* *str* values.



