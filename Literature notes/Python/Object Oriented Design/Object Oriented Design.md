---
Created Date: 2026-02-24
tags:
  - python
  - architecture
  - programming
---
---
## What We Learn
1. What is *object-oriented* means
2. Difference between *object-oriented-design* and *object-oriented-programming* 
3. The basic principles of *object-oriented-design*
4. Basic *Unified Modeling Language (UML)* and when it isn't evil

---

**Object**: every thing that we can sense, feel, and manipulate.
**Object(Computer)**: Collection of *data* and associated *behaviors*.


>[!NOTE]
>In fact, *analysis*, *design*, and *programming* are all *stages* of *software development*.
 Calling them **object-oriented** simply specifies what kind of *software development* is
 being pursued.

---
- **Object-Oriented-Analysis:** 
The process of looking at a *problem*, *system* or *task* and identifying the *object* and interaction between them(*what* we need).
Output of the *analysis stage* often in the form of **[[requirements]]**.  

- **Object-Oriented-Design:**
The process of converting such **requirements** into an implementation specification such as name *objects* and *behaviors*(transform *what* to *how* it should be done)

- **Object-Oriented-Programming:**
The process of converting a *design* into a working program that does what the product owner originally requested.

---
### Iterative Development
In **Iterative Development Model** , a small part of the task is *modeled*, *designed* and *programmed* and *product* is *reviewed* and *expanded* to improve each *feature* and include *new feature* in a series of short *development cycles*.

---
- **Objects vs Classes:**
*Class* is blueprint of creating object .

---

> In **Python** can called *attributed* an *instance variable*.
> But generally *Attributed (settable)* referred to *members* or *properties(read-only)*

---
- **Interface:**
Collection of *attributes* and *methods* that other objects can access to interact with that object.
*Example:* remote control of TV is interface to access to TV attributes.

---
- **Encapsulation**
Hiding the *implementation* of an object is suitably called **information hiding**. 
It is also sometimes referred to as *encapsulation*, but encapsulation is actually a more encompassing term. *Encapsulated* data is not necessarily hidden.

---
- **Abstraction**
Means dealing with level of the detail that is most appropriate to a giving task.

---
##  Composition
Act of *collecting* several *objects* together to *create* a new *object*.

1. A strong relationship a whole part structure with *full ownership*
2. container control the *lifetime* of its *compositions*
3. If container *destroy* all owned parts is *destroyed* with it.

*Example:* Home compose with room

```cpp
class Romm {
	public:
	string name;
	Room(string n): name{n} {}
};

class Home {
	public:
	string name;
	vector<Room> rooms;
	
	void AddRoom(Room& r) {
		roooms.push_back(r);
	}
}
```

---
- **Object State**
Data represents the individual characteristics of a certain object its current state. 

---
- **Aggregation**
It is like *Composition*, the difference is that aggregate objects can exist independently.

Another way to differentiate between aggregation and composition is to think about the lifespan of the object:
1. If the *composite (outside)* object *controls* when the *related (inside)* objects are *created* and *destroyed*, **composition** is most suitable.
2. If the *related object* is *created independently* of the *composite object*, or can *outlast* that *object*, an *aggregate relationship* makes more sense.

*Example:* Team and players

```cpp
class Player {
	public:
	Player(string n): name{n}{}
private:
	string name;
};

class Team {
	public:
		Team(string t): tname{t}{}
		void AddPlayer(Player* player)
		{
			players.push_back(palyer);
		}
	private:
	string tname;
	vector<player*> players; // aggregate with pointers or references
}
```

---
- **Association**
1. it general relation
2.  object can *use* or *interact* with another
3. *Neither* object *owns* the other 
4. All objects exist *independently*
5. Their *association* is *temporary*
6. **Multiplicity**: one-to-one, one-to-many

*Example:* teacher and student

```cpp
class Student {
	void study();
};

class Teacher {
	void teach(Student& s) {
		s.study();
	}
}
```

---
## Inheritance
Driven class inherit Base class behavior , methods or properties.
if use Abstract class driven class must be *override* abstract method.

*Pron:* It make to repeatability and we don't need to rewrite code
*Cron:* tightly coupling in interface and driven class  


- **Interface(Python):** Class with pure abstract method.

```python
class Base(ABC):
	@abstractmethod
	def some_method(self)
		return NotImplemented

class Driven(Base):
	def some_method(self):
		print("some_method overrided")
```


- **Polymorphism:** ability to treat a class differently depending on with subclass is implemented.

```python
class Base:
	def some_method(self):
		print("some_method in bass class called")

class Driven(Base):
	def some_method(self):
		print("some_method in driven class called")
```



---
## Multiple Inheritance
Allow *subclass* inherit functionality from multiple parent classes.
it is *harmful* if parents provide *overlapping* .

- **Method Resolution Order(MRO)**
Python provide *MRO* to understand witch of the alternative methods will be used and avoiding *overlapping*.
#### Multiple inheritance as a *mixin* *technique* for combining unrelated aspects can be helpful.
