# Pocketpad
### Wireless Trackpad for Your PC

Pocketpad turns your phone into a wireless trackpad — no apps, no Bluetooth, no extra hardware. Just your phone, your computer, and the same WiFi network.

If you've got a Samsung S Pen or any phone stylus, this is basically a free budget tablet. That S2X Ultra in your pocket? It's been a drawing tablet this whole time.


Built because I didn't want to buy an expensive drawpad ;)

---

## What It Does

Most wireless trackpad solutions need you to install an app, pair over Bluetooth, or buy hardware. Pocketpad doesn't.

Run a Python server on your PC. Open a URL on your phone's browser. Drag your finger. Your cursor moves. That's it.

---

## Features

- **Cursor movement** — drag your finger, cursor follows. Smoothed, damped, and low-latency
- **Tap to click** — single tap registers as a left click. A state machine distinguishes taps from drags
- **Two-finger scroll** — scroll up/down just like a laptop trackpad
- **Auto IP detection** — server finds its own LAN IP, no hardcoding or config files
- **Zero phone-side dependencies** — runs entirely in the browser, nothing to install on your phone
- **Typed message protocol** — extensible architecture, adding new input types is one message + one handler

---

## Tech Stack

| Layer | Technology |
|---|---|
| Server | Python, asyncio, websockets |
| Input Control | pynput |
| Client | Vanilla JS, HTML Canvas |
| Communication | WebSocket (real-time, bidirectional) |
| Networking | Auto LAN IP detection via socket |

---

## Project Structure

```
Pocketpad/
├── Server.py          — WebSocket server + event dispatcher
├── index.html         — touch input + client-side state machine
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.x
- Both devices on the same WiFi network

### Install dependencies

```bash
pip install websockets pynput
```

### Run Pocketpad

```bash
python Server.py
```

It'll print something like:

```
Server is running... Waiting for Phone to connect.
HTML served at http://10.50.6.92:8080
WebSocket running on port 8765
```

Open that URL on your phone's browser. Start dragging.

---

## How It Works

```
Phone (browser)                                    PC (Python server)
                                                          |
Touch Events                                     ConnectionState
- touchstart                                     - sensitivity
- touchmove             ──WebSocket──>           - smoothing
- touchend                                       - damping
       |                                                  |
  State Machine                                    Dispatcher
  - idle                                          - handle_move()
  - waiting              {type, dx, dy}           - handle_click()
  - moving               {type, button}           - handle_scroll()
  - scrolling            {type, scroll_y}                 |
                                                     pynput
                                                  Mouse Controller
                                                  - move()
                                                  - click()
                                                  - scroll()
```

---

## Message Protocol

All messages follow a typed JSON schema. The server reads `type` first, then routes to the right handler.

| Type | Fields | Action |
|---|---|---|
| `move` | `dx`, `dy` | Move cursor with smoothing + damping |
| `click` | `button` | Left or right click |
| `scroll` | `scroll_x`, `scroll_y` | Vertical/horizontal scroll |

Adding a new input type = one new message + one new method on `ConnectionState`.

---

## Client-Side State Machine

```
IDLE ──touchstart──> WAITING
WAITING ──moved > threshold──> MOVING (send dx/dy)
WAITING ──touchend (barely moved)──> send click ──> IDLE
MOVING ──touchend──> IDLE
WAITING ──2nd finger──> SCROLLING
SCROLLING ──touchend──> IDLE
```

The state machine solves the core problem: how do you tell the difference between a tap (click) and a drag (move)? You wait and see what happens after `touchstart`.

---

## Roadmap

- [x] Core cursor movement over WebSocket
- [x] Smoothing & damping for natural feel
- [x] Typed message protocol + dispatcher architecture
- [x] pynput swap (lower latency than pyautogui)
- [x] Auto LAN IP detection
- [x] Tap to click (state machine)
- [x] Two-finger scroll
- [ ] S Pen barrel button → drag/draw mode
- [ ] Right click (two-finger tap or long press)
- [ ] Three-finger gestures
- [ ] Keyboard input overlay
- [ ] Pressure sensitivity for stylus users

---

## Why pynput over pyautogui?

pyautogui adds a built-in 0.1s pause after every action — that's 100ms of artificial latency on every mouse move. For a trackpad sending 60+ events per second, that kills responsiveness. pynput has no such delay.

---

## Author

Aditi Singh Pradhan
1st Year B.E. Computer Science — BITS Goa + RMIT (2+2 degree)