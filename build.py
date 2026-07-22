#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for mortenskouandersen.dk — statisk site uden WordPress.
Kør: python3 build.py  (skriver HTML-filer i samme mappe)"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

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
releases = [
    ("Forældrelandssange", "Album, 2023", "foraeldrelandssange.jpg", None),
    ("Boligindretning", "Album, 2018", "boligindretning.jpg", None),
    ("Digressioner", "Album, 2015", "digressioner.jpg", "../digressioner/"),
    ("Varme hænder koldt hjerte", "Album, 2012", "varme-haender-koldt-hjerte.jpg", "../varme-haender-koldt-hjerte/"),
    ("Morten Skou Andersen &amp; de mennesker han normalt sammenligner sig med", "Album, 2009", "orange-plade.jpg", "../morten-skou-andersen-de-mennesker-han-normalt-sammenligner-sig-med-den-orange-plade/"),
    ("I fingrene", "Album, 2007", "i-fingrene.jpg", "../5537-2/"),
]
single = ("Brev til Anders Breivik (singleversion) / Holmbladsgade-blues i h-mol", "Single, 2013", "breivik-single.jpg", "../brev-til-anders-breivik-singleversion-holmbladsgade-blues-i-h-mol-single/")

def release_item(title, sub, img, href):
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

rel_html = "\n".join(release_item(*r) for r in releases)
pages.append(page("udgivelser", "Udgivelser – Morten Skou Andersen", f"""
  <main class="content">
    <h1 class="page-header">ALBUM</h1>
    <div class="releases">
{rel_html}
    </div>
    <h1 class="page-header">SINGLE</h1>
    <div class="releases">
{release_item(*single)}
    </div>
  </main>
"""))

# ---------------------------------------------------------------- KONCERTER
def K(date, venue, extra=None):
    out = f'      <p class="gig"><span class="gig-date">{date}</span><br>{venue}'
    if extra:
        out += "<br>" + extra
    return out + "</p>"

