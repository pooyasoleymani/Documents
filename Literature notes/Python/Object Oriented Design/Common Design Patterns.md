---
Created Date: 2026-05-22
tags:
  - python
  - architecture
  - programming
Next: "[[Advanced Design Patterns]]"
---
---
## What we Learn
In this chapter, we'll see:
- The *Decorator* pattern
- The *Observer* pattern
- The *Strategy* pattern
- The *Command* pattern
- The *State* pattern
- The *Singleton* pattern
---
## The Decorator pattern
The *Decorator* pattern allows us to *wrap* an *object* that provides *core functionality* with other *objects* that *alter* this *functionality*.

There are two primary uses of the **Decorator pattern**:
1. *Enhancing* the *response* of a *component* as it sends *data* to a *second* *component*
2. Supporting *multiple optional behaviors*

```python
import contextlib  
import socket  
from random import randint  
  
  
def dice_roller(request: bytes) -> bytes:  
    request_text = request.decode("utf-8")  
    numbers = [randint(1, 10) for _ in range(10)]  
    response = f"{request_text} {sum(numbers)}".encode("utf-8")  
    return response  
  
def dice_response(client: socket.socket) -> None:  
    request = client.recv(1024)  
    try:  
        response = dice_roller(request)  
    except (ValueError, KeyError) as ex:  
        response = repr(ex).encode("utf-8")  
    client.send(response)  
  
  
def main_1():  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.bind(('localhost', 8080))  
    server.listen(1)  
    with contextlib.closing(server):  
        while True:  
            client, address = server.accept()  
            dice_response(client)  
            client.close()  
  
def main():  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.connect(('localhost', 8080))  
    count = input("How many roller: ") or "1"  
    pattern = input("Dic pattern nd6[dk+-]a: ") or "d6"  
    command = f"Dice {count} {pattern}".encode("utf-8")  
    server.send(command)  
    response = server.recv(1024)  
    print(response.decode("utf-8"))  
    server.close()
```

- create `LogSocket` *decorator*
```python
class LogSocket:
	def __init__(self, socket: socket.socket) -> None:
		self.socket = socket
	
	def recv(self, count: int) -> bytes:
		data = self.socket.recv(count)
		print(f"Receiving {data!r} from {self.socket.getpeername()[0]}")
		return data
	
	def send(self, data: bytes) -> None:
		print(f"send {data!r} to {self.socket.getpeername()[0]}")
		self.send(data)
	
	def close(self) -> None:
		self.socket.close()
```

- *decorate* with `__call__()` method:
```python
import gzip
import io

Address = Tuple[str, int]

class LogRoller:
	def __init__(self, dice: Callable[[bytes], bytes], remote_address: Address) -> None:
	self.dice = dice
	self.remote_address = remote_address
	
	def __call__(self, request: bytes) -> bytes:
		print(f"Receiving {request!r} from {self.remote_addr}")
		dice_roller = self.dice_roller
		response = dice_roller(request)
		print(f"Sending {response!r} to {self.remote_addr}")
		return response



class ZipRoller:
	def __init__(self, dice: Callable[[bytes], bytes]) -> None:
		self.dice_roller = dice

	def __call__(self, request: bytes) -> bytes:
		dice_roller = self.dice_roller
		response = dice_roller(request)
		buffer = io.BytesIO()
		with gzip.GzipFile(fileobj=buffer, mode="w") as zipfile:
			zipfile.write(response)
		return buffer.getvalue()

def dice_response(client: socket.socket) -> None:
	request = client.recv(1024)
	try:
		remote_addr = client.getpeername()
		roller_1 = ZipRoller(dice.dice_roller)
		roller_2 = LogRoller(roller_1, remote_addr=remote_addr)
		response = roller_2(request)
	except (ValueError, KeyError) as ex:
		response = repr(ex).encode("utf-8")
	client.send(response)
```


### Decorator in python

**Decorator** in python have additional options .
for example *monkey-patching* changing *class definition* at *runtime* to get similar effect.

```python
from fonctools import wraps

def log_args(function: Callable[..., Any]) -> Callable[..., Any]:
	@wraps(function)
	def wrapped_function(*args: Any, **kwargs: Any) -> Any:
		print(f"Calling {function.__name__}(*{args}, **{kwargs})")
		result = function(*args, **kwargs)
		return result
	return wrapped_function
```

