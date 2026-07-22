#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for mortenskouandersen.dk — statisk site uden WordPress.
Kør: python3 build.py  (skriver HTML-filer i samme mappe)"""
import os
import json


ROOT = os.path.dirname(os.path.abspath(__file__))

def load_data(name, default):
    """Indlæs redigerbart indhold fra data/<name>.json (admin-siden skriver dem)."""
    try:
        with open(os.path.join(ROOT, "data", name + ".json"), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

NAV = [
    ("Forside", ""),
    ("Udgivelser", "udgivelser/"),
    ("Koncerter", "koncerter/"),
    ("Videoer", "videoer/"),
    ("Billeder", "billeder/"),
    ("Nyheder", "nyheder/"),
    ("Butik", "butik/"),
    ("Filologi", "filologi/"),
    ("Om", "om/"),
]

def page(slug, title, body, extra_head="", body_class=""):
    """slug '' = forside (root), ellers mappe-navn. Returnerer (sti, html)."""
    depth = 0 if slug == "" else 1
    pre = "../" * depth
    nav_items = []
    for label, href in NAV:
        target = pre if href == "" else pre + href
        if target == "":
            target = "./"
        active = ' class="current"' if href == (slug + "/" if slug else "") else ""
        nav_items.append(f'<li{active}><a href="{target}">{label}</a></li>')
    nav_html = "\n          ".join(nav_items)
    html = f"""<!DOCTYPE html>
<html lang="da">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}assets/css/style.css">
{extra_head}</head>
<body class="{body_class}">
  <header id="site-header">
    <nav>
      <button id="menu-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul id="top-menu">
          {nav_html}
      </ul>
    </nav>
  </header>
{body}
  <script src="{pre}assets/js/main.js"></script>
</body>
</html>
"""
    path = os.path.join(ROOT, slug, "index.html") if slug else os.path.join(ROOT, "index.html")
    return path, html

pages = []

# ---------------------------------------------------------------- FORSIDE
pages.append(page("", "Morten Skou Andersen – &de mennesker han normalt sammenligner sig med", """
  <section class="hero" style="background-image:url('assets/img/forside-hero.jpg')">
    <div class="hero-inner">
      <h1>Morten Skou Andersen</h1>
      <p class="hero-sub">&amp; de mennesker han normalt sammenligner sig med</p>
      <p class="hero-buttons">
        <a class="btn" href="https://www.facebook.com/mortenskouandersen">Facebook</a>
        <a class="btn" href="https://mortenskouandersen.bandcamp.com/">Bandcamp</a>
      </p>
    </div>
  </section>
""", body_class="home"))

# ---------------------------------------------------------------- UDGIVELSER
_udg = load_data("udgivelser", {"album": [], "single": []})

def release_item(r):
    title, sub, img, href = r.get("title", ""), r.get("sub", ""), r.get("img", ""), r.get("href")
    cover = f'<img src="../assets/img/covers/{img}" alt="{title} – cover" loading="lazy">'
    if href:
        return f"""      <a class="release" href="{href}">
        {cover}
        <span class="release-info"><span class="release-title">{title}</span><span class="release-sub">{sub}</span></span>
      </a>"""
    return f"""      <div class="release">
        {cover}
        <span class="release-info"><span class="release-title">{title}</span><span class="release-sub">{sub}</span></span>
      </div>"""

_udg_body = ""
if _udg.get("album"):
    rel_html = "\n".join(release_item(r) for r in _udg["album"])
    _udg_body += f"""    <h1 class="page-header">ALBUM</h1>
    <div class="releases">
{rel_html}
    </div>
"""
if _udg.get("single"):
    sin_html = "\n".join(release_item(r) for r in _udg["single"])
    _udg_body += f"""    <h1 class="page-header">SINGLE</h1>
    <div class="releases">
{sin_html}
    </div>
"""
pages.append(page("udgivelser", "Udgivelser – Morten Skou Andersen", f"""
  <main class="content">
{_udg_body.rstrip()}
  </main>
