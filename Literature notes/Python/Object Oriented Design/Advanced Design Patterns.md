---
Created Date: 2026-05-23
tags:
  - python
  - architecture
  - programming
Next: "[[Testing Object-Oriented Programs]]"
---
---
## What we Learn
- The *Adapter* pattern
- The *Façade* pattern
- *Lazy* initialization and the *Flyweight* pattern
- The *Abstract Factory* pattern
- The *Composite* pattern
- The *Template* pattern


---
## The Adapter pattern
**Adapters** are used to allow two *preexisting* *objects* to work *together*, even if their *interfaces are not compatible*. Like the display *adapters* that allow you to plug your *Micro USB* charging cable into a *USB-C phone*, an *adapter object* sits between two different *interfaces*, translating between them on the *fly*.

> Simplified of **Adapter** is similar to **decorator**.


- We have *pre-existing class* which takes string *timestamps* in format `HHMMSS` and calculates interval from those strings:
```python
class TimeSince:  
    @staticmethod  
    def parse_time(time: str) -> Tuple[float, float, float]:  
        return (  
            float(time[:2]),  
            float(time[2:4]),  
            float(time[4:]),  
        )  
  
    def __init__(self, time: str) -> None:  
        self.hr, self.min, self.sec = self.parse_time(time)  
        self.strat_second = ((self.hr * 60) + self.min) * 60 + self.sec  
  
    def interval(self, loge_time) -> float:  
        log_hr, log_min, log_sec = self.parse_time(loge_time)  
        log_second = log_hr * 3600 + log_min*60 + log_sec  
        return log_second - self.strat_second
```

- We want to use old logs to calculate *interval* time from first time that `ERROR` occurs
```python
class LogProcessor:  
    def __init__(self, log_entries: list[tuple[str, str, str]]) -> None:  
        self.log_entries = log_entries  
  
    def report(self) -> None:  
        first_time, frist_sev, first_msg = self.log_entries[0]  
        for loge_time, severity, message in self.log_entries:  
            if severity == "ERROR":  
                first_time = loge_time  
	        # >>> We need to compute an interval ????  
	        print(f"{interval:8.2f} | {severity:7s} {message}")
```



- We have several *scenarios*:
	1.  Rewrite `TimeSince` *class* to work with pair of time strings this make violation of `open/close principles`
	2. Create new object of `TimeSince` class for compute interval its make to create a *lot of object* and *violate* `Single Responsibility Principle` and `DRY Principle`


- We use **Adapter class** It consumes the *interface* offered by the `TimeSince` *class*. It allows for *independent* evolution of the two *classes*, leaving them **closed to modification**, but **open to extension**. It looks like this:
```python
class IntervalAdapter:
	self.ts: Optional[TimeSince] = None

	def time_offset(self, start: str, now: str) -> float:
		if self.ts is None:
			self.ts = TimeSince(start)
		else:
			h_m_s = self.ts.parse_time(start)
			if h_m_s != (self.ts.hr, self.ts.min, self.ts.sec):
				self.ts = TimeSince(start)
		return self.ts.interval(now)
		

class LogProcessor:  
    def __init__(self, log_entries: list[tuple[str, str, str]]) -> None:  
        self.log_entries = log_entries
        self.time_convert = IntervalAdapter()  
	def report(self) -> None:
		 first_time, frist_sev, first_msg = self.log_entries[0]  
         for loge_time, severity, message in self.log_entries:  
             if severity == "ERROR":  
                first_time = loge_time  
	         interval = self.time_convert.time_offset(first_time, log_time)
	         print(f"{interval:8.2f} | {frist_sev:7s} {first_msg}")
```



>[!NOTE]
> 1. We also use **inheritance** for add `TmeSince` functionality to `LogProcesse` *class* .
> 2. *Monkey patching* another way for add `parse_time()` method (just use in *unittest*)
> 3. Use *function* for **Adapter** is  a good  idea.

>[!IMPORTANT]
> **Adapter** is *design-time* choice but **Strategy** is a *runtime* pattern



---
## The Facade pattern
The **Facade pattern** is provide a simple *interface* to *complex system* of *components*.
It is allow us to *define* a new *class* that *encapsulates* a typical usage of the *system*.

