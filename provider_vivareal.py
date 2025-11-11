
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def _int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None

def _price(s):
    s = re.sub(r"[^0-9]", "", s or "")
    return int(s) if s else None

def search_vivareal(query: dict):
    url = query["url"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a.property-card__content-link")
    results = []
    for a in cards:
        href = a.get("href")
        if href and href.startswith("/"):
            href = "https://www.vivareal.com.br" + href
        card = a.find_parent(class_="property-card__container")
        if not card: continue
        addr = (card.select_one(".property-card__address") or {}).get_text(" ", strip=True)
        price = _price((card.select_one(".property-card__price") or {}).get_text())
        details = card.select(".property-card__details li")
        feats = {"dorms":None,"banheiros":None,"suites":None,"vagas":None,"area_m2":None}
        for li in details:
            t = li.get_text(" ", strip=True).lower()
            if "m²" in t: feats["area_m2"]=_int(t)
            if "quarto" in t or "dorm" in t: feats["dorms"]=_int(t)
            if "banheiro" in t: feats["banheiros"]=_int(t)
            if "vaga" in t: feats["vagas"]=_int(t)
            if "suíte" in t or "suite" in t: feats["suites"]=_int(t)
        results.append({
            "provider": "VivaReal",
            "title": a.get_text(strip=True),
            "address": addr,
            "url": href,
            "price_brl": price,
            "features": feats
        })
    return results