"""))

# ---------------------------------------------------------------- KONCERTER
def K(date, venue, extra=None):
    out = f'      <p class="gig"><span class="gig-date">{date}</span><br>{venue}'
    if extra:
        out += "<br>" + extra
    return out + "</p>"

_gigs = load_data("koncerter", [])
gigs_html = "\n".join(K(g.get("date", ""), g.get("venue", ""), g.get("extra") or None) for g in _gigs)
pages.append(page("koncerter", "Koncerter – Morten Skou Andersen", f"""
  <main class="content narrow">
    <h1 class="page-header">KONCERTER</h1>
{gigs_html}
    <p class="gig-end"><em>Længere tilbage går historikken ikke.</em></p>
  </main>
"""))

# ---------------------------------------------------------------- VIDEOER
_videos = load_data("videoer", [])

def video_cell(v):
    t = v.get("title", "")
    if v.get("youtube"):
        frame = f'<iframe src="https://www.youtube.com/embed/{v["youtube"]}" title="{t}" loading="lazy" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>'
    else:
        frame = f'<video controls preload="metadata" src="../{v.get("file", "")}"></video>'
    return f"""      <div class="video-cell">
        <p class="video-title">{t}</p>
        <div class="video-frame">{frame}</div>
      </div>"""

vid_html = "\n".join(video_cell(v) for v in _videos)
pages.append(page("videoer", "Videoer – Morten Skou Andersen", f"""
  <main class="content">
    <h1 class="page-header">VIDEOER</h1>
    <div class="video-grid">
{vid_html}
    </div>
  </main>
"""))

# ---------------------------------------------------------------- BILLEDER
G = "../assets/img/galleri/"

def img(f, alt=""):
    return f'<img src="{G}{f}" alt="{alt}" loading="lazy">'

_rows = load_data("billeder", [])

def g_row(row):
    layout = row.get("layout", "single")
    cls = "g-row" if layout in ("", "single") else f"g-row {layout}"
    imgs = "".join(img(i.get("file", ""), i.get("alt", "")) for i in row.get("images", []))
    return f'    <div class="{cls}">{imgs}</div>'

_rows_html = "\n".join(g_row(r) for r in _rows)
pages.append(page("billeder", "Billeder – Morten Skou Andersen", f"""
  <main class="content gallery">
{_rows_html}
  </main>
"""))

# ---------------------------------------------------------------- NYHEDER
_news = load_data("nyheder", [])

def news_item(n):
    return f'      <article class="news"><h3 class="news-date">{n.get("date", "")}</h3>{n.get("html", "")}</article>'

news_html = "\n".join(news_item(n) for n in _news)
pages.append(page("nyheder", "Nyheder – Morten Skou Andersen", f"""
  <main class="content narrow">
    <h1 class="page-header">NYHEDER</h1>
{news_html}
  </main>
"""))

# ---------------------------------------------------------------- BUTIK
pages.append(page("butik", "Butik – Morten Skou Andersen", """
  <main class="content narrow">
    <h1 class="page-header">Butik</h1>
    <p>Al vores musik kan nu købes fysisk på Bandcamp:</p>
    <p><a href="https://mortenskouandersen.bandcamp.com/music">https://mortenskouandersen.bandcamp.com/music</a></p>
    <p>Digitale versioner af de tre første album ligger der også, og resten er på vej…</p>
  </main>