> **Facade** tries to abstract a *simpler* *interface* out of a *complex* one.
> **Adapter** only tries to *map* one *existing interface* to *another*.



```python
import re  
from pathlib import Path  
from typing import Iterator, Tuple  
  
  
class FindUML:  
    def __init__(self, base: Path) -> None:  
        self.base = base  
        self.start_pattern = re.compile(r"@startuml *(.*)")  
  
    def uml_file_iter(self) -> Iterator[Tuple[Path, Path]]:  
        for source in self.base.glob("**/*.uml"):  
            if any(n.startswith(".") for n in source.parts):  
                continue  
            body = source.read_text(encoding="utf-8")  
            for output_name in self.start_pattern.findall(body):  
                if output_name:  
                    target = source.parent / output_name  
                else:  
                    target = source.with_suffix(".png")  
                yield (
                surce.relative_to(self.base),
                 target.relative_to(self.base)
                 )

```

- We use `subprocess` to create `virtualenv` and create image
```python
import subprocess

class PlanUML:  
    conda_env_name = "CaseStudy"  
    base_env = Path.home() / "miniconda3" / "envs" / conda_env_name  
    def __init__(  
            self,  
            graphviz: Path = Path("bin") / "dot",  
            plantjar: Path = Path("share") / "plantuml.jar",  
    ) -> None:  
        self.graphviz = self.base_env / graphviz  
        self.plantjar = self.base_env / plantjar  
  
    def process(self, source: Path) -> None:  
        env = {  
            "GRAPHVIZ_DOT": str(self.graphviz),  
        }  
  
        command = [  
            "java", "-jar",  
            str(self.plantjar), "-progress",  
            str(source)  
        ]  
        subprocess.run(command, env=env, check=True)  
        print()
```

- We use **Facade pattern** to create useful command-line application:
```python
class GeneratorImages:  
    def __init__(self, base: Path) -> None:  
        self.finder = FindUML(base)  
        self.painter = PlanUML()  
  
    def make_all_images(self) -> None:  
        for source, target in self.finder.uml_file_iter():  
            if (  
                not target.exists()  
                or source.stat().st_mtime > target.stat().st_mtime  
            ):  
                print(f"Processing {source} -> {target}")  
                self.painter.process(source)  
            else:  
                print(f"Skipping {source} -> {target}")
```



>[!IMPORTANT]
>The `stat().st_mtime` is pretty obscure; it turns out the `stat()` *method* of a *Path* provides a lot of file *status information*, and the *modification time* is only one of many things we can find about a *file*.



---
## The Flyweight pattern
This pattern use for *memory optimization*.
The **Flyweight pattern** ensures that *objects* that *share a state* can use the same *memory* for their *shared state*.

**Flyweight object** has no *specific state* just when we need to operate on `SpecificState` object we pass object on **Flyweight object** *argument*.

Traditionally, the *factory* that returns an *instance* of a **Flyweight class** is a *separate object*; its purpose is to *return* individual **Flyweight objects**, perhaps organized by a *key* or *index* of some kind. It works like the *Singleton pattern* but we can create *multiple instance*.

**Flyweight pattern** working with *reference* to data.

>[!IMPORTANT] **Circular Reference**
>We can use *weak reference* to don't increase *reference count*.

- We need to create an **Adapter** for *underlying bytes* object to *transform* it into an *object* that can have *weak references*
```python
from typing import Sequence, Iterator, overload, Union  
  
  
class Buffer(Sequence[int]):  
    def __init__(self, content: bytes) -> None:  
        self.content = content  
  
    def __len__(self) -> int:  
        return len(self.content)  
  
    def __iter__(self) -> Iterator[int]:  
        return iter(self.content)  
  
    @overload  
    def __getitem__(self, index: int) -> int:  
        ...  
    @overload  
    def __getitem__(self, index: slice) -> bytes:  
        ...  
  
    def __getitem__(self,index: Union[int,slice]) -> Union[int,bytes]:  
        return self.content[index]
```


- Application may have code like this and only *one reference exist*:
```python
while True:
	buffer = Buffer(gps_device.read(1024))
	# process ... 
```


