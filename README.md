# mortenskouandersen.dk — statisk website

Håndkodet website uden WordPress. Genskabt efter det gamle Divi-site
(indhold hentet fra Wayback Machine-arkivet, billeder fra den gamle
WordPress-installations `wp-content/uploads`).

## Struktur

- `index.html` — forsiden (hero-billede + titel + Facebook/Bandcamp)
- `udgivelser/`, `koncerter/`, `videoer/`, `billeder/`, `nyheder/`,
  `butik/`, `filologi/`, `om/` — sider (samme URL-struktur som det gamle site)
- `digressioner/`, `varme-haender-koldt-hjerte/`,
  `morten-skou-andersen-...-den-orange-plade/`, `5537-2/` (I fingrene),
  `brev-til-anders-breivik-...-single/` — albumsider (gamle permalinks bevaret)
- `assets/css/style.css` — al styling
- `assets/js/main.js` — mobilmenu + menu-baggrund ved scroll
- `assets/img/` — alle billeder (omdøbt til url-venlige navne)

## Sådan redigeres sitet

Du kan redigere HTML-filerne direkte. Alternativt kan alle sider
genereres fra `build.py` (fælles menu/skabelon ét sted):

    python3 build.py

Ret indholdet i `build.py` (fx nye koncerter i listen i toppen af
koncert-afsnittet) og kør scriptet igen.

## Hosting

Alt er statiske filer — upload hele mappen til en hvilken som helst
webhost (FTP/Netlify/GitHub Pages osv.). Ingen database, ingen PHP,
ingen opdateringer at vedligeholde.

Bemærk: Skrifttypen Open Sans hentes fra Google Fonts, og videoerne
indlejres fra YouTube — begge dele kræver at den besøgende er online.
