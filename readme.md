# 🛡️ ShieldMap

**ShieldMap** is a CSP (Content Security Policy) mapping and visualization tool that automatically collects and organizes external resource domains used by a website. It helps developers craft accurate CSP rules by inspecting network traffic through a local proxy.

Using `mitmproxy`, it captures all external JS, CSS, image, and XHR requests while visiting a website. These sources are visualized as an interactive graph using D3.js, and served via a Flask backend.

---

## 🔍 Why ShieldMap?
- Automatically identify domains needed for your CSP
- Visualize all loaded resources as a network map
- Avoid trial-and-error CSP debugging
- Helps build secure and clean front-end policies

---

## 🚀 Features

- ✅ Real-time network traffic capture with mitmproxy
- ✅ Categorizes domains into `script-src`, `img-src`, etc.
- ✅ Headless browser visits via Playwright (bypasses bot detection)
- ✅ Interactive D3.js graph with zoom, pan, hover and click effects
- ✅ Node links are clickable to open domains directly
- ✅ Logs visited domains

---

## 📦 Installation

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Usage

### 1. Start mitmproxy
```bash
mitmproxy -s csp_suggester.py --listen-port 8080
```

### 2. Visit a website (via proxy)
```bash
python visit_webapp.py -u https://example.com
```

### 3. Run the Flask visualization server
```bash
python flask_server.py
```
Then visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
shieldmap/
├── flask_server.py              # Flask backend
├── csp_suggester.py             # mitmproxy add-on script
├── visit_webapp.py              # Browser automation with Playwright
├── shared/
│   └── csp_suggestions.json     # Auto-generated CSP data
├── static/
│   └── graph.js                 # D3.js graph renderer
├── templates/
│   └── map.html                 # Web interface
├── visit_log.txt                # Domain visit logs
└── requirements.txt             # Python dependencies
```

---

## 📜 License

MIT License © 2025 — Cyber Observers Collective 😎

---

## 🤝 Contributing
Pull requests are welcome! If you’d like to add new visual modes, CSP filters, or automation capabilities, feel free to fork and build!

---

> Every domain matters. Map your web dependencies. — ShieldMap