- Here's the *abstract* *Message* *class* with some common *methods* to help *parse* these *GPS messages*:
```python
class Message(abc.ABC):  
    def __init__(self) -> None:  
        self.buffer: weakref.ReferenceType[Buffer]  
        self.offset: int  
        self.end: Optional[int]  
        self.commas: list[int]  
  
    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":  
        self.buffer = weakref.ref(buffer)  
        self.offset = offset  
        self.commas = [offset]  
        self.end = None  
        for index in range(offset, offset + 82):  
            if buffer[index] == ord(b','):  
                self.commas.append(index)  
            elif buffer[index] == ord('*'):  
                self.commas.append(index)  
                self.end = index + 3  
                break  
        if self.end is None:  
            raise GPSError("Incomplete")  
  
        return self  
  
    def __getitem__(self, index: int) -> bytes:  
        if (not hasattr(self, "buffer")  
                or (buffer := self.buffer()) is None  
        ):  
            raise RuntimeError("broken reference")  
        start, end = self.commas[index] + 1, self.commas[index + 1]  
        return buffer[start:end]  
  
    def get_fix(self) -> Point:  
         return Point.from_bytes(  
         self.latitude(),  
         self.lat_n_s(),  
         self.longitude(),  
         self.lon_e_w()  
         )  
  
    @abc.abstractmethod  
    def latitude(self) -> bytes:  
        ...  
    @abc.abstractmethod  
    def lat_n_s(self) -> bytes:  
        ...  
    @abc.abstractmethod  
    def longitude(self) -> bytes:  
        ...  
    @abc.abstractmethod  
    def lon_e_w(self) -> bytes:  
        ...  
  
class GPGLL(Message):  
     def latitude(self) -> bytes:  
        return self[1]  
     def lat_n_s(self) -> bytes:  
        return self[2]  
     def longitude(self) -> bytes:  
        return self[3]  
     def lon_e_w(self) -> bytes:  
        return self[4]
```


-  create *Flyweight factory* 
```python
@functools.lru_cache()
def message_factory(header: bytes) -> Optional[Message]:
	if header == b"GPGGA":
		return GPGGA()
	elif header == b"GPGLL":
		return GPGLL()
	elif header == b"GPRMC":
		return GPRMC()
	else:
		return None
```


```sh
>>> buffer = Buffer(
... b"$GPGLL,3751.65,S,14507.36,E*77"
... )
>>> flyweight = message_factory(buffer[1 : 6])
>>> flyweight.from_buffer(buffer, 0)
<gps_messages.GPGLL object at 0x7fc357a2b6d0>

>>> flyweight.get_fix()
Point(latitude=-37.86083333333333, longitude=145.12266666666667)

>>> print(flyweight.get_fix())
(37°51.6500S, 145°07.3600E)
```

- Multiple message in a buffer
```sh
>>> buffer_2 = Buffer(
... b"$GPGLL,3751.65,S,14507.36,E*77\\r\\n"
... b"$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41\\r\\n"
... )
>>> start = 0
>>> flyweight = message_factory(buffer_2[start+1 : start+6])
>>> p_1 = flyweight.from_buffer(buffer_2, start).get_fix()
>>> p_1
Point(latitude=-37.86083333333333, longitude=145.12266666666667)
>>> print(p_1)
(37°51.6500S, 145°07.3600E)

>>> flyweight.end
30
>>> next_start = buffer_2.index(ord(b"$"), flyweight.end)
>>> next_start
32
>>>
>>> flyweight = message_factory(buffer_2[next_start+1 : next_start+6])
>>> p_2 = flyweight.from_buffer(buffer_2, next_start).get_fix()
>>> p_2
Point(latitude=37.387458333333335, longitude=-121.97236)
>>> print(p_2)
(37°23.2475N, 121°58.3416W)
```


---
### Memory optimization via Python's `__slots__`
Instead of a *Flyweight design*– where *storage* is *intentionally shared* – a **slots design** creates *objects* with their own *private data*, but avoids Python's *built-in dictionary*. Instead, there is *direct mapping* from *attribute name* to a *sequence* of values, avoiding the rather *large hash table* that is a part of every Python *dict object*.

```python
class Point:
	__slots__ = ("latitude", "longitude")
	
	def __init__(self, latitude: float, longitude: float) -> None:
		self.latitude = latitude
		self.longitude = longitude
		
	def __repr__(self) -> str:
		return (
		f"Point(latitude={self.latitude}, "
		f"longitude={self.longitude})"
		)
```



