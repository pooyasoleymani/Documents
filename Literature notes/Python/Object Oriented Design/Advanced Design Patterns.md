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
> **Adapter**only tries to *map* one *existing interface* to *another*.



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
