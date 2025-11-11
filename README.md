
# Vertex Laudos API (Railway – 1‑Click)

API simples (FastAPI) para coletar anúncios no VivaReal, calcular distância até um endereço sujeito e retornar CSV com preço/m² e média final.

## 1) Subir no Railway – do zero e sem dor

**A) Crie um repositório no GitHub**
- Nome sugerido: `vertex-laudos-api`
- Faça upload de todos os arquivos desta pasta (inclusive `Dockerfile`)

**B) Deploy no Railway**
- Acesse https://railway.app → **New Project** → **Deploy from GitHub**
- Selecione `vertex-laudos-api`
- Aguarde o build

> O Railway detecta o `Dockerfile` e executa automaticamente:
> `uvicorn api:app --host 0.0.0.0 --port 8000` (porta 8000 já exposta)

**C) Teste**
- Abra: `https://SEU-SUBDOMINIO.up.railway.app/`
- Ver `{"ok": true, ...}`
- Docs: `https://SEU-SUBDOMINIO.up.railway.app/docs`

Se `/docs` não abrir, veja os Logs. Em alguns casos, reimplantar (Deploy) resolve.

## 2) Como usar a API

### Endpoint
`POST /coletar`

### Body (JSON)
```json
{
  "endereco": "Av. do Forte, 400, Vila Jardim, Porto Alegre",
  "vivareal_url": "https://www.vivareal.com.br/venda/rs/porto-alegre/bairros/vila-jardim/casa_residencial/?quartos=2&banheiros=1&vagas=1&areaMin=72&areaMax=108",
  "radius_km": 1.0
}
```

### Resposta
```json
{ "csv": "provider,titulo,endereco,dist_km,preco_brl,..." }
```

## 3) Integração no GPT (Actions)
- OpenAPI Server URL: `https://SEU-SUBDOMINIO.up.railway.app`
- Método: `POST /coletar`
- Schema do body conforme acima.
- O GPT recebe o CSV e exibe uma tabela com preço/m² e a média na última linha.

## 4) Dicas
- Ajuste a URL do VivaReal com os filtros corretos (quartos, banheiros, vagas, área ±20% etc.).
- Para resultados “com suíte” apenas, inclua esse filtro na URL do portal (se disponível) **ou** trate no GPT para descartar sem suíte.
- Respeite limites do Nominatim (já há `sleep` 1s por requisição).
