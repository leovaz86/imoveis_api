
import argparse
import pandas as pd
from utils import geocode, haversine_km
from provider_vivareal import search_vivareal

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--endereco", required=True, help="Endereço do imóvel avaliado")
    p.add_argument("--vivareal_url", required=True, help="URL filtrada do VivaReal (bairro/tipo/area etc.)")
    p.add_argument("--radius_km", type=float, default=1.0)
    p.add_argument("--saida", default="saida.csv")
    args = p.parse_args()

    subj = geocode(args.endereco)
    if not subj:
        raise SystemExit("Falha ao geocodificar endereço do sujeito.")
    subj_lat, subj_lon = subj

    listings = search_vivareal(args.vivareal_url)

    rows = []
    for it in listings:
        addr = it.get("address")
        if not addr:
            continue
        coords = geocode(addr + ", Porto Alegre, RS, Brasil")
        if not coords:
            continue
        lat, lon = coords
        dist = haversine_km(subj_lat, subj_lon, lat, lon)
        if dist <= args.radius_km:
            feats = it.get("features") or {}
            preco = it.get("price_brl")
            area = feats.get("area_m2")
            preco_m2 = round(preco/area, 2) if (preco and area and area>0) else None
            rows.append({
                "provider": it.get("provider"),
                "titulo": it.get("title"),
                "endereco": addr,
                "dist_km": round(dist,3),
                "preco_brl": preco,
                "dorms": feats.get("dorms"),
                "suites": feats.get("suites"),
                "banheiros": feats.get("banheiros"),
                "vagas": feats.get("vagas"),
                "area_m2": area,
                "preco_m2": preco_m2,
                "url": it.get("url"),
            })

    df = pd.DataFrame(rows).sort_values(by=["dist_km"])
    # Linha final de média do m²
    if not df.empty and df["preco_m2"].notna().any():
        media = round(df["preco_m2"].dropna().mean(), 2)
        avg_row = {c: None for c in df.columns}
        avg_row["titulo"] = "MÉDIA m²"
        avg_row["preco_m2"] = media
        df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df.to_csv(args.saida, index=False, encoding="utf-8-sig")
    print(f"Gerado: {args.saida} ({len(df)} linhas)")

if __name__ == "__main__":
    main()