"""))

# ---------------------------------------------------------------- FILOLOGI
pages.append(page("filologi", "Filologi – Morten Skou Andersen", """
  <main class="content narrow">
    <h1 class="page-header">FILOLOGI</h1>
    <p>Morten Skou Andersen er klassisk filolog, cand. mag. i latin med sidefag i græsk. Han er lektor ved Aurehøj Gymnasium og tidligere ekstern lektor ved Københavns Universitet.<br>
    Han beskæftiger sig især med oversættelse af romersk litteratur, fortrinsvis romersk poesi.<br>
    Han har færdiggjort en komplet dansk oversættelse af Catuls digte, som efter planen udgives i efteråret 2024.<br>
    Han er desuden i samarbejde med Sebastian Maskell Andersen i gang med en oversættelse af Ciceros De amicitia (om venskab).<br>
    Ved siden af arbejder han ind imellem på en oversættelse af Lucans epos Pharsalia eller De bello civili (om borgerkrigen), men det er et uhyre langsigtet projekt.</p>

    <h2 class="section-header">Publikationer</h2>

    <div class="pub">
      <img src="../assets/img/filologi/statius.jpeg" alt="Statius' Silvae i udvalg – forside" loading="lazy">
      <div>
        <h3>Statius’ Silvae i udvalg (2019)</h3>
        <p>Statius’ Silvae i udvalg – oversat med udførlige introduktioner og kommentarer af Morten Skou Andersen.</p>
        <p>Udgivet af Forlaget Atalante.</p>
        <p><a href="https://atalante.dk/udgivelser1/silvae">https://atalante.dk/udgivelser1/silvae</a></p>
      </div>
    </div>

    <div class="pub">
      <img src="../assets/img/filologi/lucan.jpg" alt="Lucan-artiklen i Aigis" loading="lazy">
      <div>
        <h3>Lucan, Pharsalia VI,507-830 (2013)</h3>
        <p>„Underverdenen og borgerkrigen. Lucan, Pharsalia VI,507-830, oversat af Morten Skou Andersen.”</p>
        <p>Artikel publiceret i Aigis 13.2, 2013.</p>
        <p><a href="https://aigis.igl.ku.dk/aigis/2013,2/MSA-Lucan.pdf">https://aigis.igl.ku.dk/aigis/2013,2/MSA-Lucan.pdf</a></p>
      </div>
    </div>

    <div class="pub">
      <img src="../assets/img/filologi/satyrica.jpg" alt="Satyrica-artiklen i Aigis" loading="lazy">
      <div>
        <h3>Priapos’ rolle i Satyricon (2012)</h3>
        <p>„Encolpius og Priapos – en undersøgelse af Priapos’ rolle i Satyrica.”</p>
        <p>Artikel publiceret i Aigis 12.2, 2012.</p>
        <p><a href="https://aigis.igl.ku.dk/aigis/2012,2/MSA-Priap.pdf">https://aigis.igl.ku.dk/aigis/2012,2/MSA-Priap.pdf</a></p>
      </div>
    </div>

    <h2 class="section-header">Foredrag</h2>
    <p>„Fortryllelse og forbandelse. Hekse i romersk skønlitteratur.” Et foredrag om heksen som litterær figur i Horats’ epoder, Lukans Pharsalia og Apulejus’ Det gylde æsel; holdt den 8. marts, 2014 ved Phrontisteriums Seminar, Københavns Universitet.</p>
    <p>„Thessala vates vatem eligit. How to read Lucan – an interpretative guide to making sense of Lucan’s Pharsalia.” Foredraget blev holdt for Hic Sunt Leones den 5. December 2013, på CML, Syddansk Universitet Odense.</p>
  </main>
