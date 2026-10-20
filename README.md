# Terminal Territories

*A multiplayer terminal-based strategy game designed to teach networking, APIs, data modelling, concurrency, and distributed systems concepts through incremental development.*

## The Elevator Pitch

Players connect to a central server and compete to control territory on a shared map.

Everything happens in a terminal window.

At first it's a simple turn-based game using a REST API. As the project grows, the networking becomes increasingly real-time until juniors are dealing with sockets, server authority, UDP updates, prediction, and synchronisation.

The clever part is that every new programming concept naturally emerges from a game feature.

---

# Teaching Goals

Rather than teaching technologies directly:

> "Today we're learning Flask."

You teach through problems:

> "Players keep overwriting each other's moves. How do we fix it?"

Which leads naturally to:

- REST APIs
- JSON
- Client/server architecture
- Authentication
- State machines
- Database persistence
- Threading
- Async programming
- TCP sockets
- UDP networking
- Event processing
- Distributed systems concepts
- Cheat prevention

---

# Core Gameplay

The world is a rectangular grid.

```text
+----------------+
| A A . . B B B |
| A A . . B B B |
| A . . C C B B |
| . . C C C C . |
| D D D C E E E |
| D D D . E E E |
+----------------+
```

Each letter represents territory ownership.

Each player starts with:

- One capital tile
- Limited resources
- Limited actions per turn

Goal:

- Control the highest percentage of the map after N turns.
- Or eliminate all opponents.

---

# Territories

```json
{
  "owner": "alex",
  "strength": 5,
  "resources": 20,
  "terrain": "plains"
}
```

---

# Basic Actions

## Expand
Claim an adjacent unowned tile.

## Fortify
Increase defensive strength.

## Attack
Attack adjacent enemy territory.

---

# Development Roadmap

## Version 1: REST API

Endpoints:

```http
GET /map
GET /player
POST /move
POST /attack
```

Concepts:

- HTTP
- REST
- JSON
- Validation

## Version 2: Persistence

Add a database.

Concepts:

- SQL
- ORM usage
- Data modelling

## Version 3: Fog of War

Server controls visibility.

Concepts:

- Server authority
- Security
- Data filtering

## Version 4: Real-Time Updates

Move from polling to WebSockets.

## Version 5: Alliances

Add diplomacy, trading and shared vision.

## Version 6: TCP Rewrite

Replace REST with a custom TCP protocol.

## Version 7: UDP Battlefield Mode

Teach:

- Packet loss
- Reliability
- Sequence numbers
- Reconciliation

## Version 8: Economy Layer

Resource-producing terrain and simulation loops.

## Version 9: AI Players

Introduce bot opponents and decision-making algorithms.

## Version 10: Distributed Architecture

Split into:

- Game Server
- Auth Server
- Chat Server
- Leaderboard Server

---

# Terminal UI

```text
+------------------------------------+
| Terminal Territories               |
+------------------------------------+
| Map                                |
|                                    |
| A A A . B B                        |
| A A . . B B                        |
| A . . C C C                        |
|                                    |
+------------------------------------+
| Resources: 42                      |
| Territory: 12                      |
| Commands:                          |
| [E]xpand [A]ttack [F]ortify        |
+------------------------------------+
```

Suggested stack:

- Python
- FastAPI
- SQLite
- Textual
- WebSockets
- TCP sockets
- UDP combat mode

---

# Why It Works

The biggest strength of Terminal Territories is that every engineering problem emerges naturally from gameplay. Instead of building another CRUD application, junior developers are motivated by a multiplayer game while learning many of the skills used in modern backend and distributed systems development.
