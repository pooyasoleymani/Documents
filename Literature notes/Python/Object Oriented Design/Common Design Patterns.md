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

- *decorate*with `__call__()` method:
```python
import gzip
import io

Address = Tuple[str, int]

class LoogRoller:
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
**Decorator** in python have additional options .for example *monkey-patching* changing *class definition* at *runtime* to get similar effect.
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
In python can notify objects with `__call__()` .
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
