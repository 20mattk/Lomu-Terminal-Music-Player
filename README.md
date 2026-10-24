# Lomu Terminal Music Player

## Background
- A personal project to build a terminal music player from scratch for fun.

## Structure
- As of now, there exists two main directories:
    1. The main project directory
    2. The testing directory (using `pytest`)
- I've split up the main application into three parts:
    1. Library (tracks, metadata, playlists)
    2. Playback (controlling library playback)
    3. UI (terminal UI)

## Disclaimer
- I'm almost completely new to building something like this.
- Things are subject to change as I learn more.

## Things I've Learned
### General Things
- General Terms
    - Resourced Managed Player Client (RPMC)
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
### Types
- `from typing import Optional`
    - Like Optionals in Swift
    - A value can be of a certain type, or `None`
    - `var: Optional[int] = None`
- Named Constants (`Enum`)
    - Implemented in `lomu/library/track.py`
    - Learned how to create safe, type-checked constants
    - To ensure type safety from string values
    - Was used for my file audio types
### Classes
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
### Testing
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