"""))

# ---------------------------------------------------------------- OM
pages.append(page("om", "Om – Morten Skou Andersen", """
  <main class="content narrow">
    <h1 class="page-header">MORTEN SKOU ANDERSEN<br><span class="page-header-sub">&amp; de mennesker han normalt sammenligner sig med</span></h1>

    <h2 class="section-header">Kontakt</h2>
    <p>mortenskouandersen@gmail.com<br>
    <a href="https://www.facebook.com/mortenskouandersen">https://www.facebook.com/mortenskouandersen</a></p>

    <h2 class="section-header">Bandmedlemmer</h2>
    <p>Morten Skou Andersen; guitar og sang.<br>
    Jacob Karl Viktor Lundgren Lövenlund: tangenter.<br>
    Bo Hollænder: bas.<br>
    Allan Sonne: trommer.</p>
    <p>Tidligere medlemmer:<br>
    Adam Juhl Norholt: bas (2008-2015)<br>
    Rasmus Emil Mikkelsen: percussion og trommer (2010-2021).<br>
    Jacob Svensmark: bas (2015-2020).</p>

    <h2 class="section-header">Baggrund</h2>
    <p>Paralleller til Morten Skou Andersens sange er svære at finde. Han og hans band står for en særegen sarkasme og rå, personlige fremførelser. Samfundssarkasmen i teksterne går hånd i hånd med historie, geologi, træsorter, bizar kærlighed, og hvad du mindst venter. I oktober 2023 udkom bandets femte album Forældrelandssange, som er et forsøg på at forenene fædrelandssang og samfundskritik. Endnu et nyt album er på vej og går forhåbentlig i trykken i efteråret 2024. Bandet blev nomineret til Gaffaprisens afstemningsrunde som Årets Danske Band 2019.</p>

    <h3>Solo (Jan Obs død og det at være uenig med sit jeg)</h3>
    <p>Morten har skrevet sange siden 1990; ti år var han da. Først i 2005 begyndte han at optræde jævnligt med dem. Til at begynde med påstod han, at alle sangene var skrevet af en mystisk, sky mand, der hed Jan Ob, og som boede ien bunker på Fyn. Men det gik op for Morten, at publikum troede på røverhistorierne og slet ikke forstod, at sangene i virkeligheden var hans egne. Kort før den første pladeudgivelse aflivede han Jan Ob og stod frem som ophavsmand til viserne.</p>
    <p>På det tidspunkt skrev Morten moderne protestviser. Teksterne er portrætter og skrevet i et helt ligefremt sprog, som om nogen deler sine almindelige betragtninger om en eller anden sag med lytteren. Morten gjorde meget ud af at rydde sproget for metaforer og skrive så konkret som muligt. Det var en fornyelse af den såkaldte topical songwriting, som de amerikanske protestsangere i 1960’erne dyrkede. Han optrådte med dem solo og udgav i september 2007 cd’en I fingrene med støtte fra Kunstrådet. Det blev den første af to plader produceret af Simon Gylden. Sangen Det er ikke fordi vi ikke går ind for integration blev inkluderet i sangbogen Den Nye Sangskat. Morten optræder stadig solo ind imellem.</p>
    <p>Oftest er teksten formuleret i jeg-form, men sådan, at jeget ikke er identisk med Morten selv, og stemmen kan endda ofte give udtryk for holdninger, som Morten er uenig i. På den måde opstår der en sarkasme og en tone i sangene, som helt er Mortens egen. Han holder sig for eksempel ikke tilbage for at synge fra en kvindes synspunkt, eller helt outreret fx fra en pædofils.</p>

    <h3>Med band</h3>
    <p>Men i 2008 slog Morten pjalterne sammen med Adam Juhl Norholt og Jacob Karl Viktor Lundgren Lövenlund og dannede Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med. Adam og Morten har spillet sammen i forskellige sammenhænge siden 2002, hvor de og Jonas Jensen dannede art rock-bandet Leende kvinde i vindue. Jacob og Morten spiller sammen i sideprojektet Påskemissionærerne II. I oktober 2009 udkom en kombineret dobbeltvinyl og cd med titlen Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med.</p>
    <p>Siden foråret 2010 har gruppen været en kvartet. Rasmus Emil Mikkelsen kom med på slagtøj, og musikken er ændret radikalt. I begyndelsen kunne det stadig kaldes viser, men Morten begyndte at eksperimentere voldsomt med genren, som det høres på tredobbeltalbummet Varme hænder koldt hjerte fra 2012, en temaplade om død, forfald, dekadence og onde varsler. Nogle har kaldt genren dødsviser.</p>
    <p>Næste skridt blev at skifte harmonika og percussion ud med klaver/orgel og trommer. Det blev til albummet Digressioner (2014 (cd) og 2015 (vinyl)) og forløbersinglen Brev til Anders Brevik. Temaerne på det album er geologi og menneskelig fiasko. Især nummeret Brev til Anders Breivik udforsker de mørke sider af menneskesindet, idet teksten er formuleret som et brev fra en kvinde, der har forelsket sig i en massemorder. I bund og grund er portrættet stadig i fokus, selv om det af og til gemmer sig et stykke nede i teksten. Bandet optrådte med nummeret i Mik Shacks Public Service, og Morten gav interview om kontroversiel sangskrivning i Kulturnyt på DRP1.</p>

    <h3>Elektrisk</h3>
    <p>Med albummet Boligindretning, som udkom efter lang tids produktion i 2018, skiftede Morten den spanske guitar, som ellers har været hans varemærke, ud med en elektrisk. I teksterne arbejder han med at forene de lyriske elementer med hans tidligere konkretisme. Ironien i teksterne er blevet så underspillet, at den gik hen overhovedet på flere anmeldere.</p>
    <p>I 2015 forlod Adam Juhl Norholt bandet på grund af tinnitus (et sørgmodigt vidnesbyrd om den metamorfose, musikken har gennemgået), og Jacob Svensmark kom med i stedet.</p>
    <p>Bandets livedynamik er blevet helt anderledes med introduktionen af rock og elektriske instrumenter. Sættet er utroligt afvekslende, en komplet uforudsigelig blanding af viser, pop, avantgarde og forskellige former for folk, højt tempo og særegent indigneret vrål og besyngelse af historiske pinagtigheder veksler med underspillet sarkasme og besynderlige barokke kommentarer til det, der omgiver os hver dag.</p>

    <h3>Det nye band</h3>
    <p>Jacob Svensmark forlod bandet i 2020 for at forfølge sin karriere som astrofysiker og en postdocstilling på Oxford. Rasmus Emil Mikkelsen gik ud af bandet året efter for at hellige sig lydproduktion, men han nåede at være med til at indspille albummet Forældrelandssange, som udkom i oktober 2023. Rasmus spillede også en stor rolle på albummet i forbindelse med optagelsen og redigeringen af musikken. En ny bassist, Bo Hollænder spiller på de fleste af numrene, men Jacob Svensmark biddrager hist og her. Desuden er der flere gæster.</p>
    <p>Men Bo Hollænder er altså nu kommet med på bas, og Allan Sonne på trommer. Jacob Lövenlund er stadug med, på synthesizer nu. Morten og bandet trådte ud af coronavirusepidemi-nedlukningen med en ny og mere hårdtslående attitude, og med et album, altså Forældrelandssange, hvor den attitude overhovedet ikke kommer til udtryk.</p>
    <p>Endnu et nyt album har imidlertid allerede taget form. Det blev skrevet sideløbende med indspilningen af Forældrelandssange, og det meste af det var indspillet før udgivelsen af dét. Er De forvirret? Så hold øjnene åbne og glæd dig til at høre nyt om Moderne desperation eller Det bliver blandet nede i maven alligevel, som nu, i sommeren 2024 er færdigmastereret og forhåbentlig snart kan gå i trykken…</p>
  </main>
