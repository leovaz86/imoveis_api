
import argparse
from utils import geocode, haversine_km
from provider_vivareal import search_vivareal
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endereco")
    parser.add_argument("--url")
    parser.add_argument("--saida", default="saida.csv")
    args = parser.parse_args()

    subj = geocode(args.endereco)
    listings = search_vivareal({"url": args.url})
    rows=[]
    for it in listings:
        c = geocode((it.get("address") or "") + ", Porto Alegre, RS, Brasil")
        if not c: continue
        dist = haversine_km(subj[0],subj[1],c[0],c[1])
        it["distance_km"]=round(dist,3)
        rows.append(it)
    df = pd.DataFrame(rows)
    df.to_csv(args.saida, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
