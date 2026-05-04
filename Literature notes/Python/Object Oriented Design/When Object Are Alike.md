---
Created Date: 2026-05-03
tags:
  - python
  - architecture
  - programming
---
---
## What We learn
- Basic Inheritance 
- Inheriting from build-in types
- Multiple inheritance
- Polymorphism and duck typing
---

> Technically every *class* we create uses *inheritance* and implicitly *inherit* from *object*  


```python
class Contact:
	contact_list: List[str] = []
	
	def __init__(self, name: str, email: str) -> None:
		self.name = name
		self.email = email
		self.contact_list.append(self)
	
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}: ({self.name!r}, {self.email!r})" 
		

class Supplier(Contact):
	def order(self, order: "Order") -> None:
		print(f"Order: {order!r} from {self.name!r}")
```
Reff: [[Use shared_ptr for shared-ownership resource management]]


---
## Extending built-ins
*Inherit* form *built-in* classes to adding *new functionality*.

```python
from __future__ import annotations

class ContactList(list["Contact"]):
	def search(self, name: str) -> list["Contact"]:
		matching_contacts: list["Contact"] = []
		for contact in self:
			if name in contact.name:
				matching_contacts.append(contact)
		return matching_contacts

class Contact:
	all_contacts = ContactList()

	def __init__(self, name: str, email: str) -> None:
		self.name = name
		self.email = email
		Contact.all_contacts.append(self)
	
	def __repr__(self) -> str:
		return (
			f"{self.__class__.__name__}("
			f"{self.name!r}, {self.email!r}" f")"
		)
```


- Generic collections: set, list, dict. These use type hints like `set[something]`, `list[something],` and `dict[key, value]` to narrow the hint from purely generic to something more specific that the application will actually use. To use the generic types as annotations, a from __future__ import annotations is required as the first line of code.

- The *typing.NamedTuple* definition lets us define new kinds of immutable tuples and provide useful names for the members. 

- Python has type hints for file-related *I/O* objects. A new kind of file can use a type hint of *typing.TextIO* or *typing.BinaryIO* to describe built-in file operations.

-  It's possible to create new types of strings by extending *typing.Text*. For the most part, the built-in *str* class does everything we need.

-  New numeric types often start with the numbers module as a source for built in numeric functionality.


### super()
This method allow us to use parent method directly and diamond problem.

---
## Polymorphism
Different behaviors happen depending on which *subclass* is  being used. 
It also called the **Liskov Substitution Principle**

> Python is *duck typing* allow us to use any object that provides the required behavior without forcing it to be a *subclass*.

- **Polymorphism** is one of the most important reasons to use *inheritance* in many *object-oriented* context (but not in python) because we need to *public interface*.


---

## SOLID Principles
Design principle in object-oriented-programming 
- Make code more *maintainable*.
- Make code more *extensible*.
- *Loose coupling*.
- easy to write *Unit Test*

1. **S. Single Responsibility Principle**. A class, module, function most be have one responsibility. this mean one reason to change when the application need to change.
2. **O. Open/Close**. A class, module, function should be open to *extension* but close to *modification*.
3. **L. Liskov Substitution**. Any subclass can be substituted for its *superclass*. This tends to focus a class *hierarchy* on classes that have very similar *interfaces*, leading to *polymorphism* among the objects. This the essence of inheritance.
4.  **I. Interface Segregation**. A class should have the *smallest interface possible*. This is, perhaps, the most important of these principles. *Classes* should be relatively *small* and *isolated*.
5.  **D. Dependency Inversion**. This has a peculiar name. We need to know what a bad *dependency* relationship is so we know how to invert it to have a good relationship. Pragmatically, we'd like *classes* to be *independent*, so a *Liskov Substitution* doesn't involve a lot of code changes. In Python, this often means referring to *superclasses* in type hints to be sure we have the flexibility to make changes. In some cases, it also means providing parameters so that we can make global class changes without revising any of the code.