---
## Abstract Factory pattern
The **Abstract Factory** pattern is appropriate when we have *multiple* possible implementations of a *system* that depend on some *configuration* or *platform* detail. The calling *code requests* an *object* from the **Abstract Factory**, not knowing exactly what *class* of *object* will be returned. The underlying implementation returned may depend on a variety of factors, such as the *current locale*, *operating system*, or *local configuration*.

**Example:**  operation-system-independent toolkit, database backends

---
There are *two* central features of an **Abstract Factory**:
	-  We need to have *multiple implementation choices*. Each implementation has a *factory class* to *create objects*. A *single Abstract Factory* defines the *interface* to the implementation *factories*.
	-  We have a number of *closely* *related* *objects*, and the relationships are *implemented* via *multiple methods* of each *factory*.

---

```python
import abc  
from enum import Enum, auto  
from typing import NamedTuple, List  
  
  
class Suit(str, Enum):  
    Clubs = "\N{Black Club Suit}"  
    Diamonds = "\N{Black Diamond Suit}"  
    Hearts = "\N{Black Heart Suit}"  
    Spades = "\N{Black Spade Suit}"  
  
####################################################################### 
class Trick(str, Enum):  
    pass  
    
####################################################################### 
class Card(NamedTuple):  
    rank: int  
    suit: Suit  
  
    def __str__(self):  
        return f"{self.rank}{self.suit}"  
        
####################################################################### 
class Hand(List[Card]):  
    def __init__(self, *cards: Card) -> None:  
        super().__init__(cards)  
  
    def scoring(self) -> int:  
        pass  
        
####################################################################### 
class CardGameFactory(abc.ABC):  
    @abc.abstractmethod  
    def make_card(self, rank: int, suit_: Suit) -> "Card":  
        ...  
    @abc.abstractmethod  
    def make_hand(self, *cards: Card) -> "Hand":  
        ...  
        
        
class PokerFactory(CardGameFactory):  
     def make_card(self, rank: int, suit_: Suit) -> "Card":  
        if rank == 1:  
            # Aces above kings  
            rank = 14  
        return PokerCard(rank=rank, suit=suit_)  
  
     def make_hand(self, *cards: Card) -> "Hand":  
        return PokerHand(*cards)
        
#######################################################################  
class CribbageCard(Card):  
     @property  
     def points(self) -> int:  
        return self.rank  
  
class CribbageAce(Card):  
     @property  
     def points(self) -> int:  
        return 1  
  
class CribbageFace(Card):  
     @property  
     def points(self) -> int:  
        return 10  
  
class CribbageHand(Hand):  
    starter: Card  
  
    def upcard(self, starter: Card) -> Hand:  
        self.starter = starter  
        return self  
  
    def scoring(self) -> int:  
        tricks = Trick.value  
        return tricks  
  
#######################################################################  
class PokerCard(Card):  
     def __str__(self) -> str:  
        if self.rank == 14:  
            return f"A{self.suit}"  
        return f"{self.rank}{self.suit}"  
  
class PokerHand(Hand):  
     def scoring(self) -> list[Trick]:  
         """Return a single 'Trick'"""  
         #... details omitted ...  
         rank = Trick.value  
         return [rank]  
```


---
### Abstract Factory in python
In python we don't need *abstract base class* .
This *class* have *separate modules* we can import factory method like that `from cribbage import CardGameFactory` 

```python
class CardGameFactoryProtocol(Protocol):
	def make_card(self, rank: int, suit: Suit) -> "Card":
		...
		
	def make_hand(self, *cards: Card) -> "Hand":
		...
```



>[!NOTE]
>Unlike the *abstract base class* definition, this is not a *runtime check*. A *protocol* definition is only used by *mypy* to *confirm* that the code is likely to pass its unit test suite.




---
## The Composite pattern
The **Composite pattern** allows *complex tree structures* to be built from *simple components*, often called **nodes**.

A *composite object* is – generally – *a container object*, where the content may be another *composite object*.
Each **node** in a *composite object* must be either a **leaf node** (that cannot contain other *objects*) or a **composite node**.

**Example:**  *Markup languages*, like *HTML*, *XML*, *RST*, and *Markdown*, tend to reflect some common *composite* concepts like *lists* of *lists*, and *headers* with *sub-headings*.