gigs_html = "\n".join([
    K("14. november 2025 (lørdag) 20:00", "MUSIKHUZET (Rønne)."),
    K("2. august 2025 (lørdag)", "(Annonceres senere.)"),
    K("14. juni 2025 (lørdag) 17:00", "VÆSKEBALANCEN (København)."),
    K("26. april 2025 (lørdag) 19:00 Release-koncert",
      'AMAGER RECORDS (København). <a href="https://www.facebook.com/events/594086966808934">Link</a>.',
      'Opvarming: Morgan Helltown &amp; The Lost Cause.<br>Entré: standard 75 kr. / studerende 50 kr. <a href="https://www.place2book.com/da/sw2/sales/a9bbzb395e">Billet</a>.'),
    K("9. april 2025 (onsdag) 20:00", "BLÅGÅRDS APOTEK (København)."),
    K("11. september 2024 (onsdag) 20:30", "BLÅGÅRDS APOTEK", "Hovednavn til Songwriters’ Playground."),
    K("13. juli 2024 (lørdag) 15:00", "PENYLLAN BREWERY (Tejn, Bornholm)."),
    K("12. juli 2024 (fredag) 20:00", "DEN MARINEDE SILD (Rønne)."),
    K("8. juni 2024 (lørdag) 21:45",
      'DROP INN, København. <a href="https://www.facebook.com/events/401818526138355/">Link</a>.',
      "International Pop Overthrow Festival nr. 25."),
    K("20. april 2024 (lørdag) 20:00", 'DISPENSARY, København. <a href="https://www.facebook.com/events/334947452886070">Link</a>.'),
    K("10. april 2024 (onsdag) 21:30 (dørene åbner 20:00)", "TJILIPOP, København."),
    K("3. februar 2024 (lørdag) 19:30 (dørene åbner 18:30)", 'AMAGER RECORDS, København. <a href="https://www.facebook.com/events/871533354296428">Link</a>.'),
    K("6. december 2023 (onsdag) 20:30",
      'BLÅGÅRDS APOTEK, København. <a href="https://www.facebook.com/events/270500582503382/270500635836710/">Link</a>.',
      "Hovednavn til Songwriters’ Playground."),
    K("11. november 2023 (lørdag) 20:00",
      'HUSET PÅ NÆSSET, Tuse Næs, Holbæk. <a href="https://www.facebook.com/events/820741866193503">Link</a>.',
      "Dobbeltkoncert med Morgan Helltown &amp; The Lost Cause."),
    K("28. oktober 2023 (lørdag) 16:00",
      'FLERE FUGLE, København. <a href="https://www.facebook.com/events/2046716045685171">Link</a>.',
      "Releasefest, koncert og dj’s."),
    K("12. august 2023 (lørdag) 16:00", 'MUSICON MIKROBRYGGERI, Roskilde. <a href="https://www.facebook.com/events/932197757908577">Link</a>.'),
    K("5. august 2023 (lørdag) 17:00",
      'FLERE FUGLE, København. <a href="https://www.facebook.com/events/1268818000420705">Link</a>.',
      "Morten Skou Andersen solo-koncert + dj-sæt."),
    K("24. maj 2023 (onsdag), dørene åbner 20:30", "BLÅGÅRDS APOTEK, København.", "Hovednavn til Songwriters’ Playground."),
    K("25. november 2022 (fredag) 19:00", 'HOPPE BEER, Solrød. <a href="https://www.facebook.com/events/5598349876874860">Link</a>.'),
    K("5. november 2022 (lørdag) 21:00",
      'GIMLE, Roskilde. <a href="https://www.facebook.com/events/487998619964740">Link</a>.',
      "Til releasefest for Morgan Helltown &amp; the Lost Cause."),
    K("16. september 2022 (fredag) 17:00", 'TOFTEGÅRDS PLADS, Valby. <a href="https://www.facebook.com/events/647789813424371">Link</a>.'),
    K("10. september 2022 (lørdag) ca. 19:00", 'DET LILLE BRYGGERI, Bringstrup, Ringsted. <a href="https://www.facebook.com/events/597076295166336">Link</a>.'),
    K("27. august 2022 (lørdag) 15:00", "SPYBREW, Hvidovre."),
    K("5. august 2022 (fredag) 14:00", 'PENYLLAN BREWERY, Tejn, Bornholm. <a href="https://penyllan.com/events/">Link</a>.'),
    K("29. juli 2022 (fredag) 14:30", 'NAKKEFESTIVAL, Rørvig. <a href="https://www.facebook.com/OfficielNakkefestival">Link</a>.'),
    K("16. april 2022 (lørdag) 20:00", "SORTE RENÉ, København."),
    K("30. oktober 2021 (lørdag) 20:00", 'MUSICON MIKROBRYGGERI, Roskilde. <a href="https://www.facebook.com/events/905922953686900">Link</a>.'),
    K("20. august 2021 (fredag) 17:00", 'VORES BRØD, Valby, København. <a href="https://www.facebook.com/events/548421019634392">Link</a>.'),
    K("22. juli 2021 (torsdag) 20:00", 'FÆLLESTIVAL, Stenstrup, Fyn. <a href="https://faellestival.dk/wp/program-2021/">Link</a>.'),
    K("21. november 2020 (lørdag) 19:00", 'HUSET PÅ NÆSSET, Udby, Holbæk. <a href="https://www.facebook.com/events/386510179416042/">Link</a>.'),
    K("14. november 2020 (lørdag) 20:00", 'STUDENTERHUS ODENSE. <a href="https://www.facebook.com/events/2976426032452138/">Link</a>.'),
    K("31. august 2019 (lørdag)", "RAVEN FEST, Pinovar Raven, Pilsen, Czekkiet."),
    K("3. august 2019 (lørdag)", "ØLLUMINATI, Viborg."),
    K("1. august 2019 (torsdag)", "SPIREFESTIVAL, Udby, Holbæk."),
    K("5. juli 2019 (fredag) 20:00", "KØBENHAVNERIET, Rørvig, Odsherred."),
    K("29. juni 2019 (lørdag) eftermiddag.", "MAGISK MIDSOMMER, Allingåbro, Djursland."),
    K("1. juni 2019 (lørdag) eftermiddag/aften", "PENNYLAN, Tejn, Bornholm."),
    K("17. april 2019 (onsdag).", "BLÅGÅRDS APOTEK, København. Hovednavn til Songwriters’ Playground."),
    K("26. januar 2019 (lørdag) 20:00", "MUSICON MIKROBRYGGERI, Roskilde."),
    K("11. oktober 2018 (torsdag), 21:00", "STUDENTERHUSET, København."),
    K("28. juli 2018 (lørdag), 13:15", "NAKKEFESTIVAL, Rørvig."),
    K("20. juli 2018 (fredag), 14:00", "LOPPEN FESTIVAL, Christiania, København."),
    K("2. juni 2018 (lørdag), 12:00", "HORNSROCK, Skibby, Hornsherred."),
    K("18. maj 2018 (fredag)", "BRAW, Nørrebro Bryghus, København."),
    K("2. maj 2018 (onsdag), 20:00", "BLÅGÅRDS APOTEK, København. Hovednavn til Songwriters’ Playground."),
    K("28. april 2018 (lørdag), 19:30", "ØLLUMINATI, Viborg."),
    K("14. april 2018 (lørdag), 21:00", "BOLDTS BAR, Haderslev."),
    K("7. april 2018 (lørdag), 20:00", "RELEASEFEST på DISPENSARY, København."),
    K("18. november 2017, 20:00", "BØRNETEATERET, Christiania."),
    K("8. september 2017, 19:00", "VESTEGNENS KULTURUGE, KULTURNATTEN, Rødovre."),
    K("26.-27. august 2017", "BREWSKIVAL, Helsingborg, Sverige."),
    K("5. august 2017 (lørdag), 14:00 OG 15:15", "SPIREFESTIVAL, Udby, Tuse Næs."),
    K("4. august 2017, 14:00", "FREDERIKSSUNDFESTIVAL, Frederikssund."),
    K("17. juni 2017 (lørdag), 11:00-22:00", "BLUE BEETLE ROCK FOR CHARITY – Til fordel for Hjernebarnet", "Flying Couch Bryggeri, København."),
    K("5. maj 2017 (fredag), 20:00", "CAFÉ HABIBI, Jyderup, Vestsjælland."),
    K("15. februar 2017 (onsdag), 20:00", "BLÅGÅRDS APOTEK, København, Nørrebro. Songwriters’ playground."),
    K("19. november 2016 (lørdag), 20:00", "BØRNETEATERET, Christiania. Dobbeltkoncert med Rune Rux. Entré 50 kr."),
    K("17. september 2016 (lørdag), 17:00", "GOLDEN DAYS, Kuben, Frederiksberg, Hovedstaden. Entré 90 kr."),
    K("26. august 2016 (fredag)", "BREWSKIVAL, Cindersgatan 8, Helsingborg."),
    K("20. august 2016 (lørdag), 16:30.", "BRYG &amp; TRÅD, Ølsted."),
    K("20. august 2016 (lørdag), 14:15.", "DANMARK DEJLIGST, Udby, Tuse Næs."),
    K("25. juni 2016 (lørdag)", "RÅHUSET, København. Støttefest for Spirefestival."),
    K("4. maj 2016 (onsdag), dørene åbner 20:00", "BLÅGÅRDS APOTEK."),
    K("9. januar 2016 (lørdag), 20:00", "PH-Caféen, København. Dobbeltkoncert med Elevatorfører. Entré 75 kr."),
    K("11. december 2015 (fredag), 19:00", "HEADQUARTERS, Aarhus. Dobbeltkoncert med Elevatorfører. Entré 75 kr."),
    K("6. oktober 2015 (fredag, kulturnat), 18:00", "PVC, København; ikke koncert, men forpræmiere på musikvideoen til Hilsen den afskyelige snemand"),
    K("23. august 2015 (onsdag), 20:30", "BLÅGÅRDS APOTEK, København"),
    K("9. april 2015 (torsdag)", "STUDENTERHUSET, København"),
    K("6. marts 2015 (fredag) 20:00 – Morten Skou Andersen solo", "RÅHUSET, København, releasefest for Merigold"),
    K("5. marts 2015 (torsdag) – Morten Skou Andersen solo", "HUSET I HASSERISGADE, The Quite Quiet Club, Ålborg"),
    K("14. februar 2015 (lørdag)", "BØRNETEATERET, Christiania"),
    K("29. november 2014 (lørdag), 19:00 (som trio)", "PROJEKTRUM VERA, Åboulevarden 9c, København"),
    K("19. november 2014, 20:30", "BLÅGÅRDS APOTEK, Blågårds Plads, København"),
    K("22. august 2014", "BRYG &amp; TRÅD #3, Herslev"),
    K("26. juli 2014", "NAKKEFESTIVAL, Rørvig, Odsherred"),
    K("9.-12. juli 2014", "LOVE IN, Festivalen på Skarø"),
    K("5. juli (lørdag) 2014", "ULDUM GADEMUSIKFESTIVAL, Uldum."),
    K("21. juni (lørdag) 2014, 20:30", "RELEASEFEST I KB18, København"),
    K("29. maj 2014 (torsdag, Kristi himmelfart)", "LOPPEN, Christiania, Dobbeltkoncert sammen med Frodegruppen 40"),
    K("17. april 2014 (torsdag), kl. 18:00", "MOJO, København, Støttefest for Spirefestival"),
    K("2. april 2014 (onsdag), kl. 19:00", "POLITIKENS HUS, Rådhuspladsen, Kbh"),
    K("12. marts 2014 (onsdag), kl. 19:00", "POLITIKENS HUS, Rådhuspladsen, Kbh, Dommedag i Boghallen"),
    K("27. november 2013 (onsdag), dørene åbner 20:30", "BLÅGÅRDS APOTEK, Blågårds Plads, København"),
    K("19. november 2013 (tirsdag), dørene åbner klokken 20:00", "DOVNE ROBERTS VALGAFTENSFEST", "Vela Gay Club, Klub Nysgerrig, Viktoriagade, København"),
    K("9. november 2013 (lørdag) Kierkegaard i Rundetaarn", "RUNDETÅRN, København",
      "Morten Skou Andersen (solo) spiller Deus ex machina til et foredrag om selvet hos Kierkegaard.<br>Foredragene kan streames live."),
    K("11. oktober 2013 (fredag): Kulturnatten", "LANDSFORENINGEN LIV &amp; DØD, Nikolaj Plads 27 i København"),
    K("25. september 2013 (onsdag)", "BLÅGÅRDS APOTEK, Blågårds Plads, København"),
    K("23.-25. august 2013 (fredag til søndag)", "BRYG OG TRÅD #2, Herslev"),
    K("2. august 2013 (fredag)", "SPIREFESTIVAL, Udby Sj."),
    K("27. juli 2013 (lørdag)", "BØRNETEATERET, Christiania"),
    K("8. juni 2013 (lørdag), 16:00: Sammensurium", "ILLUTRON, København – Entré 70 kr."),
    K("17. maj 2013 (fredag), dørene åbner klokken 17:00.", "ET ATELIER PÅ CARLSBERG, Malttorvet 2, København"),
    K("1. maj 2013 (onsdag), klokken 17:30: Jubilæumsfest for DiGiDi", "HUSET I MAGSTRÆDE, København – Entré."),
    K("5. april 2013 (fredag), klokken 21:00: Vi spiller til Workers In Songs’ releasefest", "LOPPEN, Christiania – Entré 40 kr."),
    K("21. februar 2013 (torsdag), klokken 19:30. Jonathan varmer op for os.", "BØRNETEATRET, Christiania – Entré 40 kr."),
    K("14. februar 2013 (torsdag), dørene åber klokken 20:00 (et sæt på en halv time)", "CAFE RETRO, København"),
    K("13. februar 2013 (onsdag)", "CAFE MONSTER TIMES, København SV."),
    K("30. januar 2013 (onsdag), dørene åbner klokken 20:30 (et sæt på en god halv time)", "BLÅGÅRDS APOTEK, Blågårds plads, København."),
    K("31. oktober 2012 (onsdag), 20:00", "BLÅGÅRDS APOTEK, Blågårds plads, København."),
    K("27. oktober 2012 (lørdag), opvarmning for Zero Absolu, klokken 21:00", "UNDERWERKET (KraftWerkets musikscene), Valby."),
    K("25. oktober 2012 (torsdag), Spil dansk-dag klokken 22:00", "NUTID, Skt. Pederstræde 1, København."),
    K("3. oktober 2012 (onsdag), 20:00", "GIMLE, Roskilde."),
    K("14. september 2012 (fredag), 14:40: Morten Skou Andersen solo", "TRE FESTDAGE FOR MALERIET i Huset I Magstræde, Købehavn."),
    K("28. august 2012 (tirsdag), 18:00", "ISLANDS BRYGGE KULTURHUS, København"),
    K("25. august 2012 (lørdag)", "DET BLIVER TIL NOGET-FESTIVAL på Studentergården i København."),
    K("18. august 2012 (lørdag)", "BRYG OG TRÅD – Brew down ved Herslev Bryghus."),
    K("2. august 2012 (torsdag)", "SPIREFESTIVAL i Udby, Tuse Næs – Vi åbner årets festival."),
    K("16. juli 2012 (mandag), 15:00", "RICCOS KAFFEBAR, Anholt."),
    K("15. juli 2012 (søndag) klokken 18:00", "MOLEVITTEN, Anholt."),
    K("14. juli 2012 (lørdag) klokken 18:00", "MOLEVITTEN, Anholt."),
    K("4. juli 2012 (onsdag) klokken 17:00-17:30", "MOZARTS PLADS, København – Til indvielsen af en gynge-lydinstallation."),
    K("16. juni 2012 (lørdag), 19:00.", "RELEASEFEST i HUSET I MAGSTRÆDE, 1. SAL",
      "– Vi spiller to sæt. Bl. andet med kor for første gang live!<br>– Workers In Songs spiller svedig støvet countryfolk (www.workersinsongs.com).<br>– Hvalen Para Human synger sit hjerte ud til undersøisk rythm and blues.<br>– Dj Don Stener svinger grammofonerne."),
    K("31. maj 2012 (torsdag). Dørene åbner klokken 20.00. Vi spiller et sæt senere.", "CAFÉ RETRO, Knabrostræde, København."),
    K("23. maj 2012 (onsdag). Dørene åbner klokken 20.00", "BLÅGÅRDS APOTEK, København."),
    K("16. maj 2012, 18:00", "MOJO BLUES BAR, København – Støttefest for Spirefestival."),
])
pages.append(page("koncerter", "Koncerter – Morten Skou Andersen", f"""
  <main class="content narrow">
    <h1 class="page-header">KONCERTER</h1>
{gigs_html}
    <p class="gig-end"><em>Længere tilbage går historikken ikke.</em></p>
  </main>
"""))