- *Parameterized decorators*
```python
class NamedLogger:
	def __init__(self, logger_name: str) -> None:
		self.logger = logging.getLogger(logger_name)
	
	def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
		@wraps(function)
		def wrapped_function(*args: Any, **kwargs: Any) -> Any:
			strat = time.perf_counter()
			try:
				result = function(*args, **kwargs)
				dt = (time.perf_counter() - start) * 1_000_000
				self.logger.info(f"{function.__name__}, {dt:.1f}")
			except Exception as ex:
				dt = (time.perf_counter() - start) * 1_000_000
				self.logger.error(f"{function.__name__}, {dt:.1f}")
				raise
		return wrapped_function
```


----
## The Observer pattern

The **Observer pattern** is useful for *state monitoring* and *event handling* situations. This pattern allows a given *object* to be *monitored* by an *unknown* and *dynamic group* of *observer objects*. The core *object* being *observed* needs to implement an *interface* that makes it *observable*.

This allows tremendous *flexibility* by *decoupling* the *response* to a **state change** from the *change itself*.
In python can *notify* objects with `__call__()` .
**Examples**: GUI applications , cloud-base application 

```python
from typing import Protocol, List  
  
  
class Observer(Protocol):  
    def __call__(self, *args, **kwargs) -> None:  
        ...  
  
class Observable:  
    def __init__(self):  
        self._observers: List[Observer] = []  
  
    def attach(self, observer: Observer) -> None:  
        self._observers.append(observer)  
  
    def detach(self, observer: Observer) -> None:  
        self._observers.remove(observer)  
    def _notify_observers(self, *args, **kwargs) -> None:  
        for observer in self._observers:  
            observer(*args, **kwargs)  
  
  
Hand = List[int]  
class ZonkHandHistory(Observable):  
    def __init__(self, player: str, dice_set: Dice) -> None:  
        super().__init__()  
        self.player = player  
        self.dice_set = dice_set  
        self.rolls: list[Hand]  
  
     def start(self) -> Hand:  
         self.dice_set.roll()  
         self.rolls = [self.dice_set.dice]  
         self._notify_observers() # State change  
         return self.dice_set.dice  
  
     def roll(self) -> Hand:  
         self.dice_set.roll()  
         self.rolls.append(self.dice_set.dice)  
         self._notify_observers() # State change  
         return self.dice_set.dice  
         
         
class SaveZonkHand(Observer):  
     def __init__(self, hand: ZonkHandHistory) -> None:  
         self.hand = hand  
         self.count = 0  
  
     def __call__(self) -> None:  
         self.count += 1  
  
         message = {  
             "player": self.hand.player,  
             "sequence": self.count,  
             "hands": json.dumps(self.hand.rolls),  
             "time": time.time(),  
         }  
         print(f"SaveZonkHand {message}")
```



---
## The Strategy pattern

The **Strategy pattern** is a common demonstration of *abstraction* in *object-oriented programming*. The pattern implements *different solutions* to a *single problem*, each in a different *object*. The *core class* can then choose the most appropriate implementation *dynamically* at *runtime*.
```python
import abc  
from pathlib import Path  
from typing import Tuple  
  
from PIL import Image  
  
Size = Tuple[int, int]  
  
class FillAlgorithm(abc.ABC):  
    @abc.abstractmethod  
    def make_background(self, image_file: Path, desktop_size: Size) -> Image:  
        pass  
        
class TiledStrategy(FillAlgorithm):  
     def make_background(  
         self,  
         img_file: Path,  
         desktop_size: Size  
         ) -> Image:  
         in_img = Image.open(img_file)  
         out_img = Image.new("RGB", desktop_size)  
         num_tiles = [o // i + 1 for o, i in zip(out_img.size, in_img.size)]  
         for x in range(num_tiles[0]):  
            for y in range(num_tiles[1]):  
                 out_img.paste(  
                 in_img,  
                 (  
                 in_img.size[0] * x,  
                 in_img.size[1] * y,  
                 in_img.size[0] * (x + 1),  
                 in_img.size[1] * (y + 1),  
                 ),  
             )  
         return out_img  
  
class Resizer:  
     def __init__(self, algorithm: FillAlgorithm) -> None:  
         self.algorithm = algorithm  
     def resize(self, image_file: Path, size: Size) -> Image:  
         result = self.algorithm.make_background(image_file, size)  
         return result
```

### Strategy in Python

