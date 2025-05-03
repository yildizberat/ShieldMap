from mitmproxy import http
from urllib.parse import urlparse
import json
from pathlib import Path

# Kaydedilecek JSON dosyası
CSP_FILE = Path("shared/csp_suggestions.json")

# İlk ziyaret edilen domain merkezi olacak
origin_domain = None

# Kaynak türlerine göre domain'leri grupluyoruz
domains = {
    "script-src": set(),
    "style-src": set(),
    "img-src": set(),
    "connect-src": set(),
    "default-src": set()
}

def save():
    data = {
        "origin": origin_domain or "unknown.local",
        "categories": {k: sorted(list(v)) for k, v in domains.items()}
    }
    CSP_FILE.parent.mkdir(parents=True, exist_ok=True)
    CSP_FILE.write_text(json.dumps(data, indent=2))
    print("[✔] CSP suggestions saved to", CSP_FILE)

def request(flow: http.HTTPFlow):
    global origin_domain

    parsed = urlparse(flow.request.pretty_url)
    domain = parsed.netloc
    path = parsed.path.lower()

    # İlk domain'i merkez olarak ata
    if origin_domain is None:
        origin_domain = domain
        print(f"[✔] Origin set to: {origin_domain}")

    # Kaynak türüne göre sınıflandır
    if path.endswith(".js"):
        domains["script-src"].add(domain)
    elif path.endswith(".css"):
        domains["style-src"].add(domain)
    elif any(path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]):
        domains["img-src"].add(domain)
    elif "api" in path or flow.request.headers.get("content-type", "").startswith("application/json"):
        domains["connect-src"].add(domain)
    else:
        domains["default-src"].add(domain)

    # Güncel verileri dosyaya yaz
    save()