"""))

# ---------------------------------------------------------------- ALBUMSIDER
def album_page(slug, title, cover, coveralt, body):
    return page(slug, f"{title} – Morten Skou Andersen", f"""
  <main class="content narrow album">
    <img class="album-cover" src="../assets/img/covers/{cover}" alt="{coveralt}">
{body}
  </main>
""")

pages.append(album_page("digressioner", "Digressioner", "digressioner.jpg", "Digressioner – albumcover", """
    <h1 class="album-title">Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med<br>Digressioner</h1>
    <p>21. juni 2014, cd og download; Juni 2015, vinyl (bh1).<br>Udgivet af bryggeriet Beer Here.</p>
    <h2 class="section-header">Anmeldelser</h2>
    <p>Digressioner – svinkeærinder – er væsentligt skarpere og mere to-the-point end det meste andet af tidens danske sangskrivning (<a href="http://gaffa.dk/anmeldelse/85519">Gaffa</a>).</p>
    <p>Forfriskende skæv og herligt anderledes! (<a href="http://rootszone.dk/cd-morten-skou-andersen-digressioner/">Rootszone</a>).</p>
    <h2 class="section-header">Side A</h2>
    <p>Vækst<br>Una har ikke noget ansigt<br>Scientology<br>Skybruddet<br>Brev til Anders Breivik<br>Felix Baumgartner eller Himmeporten<br>Den gamle dame</p>
    <h2 class="section-header">Side B</h2>
    <p>Landskabet<br>Fyret på Anholt<br>Hilsen den afskyelige snemand<br>Pilgrimssang</p>
    <h2 class="section-header">Billede og lyd</h2>
    <p>Al tekst og musik af Morten Skou Andersen.</p>
    <p>Art work af Anna Weber Henriksen.<br>Labyrinten er tegnet af Morten Skou Andersen.<br>Indspillet og mikset af Jesper Folke Olsen, alias Backdoor Red.<br>Mastereret af ET Mastering.</p>
    <h2 class="section-header">Gæstemusikere</h2>
    <p>Morten Krogh: mundharmonika, kor på Skybruddet.<br>Øssur Bæk: violin på Fyret på Anholt.</p>
    <h2 class="section-header">Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med</h2>
    <p>Adam Juhl Norholt: bas, kor.<br>Jacob Karl Viktor Lundgren Gantana Lövenlund: flygel, elklaver, elorgel, kor.<br>Rasmus Emil Mikkelsen: trommer, kor.<br>Morten Skou Andersen: akustisk guitar, vokal.</p>
