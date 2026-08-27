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
- Dataclasses & Slots
    - Implemented in `lomu/library/track.py`
    - This is basically like a struct
    - A class purely for holding data, and using slots for memory optimization
- General Terms
    - Resourced Managed Player Client (RPMC)
    - Music Player Daemon (MPD): Server that plays music; clients connect to it
    - Music Player Client (MPC): CLI client for controlling MPD