These **strategy classes** each define *objects* that do nothing but provide a *single method*. We could just as easily *call* that function `__call__ `and make the *object callable* directly. Since there is no other data associated with the *object*, we need do no more than create a set of *top-level functions* and pass them around as our *strategies instead*.

```python
FillAlgorithm = Callable[[Image, Size], Image]

class CenterdStrategy(FillAlgorithm): ...
```

Because we have a choice between an *abstract class* and a *type hint*, the **Strategy design pattern** seems *superfluous*. This leads to an odd conversation, starting with **"Because Python has first-class functions, the Strategy pattern is unnecessary."**

---
## The Command pattern

When we think about *class responsibilities*, we can sometimes distinguish *"passive" classes* that hold *objects* and *maintain* an *internal state*, but don't *initiate* very much, and *"active" classes* that reach out into other *objects* to take *action* and *do things*.

The **Command pattern** generally involves a *hierarchy* of *classes* that each do *something*. A **Core class** can create a *command* (or a *sequence* of *commands*) to carry out *actions*.

```python
from __future__ import annotations  
import abc  
import random  
import re  
from typing import cast, Type
  
class Adjustment(abc.ABC):  
    def __init__(self, amount: int) -> None:  
        self.amount = amount  
  
    @abc.abstractmethod  
    def apply(self, dice: "Dice"):  
        pass  
  
class Roll(Adjustment):  
    def __init__(self, n: int, d: int) -> None:  
        self.n = n  
        self.d = d  
    def apply(self, dice: "Dice") -> None:  
        dice.dice = sorted(  
            random.randint(1, self.d) for _ in range(self.n)  
        )  
        dice.modifier = 0  
  
  
class Drop(Adjustment):  
    def apply(self, dice: "Dice") -> None:  
        dice.dice = dice.dice[self.amount:]  
  
class Keep(Adjustment):  
    def apply(self, dice: "Dice") -> None:  
        dice.dice = dice.dice[:self.amount]  
  
class Plus(Adjustment):  
    def apply(self, dice: "Dice") -> None:  
        dice.modifier += self.amount  
  
class Minus(Adjustment):  
    def apply(self, dice: "Dice") -> None:  
        dice.modifier += self.amount  
  
  
  
class Dice:  
    def __init__(self, n: int, d: int, *adj: Adjustment) -> None:  
        self.adjustment = [cast(Adjustment, Roll(n, d))] + list(adj)  
        self.dice: list[int]  
        self.modifier: int  
  
    def roll(self) -> int:  
        for a in self.adjustment:  
            a.apply(self)  
        return sum(self.dice) + self.modifier  
  
    @classmethod  
    def from_text(cls, dice_text: str) -> "Dice":  
        dice_pattern = re.compile(r"(?P<n>\d*)d(?P<d>\d+)(?P<a>[dk+-]\d+)*")  
        adjustment_patter = re.compile(r"([dk+-])(\d+)")  
        adj_class: dict[str, Type[Adjustment]] = {  
            "d": Drop,  
            "k": Keep,  
            "+": Plus,  
            "-": Minus,  
        }  
        if (dice_match := dice_pattern.match(dice_text)) is None:  
            raise ValueError(f"Dice '{dice_text}' does not match pattern")  
        n = int(dice_match.group("n")) if dice_match.group("n") else 1  
        d = int(dice_match.group("d"))  
        adjustment_matches = adjustment_patter.finditer(dice_match.group("a") or "")  
        adjustments = [  
            adj_class[a.group(1)](int(a.group(2)))  
            for a in adjustment_matches  
        ]  
        return cls(n, d, *adjustments)
```

- This design allow us to manually create an instance:
```python
dice.Dice(4, dice.D6, dice.Keep(3))
# or
dice.Dice.from_text("4d6k3")
```


---
## The State pattern

The **State pattern** is structurally similar to the *Strategy pattern*, but its intent and purpose are very different. 
The goal of the **State pattern** is to represent *state transition* *systems*: *systems* where an *object's* *behavior* is constrained by the *state* it's in, and there are narrowly defined *transitions* to other *states*.

To make this work, we need a *manager* or *context class* that provides an *interface* for *switching* *states*.
Internally, this *class* contains a *pointer* to the *current state*. Each *state* knows what other *states* it is allowed to be in and will *transition* to those *states* depending on the actions invoked upon it.


