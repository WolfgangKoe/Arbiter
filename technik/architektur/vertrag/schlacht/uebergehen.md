# Vertrag: Schlacht · Gemeinsam übergehen

Abschnitt der *Schlacht*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

- **V18** Bietet die Domäne die *Sperre* zum Übergehen an (`Sperre(*gründe,
  übergehbar=True)`, nur `modellLoslassen` der *Bewegungsphase*, BEW-8.1), trägt die 409
  (V6) `"übergehbar": true`, sonst fehlt er; mit ‚keine Kohärenz‘ ist `Sperre.übergehbar`
  nie wahr (QUE-5.5). Danach bietet die Seite „gemeinsam übergehen“ an, bis zur nächsten
  Antwort auf eine Handlung oder ein Auswählen (V2, V14); die `sperrmeldung` bleibt nach V7.
  Warum: Das Einvernehmen gilt der *Sperre*, die beide gesehen haben. Auf Klick schickt sie
  dieselbe Anfrage, im Körper dazu `"übergehen": [<gründe der 409>]`; keine Liste von
  Texten eines `Grund`: 400.
  `modellLoslassen(modell, stelle, übergehen=frozenset())` prüft wie immer (D2); sind die
  *Gründe* übergehbar und alle in `übergehen`, *setzt* es wie ohne *Sperre*, auch nach
  Anhalten (BEW-8.2, 2.8), und trägt ins *Protokoll* die *Gründe* der *Sperre* ein, sonst
  `Sperre` (zweite Seite, QUE-3.2); ohne *Sperre* wie ohne `übergehen`, ohne Eintrag
  (QUE-5.1: „bei einer *Sperre*“). `Protokoll`, `Eintrag(einheit, spieler, gründe)`: `querschnitt/uebergehen.py`;
  `Schlacht.protokoll`, der älteste Eintrag zuerst. Beispiel (V6)
  [uebergehbar.json](../uebergehbar.json), nur `gründe`, `übergehbar` und
  `spielstand.schlacht`: Stand von [schlacht.json](../schlacht.json), dann die Boyz
  (`/api/spieler/1/einheiten/1/…`) über die *Base* des Warboss loslassen.
- Spielstand: `schlacht.protokoll`, der neueste Eintrag zuerst (QUE-5.4), je Eintrag
  `spieler`, `einheit` (Kennungen nach V1), `name` wie in der *Armeeliste*, `gründe` in der
  Reihenfolge von `Grund`. Beim Start leer (QUE-5.3). Beispiel
  [protokoll.json](../protokoll.json), nur `schlacht`: Stand von `uebergehbar.json`, dann
  dieselbe Anfrage mit `übergehen`, danach ebenso den Warboss über eine *Base* der Boyz.
- Seite: die *Leisten* nach [O4](../../frontend.md), unten je Eintrag ein `protokollEintrag
  spieler<n>` mit `protokollEinheit`, `protokollSpieler` („Spieler <n>“) und je *Grund*
  `protokollGrund`; in der *Aufstellung* leer. Der Knopf „gemeinsam übergehen“ nach V7.

Prüft wie im Querschnitt: Loslassen über eine *Base*, 409 mit `übergehbar`, dieselbe Anfrage
mit `übergehen`: 200, *Stellen* wie V10 ohne *Sperre*, ein Eintrag mehr; mit einem *Grund*
außerhalb von `übergehen` 409 und Stand unverändert; V17 ohne `übergehbar`. Die Schlüssel
der Beispiele nach deren Anfragen gleich `uebergehbar.json` und `protokoll.json`. Das Ende
des Angebots nach einem Auswählen: nur Text.
