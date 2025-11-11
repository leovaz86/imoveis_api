
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def _int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None

def _price(s):
    s = re.sub(r"[^0-9]", "", s or "")
    return int(s) if s else None

def search_vivareal(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a.property-card__content-link")
    results = []
    seen = set()
    for a in cards:
        href = a.get("href")
        if not href:
            continue
        if href.startswith("/"):
            href = "https://www.vivareal.com.br" + href
        if href in seen:
            continue
        seen.add(href)
        card = a.find_parent(class_="property-card__container")
        if not card:
            continue
        addr_el = card.select_one(".property-card__address")
        addr = addr_el.get_text(" ", strip=True) if addr_el else None
        price_el = card.select_one(".property-card__price")
        price = _price(price_el.get_text(" ", strip=True) if price_el else None)
        feats = {"dorms":None,"banheiros":None,"suites":None,"vagas":None,"area_m2":None}
        for li in card.select(".property-card__details li"):
            t = li.get_text(" ", strip=True).lower()
            if "m²" in t: feats["area_m2"]=_int(t)
            elif "suíte" in t or "suite" in t: feats["suites"]=_int(t)
            elif "quarto" in t or "dorm" in t: feats["dorms"]=_int(t)
            elif "banheiro" in t: feats["banheiros"]=_int(t)
            elif "vaga" in t: feats["vagas"]=_int(t)
        results.append({
            "provider": "VivaReal",
            "title": a.get_text(strip=True),
            "address": addr,
            "url": href,
            "price_brl": price,
            "features": feats
        })
    return results