"""))

pages.append(album_page("varme-haender-koldt-hjerte", "Varme hænder koldt hjerte", "varme-haender-koldt-hjerte.jpg", "Varme hænder koldt hjerte – albumcover", """
    <h1 class="album-title">Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med<br>Varme hænder koldt hjerte</h1>
    <p>16. juni, 2012.<br>Tredobbelt lp, dobbelt cd og download (MSA3VH).<br>Udgivet på National Masterpiece Library.</p>
    <h2 class="section-header">Anmeldelser</h2>
    <p>„Lad mig sige det straks: Fra første nummer var jeg fanget. … Sådan skal moderne samfundskritik lyde. Man ler og forstemmes. Og musikken stikker godt.” (Jens Blendstrup, <a href="http://www.undertoner.dk/2012/09/morten-skou-andersen-og-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte/">Undertoner</a>)</p>
    <p>„Morten Skou Andersen har med seneste udspil understreget sin status som en ganske ubestridt ener på den danske musikscene.” (Morten Wamsler, <a href="http://www.diskant.dk/anmeldelser/pladeanmeldelser/morten-skou-andersen-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte.htm">Diskant</a>)</p>
    <p>„En omgang modersmåls-sangskrivning med noget på hjerte og en begavelse et stykke over gennemsnittet. Hatten af herfra.” (Espen Strunk, <a href="https://gaffa.dk/anmeldelse/66946/morten-skou-andersen-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte">Gaffa</a>)</p>
    <h2 class="section-header">DEL 1</h2>
    <p>a1&nbsp;&nbsp;&nbsp;&nbsp;Den 21. maj 2011</p>
    <h2 class="section-header">DEL 2</h2>
    <p>a2&nbsp;&nbsp;&nbsp;&nbsp;Byfornyelsen<br>b1&nbsp;&nbsp;&nbsp;&nbsp;Velfærd tager sin eyeliner<br>b2&nbsp;&nbsp;&nbsp;&nbsp;Ligesindethed skriver dagbog<br>b3&nbsp;&nbsp;&nbsp;&nbsp;Branding Danmarks sandkasse<br>b4&nbsp;&nbsp;&nbsp;&nbsp;Jeg mødte Fremskridtet på en natklub<br>b5&nbsp;&nbsp;&nbsp;&nbsp;Eurovisionen</p>
    <h2 class="section-header">DEL 3</h2>
    <p>c1&nbsp;&nbsp;&nbsp;&nbsp;Danerteorien<br>c2&nbsp;&nbsp;&nbsp;&nbsp;Nornen<br>c3&nbsp;&nbsp;&nbsp;&nbsp;Rytterstatuen af Christian V på Kongens Nytorv<br>c4&nbsp;&nbsp;&nbsp;&nbsp;Forbandede slægter<br>c5&nbsp;&nbsp;&nbsp;&nbsp;Ræter<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Uden titel)</p>
    <h2 class="section-header">DEL 4</h2>
    <p>d1&nbsp;&nbsp;&nbsp;&nbsp;Militær nødvendighed<br>d2&nbsp;&nbsp;&nbsp;&nbsp;Ritualer<br>d3&nbsp;&nbsp;&nbsp;&nbsp;Den dag da Monika slog op med mit liv<br>d4&nbsp;&nbsp;&nbsp;&nbsp;Postkort fra Helsingør<br>e1&nbsp;&nbsp;&nbsp;&nbsp;Begravelse Danmark<br>e2&nbsp;&nbsp;&nbsp;&nbsp;Spåmænd (hedder Vates på de fysiske udgaver)<br>e3&nbsp;&nbsp;&nbsp;&nbsp;Hjemmeopgave<br>e4&nbsp;&nbsp;&nbsp;&nbsp;Mariehønseår</p>
    <h2 class="section-header">DEL 5</h2>
    <p>f1&nbsp;&nbsp;&nbsp;&nbsp;Ansigt</p>
    <h2 class="section-header">Medvirkende</h2>
    <p>Tekst og musik af Morten Skou Andersen.</p>
    <p>Optaget, mikset og mastereret af Rune ‘Rux’ Friborg.</p>
    <p>Art work af Anna Samsøe, Jonas Jensen, Daniella Stender og Morten Skou Andersen.</p>
