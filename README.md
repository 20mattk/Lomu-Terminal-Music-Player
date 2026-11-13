# Lomu Terminal Music Player

## 📬 Background
- A personal project to build a terminal music player from scratch for fun.

## 🩻 Structure
- As of now, there exists two main directories:
    1. The main project directory
    2. The testing directory (using `pytest`)
- I've split up the main application into three parts:
    1. Library (tracks, metadata, playlists)
    2. Playback (controlling library playback)
    3. UI (terminal UI)

## ⚠️ Disclaimer
- I'm almost completely new to building something like this.
- Things are subject to change as I learn more.

## 📚 Things I've Learned
### 📝 General Things
- General Terms
    - Resourced Managed Player Client (RPMC)
    - Daemon: A process which runs in the background
    - Music Player Daemon (MPD): Server that plays music; clients connect to it
    - Music Player Client (MPC): CLI client for controlling MPD
- Version numbers (x.y.z)
    - x: major (breaking changes like API-breaking code)
    - y: minor (new features which are backwards compatible)
    - z: patch (bug fixes)
    - 0.1.0 is pre-release for features being added
    - 1.0.0 is first v1 stable release
- `__init__.py`
    - Tells Python "this directory is a package"
    - Docstrings and versioning
    - Can also export key classes/functions for easier importing elsewhere
    - Enables `from lomu import Player` over `from lomu.player import Player`
### 🗂️ Types
- `from typing import Optional`
    - Like Optionals in Swift
    - A value can be of a certain type, or `None`
    - `var: Optional[int] = None`
- Named Constants (`Enum`)
    - Implemented in `lomu/library/track.py`
    - Learned how to create safe, type-checked constants
    - To ensure type safety from string values
    - Was used for my file audio types
- Iterable
    - Something you can loop over
    - An object which you can get an iterator from by using `iter(obj)`
    - Example: a list of numbers
- Iterator
    - An object which produces values one at a time, remembers its progress, and is itself iterable
    - `list(nums_list)` "consumes" an iterable, collecting all of its items and leaving the iterator exhausted
    - `[nums_list]` does NOT "consume" an iterable - it just puts it inside of a list where the items are not collected
    - `next(iterator)` advances the iterator and returns the next value
    - Example: `items = [1, 2, 3]  # iterable`
    - Example: `it = iter(items)  # iterator`
### 🗃️ Classes
- Factory Methods
    - Implemented in `lomu/library/metadata.py`
    - This was a design pattern I wasn't even aware of before this project
    - Client, Product, Concrete Implementation, Creator, Factory Method
    - A Client wants a Product from the Creator
    - The Creator executes its Factory Method
    - The Factory Method decides which Concrete Implementation to return
    - An interface asks others to provide a Concrete Implementation
- Dataclasses (Slots & Frozen)
    - Implemented in `lomu/library/track.py`
    - This is basically like a struct - purely for holding data
    - Slots reduce memory footprint by eliminating the dynamic dictionary
    - Frozen for object ummutability (safer to freeze an audio track's data)
- `object.__setattr__()`
    - Allows you to dynamically set attributes of an object
    - Even if that object is frozen
- `abc`, `ABC`, `@abstractmethod`
    - Abstract Base Class is one that cannot be instantiated from
    - `class ClassName(ABC): ...`
    - It can only be inhereted from, because it defines an interface
    - `@abstractmethod` is one that MUST be defined by an implementation class
    - The child class will throw an error if `@abstractmethod` is not defined
- `@classmethod`
    - Turns that method into one that receives the CLASS
    - Instead of the instance
- `@staticmethod`
    - A static method belongs to the class itself, not to any isntance
    - However, it does need an instance or class state
    - A pure utility function that takes input and returns output
- `@property`
    - A method decorator to call the method like an attribute
    - Can use to return immutable or private internal attributes in the body
    - To protect or hide internal data
    - Can also be used to return "computed properties" where the value must be computed in the body each time you call for it
### 🧪 Testing
- Unit/Integration Testing
    - Implemented in `tests/`
    - I learned some basics of unit/integration testing using `pytest`
    - Also learning `pytest` fixtures
    - There was a lot more I could've done with mocking
- `pytest`
    - You don't run the steering wheel, you run the whole car
    - `pytest` is a testing framework
    - Helps automate testing of all features, so you don't need to remember
    - Looks for files that match `test_*.py`
    - Runs all functions `def test_...`
    - Collects assertions and reports which ones failed
- `pytest` Fixtures
    - Reusable setup code
    - Define a function with a `@pytest.fixture` decorator
    - In the function body, define data to return (like `Track` class instance)
    - Tests that need that data will use the function name as an argument
    - Fixture name: `def track(): ...`
    - Pass in fixture: `def test_...(track): ...`
    - `pytest` sees the fixture in the test's args, then calls the fixture
    - The returned data is then available in the test as the fixture's name
    - Does dependancy injection for you
- `assert`
    - Syntax: `assert <any Python statement or code>`
    - If true, nothing happens, if false, raises an `AssertionError`
### 🧶 Threading
- Thread
    - An independent path of execution inside one process
- Daemon
    - A process that runs in the background
- Python Non-Daemonic Thread (Default)
    - A program will wait for non-daemon threads to complete before it exits
    - `x = threading.Thread(target=thread_function, args=(1,))`
- Python Daemon Thread
    - A daemon thread will shut down immediately when the program exits
    - The program does not wait for a dameon thread to complete
    - `x = threading.Thread(target=thread_function, args=(1,), daemon=True)`
- `threading._shutdown()`
    - Python `threading` library waits for every running thread that doesn’t have the daemon flag set to finish
- `x.join()`
    - To tell one thread to "wait here" for another thread to finish
    - Like telling the main thread to wait until the `x` thread has finished to proceed with the rest of its own execution
    - The statement will wait until either kind of thread (daemon or not) is finished
- Race Condition
    - A flaw in concurrent code
    - Where the outcome depends on the relative timing or interleaving of multiple threads or processes that access shared state, when at least one of them writes to it
    - Like multiple threads writing to the value of a credit card balance or something
- Locking
    - Only one thread at a time can have the Lock (`threading.Lock()`)
    - Any other thread that wants the Lock must wait until the owner of the Lock gives it up
    - Done via `.acquire()` and `.release()`, or as a context manager using `with`
- Deadlock
    - An implementation bug where a Lock is not released properly
    - A design issue where a utility function needs to be called by functions that might or might not already have the Lock