# ---------------------------------------------------------------- VIDEOER
videos = [
    ("Her bor vi (Boligindretning)", "ipQjHeoNJ5E"),
    ("En ny regering (Boligindretning)", "VfzLLWG5Pfc"),
    ("Hilsen den afskyelige snemand (Digressioner)", "QodU8g6do8U"),
    ("Brev til Anders Breivik (Digressioner), live akustisk", "DuomDDz9QXw"),
    ("Kærlighedsgaver (&amp; de mennesker…), live", "Qys5J72P0g8"),
]
vid_html = "\n".join(
    f"""      <div class="video-cell">
        <p class="video-title">{t}</p>
        <div class="video-frame"><iframe src="https://www.youtube.com/embed/{vid}" title="{t}" loading="lazy" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>
      </div>""" for t, vid in videos)
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
pages.append(page("billeder", "Billeder – Morten Skou Andersen", f"""
  <main class="content gallery">
    <div class="g-row wide">{img('dsc-1310.jpg','Morten Skou Andersen og bandet')}</div>
    <div class="g-row wide">{img('bandfoto-2021.jpeg','Bandfoto, juni 2021')}</div>
    <div class="g-row">{img('birkeroed.jpg','Koncert i Birkerød')}</div>
    <div class="g-row wide">{img('pressefoto-boligindretning.jpg','Pressefoto, Boligindretning')}</div>
    <div class="g-row cols-2">{img('uden-pjat.jpg')}{img('deprifarver-klat.jpg')}</div>
    <div class="g-row wide">{img('forfra.jpg')}</div>
    <div class="g-row cols-3">{img('paa-raekke-adam.jpg')}{img('papir-01.jpg')}{img('papir-02.jpg')}</div>
    <div class="g-row cols-2">{img('snor-01.jpg')}{img('snor-02.jpg')}</div>
    <div class="g-row cols-4">{img('portraet-adam.jpg','Adam')}{img('portraet-jacob.jpg','Jacob')}{img('portraet-rasmus.jpg','Rasmus')}{img('portraet-morten.jpg','Morten')}</div>
    <div class="g-row">{img('paa-raekke.jpg')}</div>
    <div class="g-row cols-2">{img('haengning-morten-hiver.jpg')}{img('haengning.jpg')}</div>
    <div class="g-row wide">{img('cement.jpg')}</div>
    <div class="g-row">{img('hammer.jpg')}</div>
    <div class="g-row">{img('antenne.jpg')}</div>
    <div class="g-row">{img('portraet-i-fingrene.jpg')}</div>
  </main>
"""))