"""))

pages.append(album_page("morten-skou-andersen-de-mennesker-han-normalt-sammenligner-sig-med-den-orange-plade",
                        "Morten Skou Andersen & de mennesker han normalt sammenligner sig med (den orange plade)",
                        "orange-plade.jpg", "Den orange plade – albumcover", """
    <h1 class="album-title">Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med</h1>
    <p>26. oktober 2009<br>Kombineret dobbelt vinyl og cd (MSA2&amp;D / MSA2OD)</p>
    <h2 class="section-header">Anmeldelser</h2>
    <p>“I tider hvor glitrende, men kaloriefattige shows som X-faktor, Talent 09 og Idol dominerer mediefladen i Danmark, er det overordentligt befriende med en mand som Morten Skou Andersen. … Han har det aller, allervigtigste: nerve, indignation, fortællelyst og masser af humor” (Michael Strandbech, Arbejderen).</p>
    <p>„Pladen er det mest interessante inden for meningsfulde dansksprogede tekster, jeg længe har hørt” (Mads Simon Hestbech, Undertoner).</p>
    <h2 class="section-header">Side A</h2>
    <p>1&nbsp;&nbsp;&nbsp;Normaliseringen af Hellerup<br>2&nbsp;&nbsp;&nbsp;Kærlighedsgaver<br>3&nbsp;&nbsp;&nbsp;Skatter det er en dekonstruktion<br>4&nbsp;&nbsp;&nbsp;Engang var du studerende og jeg var på kontanten<br>5&nbsp;&nbsp;&nbsp;Guds ord</p>
    <h2 class="section-header">Side B</h2>
    <p>1&nbsp;&nbsp;&nbsp;Emilie verden er gigantisk<br>2&nbsp;&nbsp;&nbsp;De grå II<br>3&nbsp;&nbsp;&nbsp;Johns portrætter</p>
    <h2 class="section-header">Side C</h2>
    <p>1&nbsp;&nbsp;&nbsp;Meningsfuld vold<br>2&nbsp;&nbsp;&nbsp;I de lande vi normalt sammenligner os med<br>3&nbsp;&nbsp;&nbsp;Påvirket<br>4&nbsp;&nbsp;&nbsp;Flemming og effektiviseringen<br>5&nbsp;&nbsp;&nbsp;Soprten rør de satmer ikke<br>6&nbsp;&nbsp;&nbsp;Om at flytte på landet</p>
    <h2 class="section-header">Side D</h2>
    <p>1&nbsp;&nbsp;&nbsp;Dræbersneglen kommer</p>
    <p>(På cd’en er Flemming og effektiviseringen udeladt pga. pladsmangel, og I de lande… og Påvirket er byttet om.)</p>
    <h2 class="section-header">Musikere og andre medvirkende</h2>
    <p>Morten Skou Andersen: akustisk guitar og sang.<br>Adam Juhl Norholt: bas.<br>Jacob Karl Viktor Lundgren Lövenlund: harmonika.</p>
    <p>Optaget, mikset og mastereret af Simon Gylden</p>
    <p>Art work af Jonas Jensen alias Kasper Knigge.</p>
