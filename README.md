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
- Factory Methods
    - Implemented in `lomu/library/metadata.py`
    - This was a design pattern I wasn't even aware of before this project
    - Client, Product, Concrete Implementation, Creator, Factory Method
    - A Client wants a Product from the Creator
    - The Creator executes its Factory Method
    - The Factory Method decides which Concrete Implementation to return
    - An interface asks others to provide a Concrete Implementation
- Unit/Integration Testing
    - Implemented in `tests/`
    - I learned some basics of unit/integration testing using `pytest`
    - Also learning `pytest` fixtures
    - There was a lot more I could've done with mocking
- Dataclasses (Slots & Frozen)
    - Implemented in `lomu/library/track.py`
    - This is basically like a struct - purely for holding data
    - Slots reduce memory footprint by eliminating the dynamic dictionary
    - Frozen for object ummutability (safer to freeze an audio track's data)
- Named Constants (`Enum`)
    - Implemented in `lomu/library/track.py`
    - Learned how to create safe, type-checked constants
    - To ensure type safety from string values
    - Was used for my file audio types
- General Terms
    - Resourced Managed Player Client (RPMC)
    - Music Player Daemon (MPD): Server that plays music; clients connect to it
    - Music Player Client (MPC): CLI client for controlling MPD
- `abc`, `ABC`, `@abstractmethod`
    - Abstract Base Class is one that cannot be instantiated from
    - `class ClassName(ABC): ...`
    - It can only be inhereted from, because it defines an interface
    - `@abstractmethod` is one that MUST be defined by an implementation class
    - The child class will throw an error if `@abstractmethod` is not defined
- `from typing import Optional`
    - Like Optionals in Swift
    - A value can be of a certain type, or `None`
    - `var: Optional[int] = None`
- `@classmethod`
    - Turns that method into one that receives the CLASS
    - Instead of the instance
- `@staticmethod`
    - A static method belongs to the class itself, not to any isntance
    - However, it does need an instance or class state
    - A pure utility function that takes input and returns output
- `__init__.py`
    - Tells Python "this directory is a package"
    - Docstrings and versioning
    - Can also export key classes/functions for easier importing elsewhere
    - Enables `from lomu import Player` over `from lomu.player import Player`