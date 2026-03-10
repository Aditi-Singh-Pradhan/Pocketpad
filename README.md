# PocketPad 

Turn your phone into a wireless trackpad using WebSockets.

Open a webpage on your phone, drag your finger, and your PC mouse follows in real time — no app install needed.

---

## How It Works

- A Python WebSocket server runs on your PC
- You open `index.html` on your phone's browser
- Touch movement is streamed to the server, which moves the mouse via `pyautogui`

---

## Requirements

- Python 3.7+
- Your phone and PC on the **same WiFi network**

Install dependencies:

```bash
pip install websockets pyautogui
```

---

## Usage

### 1. Find your PC's local IP

**Windows:**
```bash
ipconfig
```
**Mac/Linux:**
```bash
ifconfig
```
Look for something like `192.168.x.x` or `10.x.x.x`

### 2. Update the IP in `index.html`

```javascript
const ws = new WebSocket("ws://YOUR_PC_IP:8765");
```

### 3. Start the server

```bash
python Server.py
```

### 4. Open `index.html` on your phone

You can serve it quickly with:

```bash
python -m http.server 8765
```

Then visit `http://YOUR_PC_IP:8765` in your phone's browser.

Drag your finger on the screen — your mouse will follow.

---

## Roadmap

- [ ] Click & right-click support
- [ ] Scroll gesture
- [ ] Visual UI on phone
- [ ] Auto-detect server IP
- [ ] Packaging for easy setup

---

## Built With

- [websockets](https://websockets.readthedocs.io/) — async WebSocket server
- [pyautogui](https://pyautogui.readthedocs.io/) — mouse control