```python
from __future__ import annotations  
import abc  
from typing import Optional  
  
class Node(abc.ABC):  
    def __init__(self, name: str) -> None:  
        self.name = name  
        self.parent: Optional["Folder"] = None  
  
    def move(self, new_place: "Folder") -> None:  
        previous = self.parent  
        new_place.add_child(self)  
        if previous is not None:  
            del previous.children[self.name]  
  
    @abc.abstractmethod  
    def copy(self, new_place: "Folder") -> None:  
        ...  
  
    @abc.abstractmethod  
    def remove(self) -> None:  
        ...  
  
class Folder(Node):  
    def __init__(self, name, children: Optional[dict[str, "Node"]] = None):  
        super().__init__(name)  
        self.children = children or {}  
  
    def __repr__(self) -> str:  
        return f"Folder({self.name!r}, {self.children!r})"  
  
    def add_child(self, node: "Node") -> "Node":  
        node.parent = self  
        return self.children.setdefault(node.name, node)  
  
    def copy(self, new_folder: "Folder") -> None:  
        target = new_folder.add_child(Folder(self.name))  
        for c in self.children.keys():  
            self.children[c].copy(target)  
  
    def remove(self) -> None:  
        names = list(self.children)  
        for name in names:  
            self.children[name].remove()  
        if self.parent:  
            del self.parent.children[self.name]  
  
class File(Node):  
    def __init__(self, name: str) -> None:  
        super().__init__(name)  
  
    def __repr__(self) -> str:  
        return f"File({self.name!r})"  
  
    def copy(self, new_path: "Folder") -> None:  
        new_path.add_child(File(self.name))  
  
    def remove(self):  
        if self.parent:  
            del self.parent.children[self.name]
```


---
## The Template pattern
The **Template pattern (Template method)** is useful for *removing* *duplicate code*; it's intended to support the **Don't Repeat Yourself principle**. It is designed for situations where we have several *different tasks* to accomplish that have some, *but not all*, steps in *common*. The *common* steps are implemented in a *base class*, and the *distinct* steps are *overridden* in *subclasses* to provide custom *behavior*.


These seem like quite different tasks, but they have some common features. In both cases, we need to perform the following steps:
1. Connect to the database
2. Construct a query for new vehicles or gross sales
3. Issue the query
4. Format the results into a comma-delimited string
5. Output the data to a file or email

```python
import contextlib  
import csv  
import datetime  
import sqlite3  
import sys  
from pathlib import Path  
from typing import TextIO, ContextManager, cast  
  
  
class QueryTemplate:  
     def __init__(self, db_name: str = "sales.db") -> None:  
         self.db_name = db_name  
         self.conn: sqlite3.Connection  
         self.results: list[tuple[str, ...]]  
         self.query: str  
         self.header: list[str]  
     def connect(self) -> None:  
        self.conn = sqlite3.connect(self.db_name)  
  
     def construct_query(self) -> None:  
        raise NotImplementedError("construct_query not implemented")  
  
     def do_query(self) -> None:  
        results = self.conn.execute(self.query)  
        self.results = results.fetchall()  
  
     def output_context(self) -> ContextManager[TextIO]:  
        self.target_file = sys.stdout  
        return cast(ContextManager[TextIO], contextlib.nullcontext())  
  
     def output_results(self) -> None:  
         writer = csv.writer(self.target_file)  
         writer.writerow(self.header)  
         writer.writerows(self.results)  
  
     def process_format(self) -> None:  
         self.connect()  
         self.construct_query()  
         self.do_query()  
         with self.output_context():  
            self.output_results()  
  
  
class NewVehiclesQuery(QueryTemplate):  
     def construct_query(self) -> None:  
         self.query = "select * from Sales where new='true'"  
         self.header = ["salesperson", "amt", "year", "model", "new"]  
  
  
class SalesGrossQuery(QueryTemplate):  
     def construct_query(self) -> None:  
         self.query = (  
         "select salesperson, sum(amt) "  
         " from Sales group by salesperson"         )  
         self.header = ["salesperson", "total sales"]  
  
     def output_context(self) -> ContextManager[TextIO]:  
         today = datetime.date.today()  
         filepath = Path(f"gross_sales_{today:%Y%m%d}.csv")  
         self.target_file = filepath.open("w")  
         return self.target_file
```