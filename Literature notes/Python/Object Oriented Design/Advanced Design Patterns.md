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