>[!IMPORTANT]
>The **State pattern** *decomposes* the *problem* into two types of *classes*: the *Core class* and multiple *State classes*. The *Core class* maintains the **current state**, and *forwards* actions to a *current state object*. The *State objects* are typically **hidden** from any other *objects* that are calling the *Core object*; it acts like a *black box* that happens to perform *state management internally*.


```python
  
from typing import Iterable, Iterator, cast  
  
  
class NMEAState:  
    def __init__(self, message: "Message") -> None:  
        self.message = message  
  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        return self  
  
    def valid(self) -> bool:  
        return False  
  
    def __repr__(self) -> str:  
        return f"{self.__class__.__name__}({self.message})"  
  
  
class Waiting(NMEAState):  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        if input_ == ord(b"$"):  
            return Header(self.message)  
        return self  
  
class Header(NMEAState):  
    def __init__(self, message: "Message") -> None:  
        super().__init__(message)  
        self.message.reset()  
  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        if input_ == ord(b"$"):  
            return Header(self.message)  
        size = self.message.body_append(input_)  
        if size == 5:  
            return Body(self.message)  
        return self  
  
class Body(NMEAState):  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        if input_ == ord(b"$"):  
            return Header(self.message)  
        if input_ == ord(b"*"):  
            return CheckSum(self.message)  
        self.message.body_append(input_)  
        return self  
  
class CheckSum(NMEAState):  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        if input_ == ord(b"$"):  
            return Header(self.message)  
        if input_ in {ord(b"\n"), ord(b"\t")}:  
            # incomplete checksum ... will be invalid  
            return End(self.message)  
        size = self.message.body_append(input_)  
        if size == 2:  
            return End(self.message)  
        return self  
  
class End(NMEAState):  
    def feed_bytes(self, input_: int) -> "NMEAState":  
        if input_ == ord(b"$"):  
            return Header(self.message)  
        elif input_ in {ord(b"\n"), ord(b"\t")}:  
            return Waiting(self.message)  
        return self  
  
    def valid(self) -> bool:  
        return self.message.valid  
  
######################################################################################
class Message:  
    def __init__(self) -> None:  
        self.body = bytearray(80)  
        self.checksum_source = bytearray(2)  
        self.body_len = 0  
        self.checksum_len = 0  
        self.checksum_computed = 0  
  
    def reset(self) -> None:  
        self.body_len = 0  
        self.checksum_len = 0  
        self.checksum_computed = 0  
  
    def body_append(self, input_: int) -> int:  
        self.body[self.body_len] = input_  
        self.body_len += 1  
        self.checksum_computed ^= input_  
        return self.body_len  
  
    def checksum_append(self, input_: int) -> int:  
        self.checksum_source[self.checksum_len] = input_  
        self.checksum_len += 1  
        return self.checksum_len  
  
    @property  
    def valid(self) -> bool:  
        return (  
                self.checksum_len == 2 and int(self.checksum_source, 16) == self.checksum_computed  
        )  
######################################################################################
  
class Reader:  
    def __init__(self) -> None:  
        self.buffer = Message()  
        self.state: NMEAState = Waiting(self.buffer)  
  
    def read(self, source: Iterable[bytes]) -> Iterator[Message]:  
        for byte in source:  
            self.state = self.state.feed_bytes(cast(int, byte))  
            if self.buffer.valid:  
                yield self.buffer  
                self.buffer = Message()  
                self.state = Waiting(self.buffer)
```


>[!NOTE]
> `^` *exclusive OR* mean one or the other but not both


### State VS Strategy

These two patterns are similar because they both *delegate* work to *other objects*. This *decomposes* a *complex* *problem* into several closely related but *simpler problems*. The **Strategy pattern** is used to choose an *algorithm* at *runtime*; generally, only one of those *algorithms* is going to be chosen for a particular *use case*. The idea here is to provide an implementation choice at *runtime*, as late in the design process as possible. *Strategy class* definitions are *rarely* *aware* of *other implementations*; each *Strategy* generally *stands alone*.
The **State pattern**, on the other hand, is designed to allow *switching* between different *states dynamically*, as some *process* evolves.


---
## The Singleton pattern

**Singleton pattern** is to allow exactly *one instance* of a certain *object* to exist.
```sh
>>> class OneOnly:
	... _singleton = None
	... def __new__(cls, *args, **kwargs):
		... if not cls._singleton:
			... cls._singleton = super().__new__(cls, *args, **kwargs)
	... return cls._singleton
```