# ---------------------------------------------------------------- NYHEDER
def N(date, *paras):
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f'      <article class="news"><h3 class="news-date">{date}</h3>{body}</article>'

news_html = "\n".join([
    N("29. december, 2024", "Det nye album er færditryk og står pakket på Nordsø Records. Vi er i fuld gang med at finde et sted at holde releasekoncert, og der også sat gang i et musikvideoprojekt…"),
    N("18. august, 2024", "Det kommende album er nu så godt som færdigmastereret. Billederne til omslaget er taget. Næste skridt er at få omslaget klart til tryk."),
    N("7. februar, 2024", "Arbejdet med det kommende album skrider stødt frem. Vi har foretaget et par enkelte sidste rettelser af bas og vokal, ellers bliver det et mere råt album end de foregående. Miksningen kommer forhåbentlig på plads inden længe. Møde om artwork på fredag."),
    N("22. oktober, 2023", "Endelig er der en opdateret webshop igen. Alle album ligger nu til salg i fysiske eksemplarer på Bandcamp. De tre seneste kan også streames og købes digitalt. Vi ses til release-fest den 28. oktober."),
    N("14. oktober, 2023", "I denne uge er vi i studiet igen og gået i gang med at indspille et nyt album. Det tog så lang tid at indspille “Forældrelandssange” (som stadig udkommer i slutningen af måneden), at jeg nåede at skrive alle numre til endnu et album i mellemtiden. Sådan kan det gå; de mest dedikerede lyttere vil vide, at vi allerede har spillet nogle enkelte af numrene live."),
    N("25. juli, 2023", "Nyt album, Forældrelandssange, udgives til efteråret. Der er releasefest den 28. oktober på Flere Fugle i København (se koncertkalenderen)."),
    N("21. maj, 2023", "Det nye album er færdigtrykt, og vi håber snart at kunne offenliggøre en udgivelsesdato. Hold også øje med koncertkalenderen!"),
    N("8. marts, 2022", "Det kommende album er færdigindspillet og er langt om længe ved at blive mikset. Vi håber på udgivelse senere i år."),
    N("21. oktober, 2021", "Indspilningen af det kommende album er stadig i gang, men vi kan se enden på det."),
    N("15. august, 2021", "Så har vi endelig fået hul på at spille koncerter igen. På fredag spiller vi i Valby, og andre ting er også i støbeskeen. På den måde byder vi velkommen til vores nye mand bag trommerne, Allan Sonne."),
    N("24. januar, 2021", "Velkommen til den nye hjemmeside, som er ved at vokse frem. Vi er i det hele taget ikke lukket ned under nedlukningerne. Vi er i fuld gang med et nyt album, og vi er nået langt. Forhåbentlig venter også tider forude, hvor vi kan komme ud og spille koncert igen."),
    N("09.01.19", 'Vi er nomineret til Gaffaprisen 2019 i kategorien Årets danske navn.<br>Giv os en stemme. Der kan stemmes indtil 31. januar. <a href="https://gaffa.dk/prisen">Link</a>.'),
    N("21.12.18", 'Siden har været nede, men er nu tilbage igen. Forude venter en koncert på Musiconbryggeriet i januar.<br>Af højdepunkter siden sidst: Gode anmeldelser af den nye plade – se for eksempel disse to:<br>Espen Strunk i Gaffa – <a href="https://gaffa.dk/anmeldelse/130221/flere-intelligente-tekster-i-faengende-servering">link</a>.<br>Capac anbefaler – <a href="http://www.capac.dk/wordpress/">link</a>.'),
    N("30.04.18", "Det nye album er ude. Følg med i koncertekalenderen, der er blevet længere.<br>Pladen kan købes i snart sagt alle vinylbutikker i Kbh samt i Route 66 i Århus, på cd i Sound i Kbh.<br>Albummet kan naturligvis også bestilles gennem vores webshop og downloades/streames på alle tjenester."),
    N("25.02.18", 'Nyt album, “Boligindretning,” er på gaden 7. april.<br>Samme dag er der releasefest og koncert på Dispensary, Nørrebro, København. <a href="https://www.facebook.com/events/410207956097044/">Link</a>.'),
    N("28.01.18", "Vinylen er trykt og hentet hos de gæve folk på Nordsø records.<br>Så hold øje. Udgivelsesdato er på vej."),
    N("11.01.18", "Så er de nye vinyler ved at blive trykt. Nu nærmer vi os det tidspunkt, hvor vi kan sætte en udgivelsesdato."),
    N("10.12.17", "Den nye plade er langt omlænge på vej i trykken."),
    N("10.04.17 Masterering", "Mastereringen er i gang. Det driller noget, men vi er da kommet et skridt videre."),
    N("12.01.17 Den kommende plade", "Den nye plade er nu ved at blive mikset."),
    N("19.08.16 Indspilninger og nye koncerter", "Hæftig sensommer. Vi er i fuld gang med indspilningen af det nye album.<br>Og se vores koncertkalender! Nye gigs i de kommende to weekender.<br>Den 26. bliver vi internationale i Helsingborg. Og Morten synger på svensk"),
    N("22.04.16 Nye indspilninger", "Til pinse begynder indspilningen af et nyt album."),
    N("08.12.15", "Musikvideoen til Hilsen den afskyelige snemand ude på Youtube.<br>Klik på videofanen og se den!"),
    N("06.10.15 Musikvideo til Hilsen den afskyelige snemand", 'Vores første musikvideo er en realitet, skabt af Anna Weber Henriksen.<br>Se en forpræmiere på den på kulturnatten på fredag i PVC.<br>Den er en del af udstillingen Her &amp; nu – <a href="http://veraskole.dk/projektrum-udstilling/pvc-viser-nu-her-kulturnat-910-kl18-22">Link her</a>.'),
    N("16.09.15 Velkommen igen", "Hjemmsiden har været nede i en periode, men nu er vi på igen.<br>Digressioner er udkommet på vinyl.<br>Og vi har haft to udskiftninger i bandet siden sidst. Vi arbejder på at få nogle koncerter op og stå med vores nye bassist, Jacob Svensmark"),
    N("12.07.14 Nyt album bliver godt modtaget", 'Digressioner har fået de først meget fine anmeldelser.<br>På Rootszone, <a href="http://rootszone.dk/cd-morten-skou-andersen-digressioner/">læs her</a>.<br>Og fire stjerner i Gaffa, <a href="http://gaffa.dk/anmeldelse/85519">læs her</a>.'),
    N("05.06.14 Nyt album, Digressioner, udkommer 21. juni", "Det er langt om længe blevet sandhed. 11 numre, heriblandt 3 helt nye og 8 fra de sidste to års repertoire bliver udgivet på bryggeriet Beer Here. Vi glæder os meget til at præsentere det for jer. Releasefest på KB18 den 21. juni."),
    N("19.03.14", "Den nye plade ved at blive mastereret.<br>Koncertsæsonen er så småt ved at komme i gang igen. Vi glæder os bl.a. til dobbeltkoncerten med Frodegruppen 40 på Loppen."),
    N("21.11.13", 'Så er der musik og pølsefars på dk4 i Mik Shacks Public Service.<br>Intet ny om den nye plade. Det går fremad.'),
    N("24.10.13", 'Vi arbejder stadig på den nye plade. Vi er ved at nå frem til et endeligt miks.<br>I dag har vi besøgt Mik Shack i hans køkken. Hold øje med <a href="http://www.dk4.dk/index.php/item/132-mik-schacks-public-service">dk4</a>, så er der musik og pølser!'),
    N("30.06.13 Vellykket pladeindspilning", "Vi har været i studiet igen i den forgangne uge. Det er gået over al forventning og forhåbning.<br>Du kan ligeså godt allerede nu begynde at glæde dig til den kommende lp!"),
    N("14.05.13 Køb vores nye single her:", '<a href="https://itunes.apple.com/dk/artist/morten-skou-andersen-mennesker/id628429725">iTunes</a> – <a href="http://www.shop2download.com/c/Morten-Skou-Andersen-de-mennesker-han-normalt-sammenligner-sig-med/">Basepoint</a> – <a href="http://play.tdc.dk/#!/play/artist/22918191">TDC Play</a>'),
    N("07.05.13 Ny single og interview i Kulturnyt på P1", 'I dag udkommer vores nye single Brev til Anders Breivik.<br>Morten har givet interview om sangen til Kulturnyt på P1.<br>Interviewet kan høres på <a href="http://www.dr.dk/radio">dr.dk/radio</a>. 7. maj kl 12:46.'),
    N("16.04.13 Ny single bliver mikset", "I Østbirk ved Horsens sidder en mand rører ved nogle knapper.<br>Det er vores nye single Brev til Anders Breivik, som er ved at blive mikset i Folkes Garage."),
    N("31.01.13 Ny indspilning", "Vi har ikke tænkt os at hvile på laurbærrene fra Varme hænder koldt hjerte.<br>I slutningen af februar går vi i studiet og indspiller Brev til Anders Breivik og udgiver en single."),
    N("26.12.12 Fine anmeldelser af “Varme hænder koldt hjerte”", '5 ud af 6 i Undertoner. <a href="http://www.undertoner.dk/2012/09/morten-skou-andersen-og-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte/">Læs her</a>.<br>7 ud af 10 i Diskant. <a href="http://www.diskant.dk/anmeldelser/pladeanmeldelser/morten-skou-andersen-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte.htm">Læs her</a>.<br>4 ud af 6 i Gaffa. <a href="http://gaffa.dk/anmeldelse/66946">Læs her</a>.'),
    N("11.10.12 Downloadsalg", 'Det burde ikke vare længe, før vi har den nye plade til salg som download.<br>Vi arbejder på at få den op hos Digidi, og de andre to plader skulle gerne følge efter.<br>Indtil videre kan den fås på vinyl og cd i de fleste vinylforretninger i Kbh,<br>eller ved at kontakt os per mail: mortenogdemennesker@gmail.com eller på <a href="http://www.facebook.com/pages/Morten-Skou-Andersen-de-mennesker-han-normalt-sammenligner-sig-med/201319543211966">Facebook</a>.'),
    N("11.10.12 Strålende anmeldelse af den nye plade", 'Jens Blendstrup giver den 5 ud af 6 U’er i Undertoner. <a href="http://www.undertoner.dk/2012/09/morten-skou-andersen-og-de-mennesker-han-normalt-sammenligner-sig-med-varme-haender-koldt-hjerte/">Læs artiklen her</a>.'),
    N("20.06.12 Varme hænder koldt hjerte", "Den nye plade er på gaden på vinyl og cd.<br>Den kan købes i de allerfleste vinylforretninger i København."),
    N("Releasefest!", "16. juni udkommer langt om længe den nye plade: “Varme hænder koldt hjerte.” Samme dag holder vi kæmpe releasefest i Huset I Magstræde. Tre bands og en dj er bare, hvad vi har at byde på indtil videre.<br>Kom og hold fest med os! Dørene åbner klokken 19. Musikken begynder klokken 20."),
])
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