"""))

pages.append(album_page("5537-2", "I fingrene", "i-fingrene.jpg", "I fingrene – albumcover", """
    <h1 class="album-title">Morten Skou Andersen<br>I fingrene</h1>
    <p>1. oktober 2007<br>Cd (MSA1IF)<br>Udgivet på National Masterpiece Library<br>Udgivet med støtte fra Kunstrådet</p>
    <p>Cd’en kan købes ved at skrive på Facebook, Discogs (til Dixen86) eller sende en mail:<br>mortenogdemennesker@gmail.com</p>
    <h2 class="section-header">Anmeldelser</h2>
    <p>“I Fingrene er leveret med mere glimt i øjet end alle tresser-forgængerne præsterede tilsammen.” (Gaffa)</p>
    <p>„Det er en jammerlig omgang hø og hakkelse.” (Jydske Vestkysten)</p>
    <h2 class="section-header">Numre</h2>
    <p>1&nbsp;&nbsp;&nbsp;&nbsp;Det er blevet alvorligt<br>2&nbsp;&nbsp;&nbsp;&nbsp;Åh Pia baby<br>3&nbsp;&nbsp;&nbsp;&nbsp;Tsunami-året<br>4&nbsp;&nbsp;&nbsp;&nbsp;Tænk hvis for eksempel koreanerne fik våben der kunne matche USA’s<br>5&nbsp;&nbsp;&nbsp;&nbsp;Det er ikke fordi vi ikke går ind for integration<br>6&nbsp;&nbsp;&nbsp;&nbsp;Når den dumme krig er færdig<br>7&nbsp;&nbsp;&nbsp;&nbsp;Deus ex machina (Rigtig i hovedet)<br>8&nbsp;&nbsp;&nbsp;&nbsp;Tidlig nat<br>9&nbsp;&nbsp;&nbsp;&nbsp;At have en mening<br>10&nbsp;&nbsp;De grå<br>11&nbsp;&nbsp;Da jeg var omkring de tyve<br>12&nbsp;&nbsp;Fremtiden<br>13&nbsp;&nbsp;Til Line</p>
    <p>Tekst og musik af Morten Skou Andersen.<br>Morten Skou Andersen: akustisk guitar og sang.<br>Optaget, mikset og mastereret af Simon Gylden.</p>
"""))

pages.append(album_page("brev-til-anders-breivik-singleversion-holmbladsgade-blues-i-h-mol-single",
                        "Brev til Anders Breivik (singleversion) / Holmbladsgade-blues i h-mol (single)",
                        "breivik-single.jpg", "Single-cover", """
    <h1 class="album-title">Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med<br>Brev til Anders Breivik (singleversion) / Holmbladsgade-blues i h-mol</h1>
    <p>7. maj 2013.<br>Download-single.<br>Udgivet på Damn Right Records.</p>
    <p>Brev til Anders Breivik findes i en anden indspilning på Digressioner, som er den bedste.</p>
    <h2 class="section-header">Numre</h2>
    <p>1&nbsp;&nbsp;Brev til Anders Breivik<br>2&nbsp;&nbsp;Holmbladsgadeblues i h-mol</p>
    <h2 class="section-header">Medvirkende</h2>
    <p>Tekst og musik af Morten Skou Andersen<br>Indspillet og mikset af Jesper Folke Olsen i Folkes Garage<br>Masteret af Jan Eliasson<br>Artwork af Anna Weber Henriksen</p>
    <p>Musikere:<br>Morten Skou Andersen: vokal og guitar<br>Jacob Karl Viktor Lundgren Gantana Lövenlund: flygel<br>Adam Juhl Norholt: bas<br>Rasmus Emil Mikkelsen: trommer</p>
    <p>Desuden på Holmbladsgadeblues i h-mol:<br>Morten Krogh: mundharmonika</p>
"""))

for path, html in pages:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("skrev", os.path.relpath(path, ROOT))
print(f"{len(pages)} sider genereret.")
