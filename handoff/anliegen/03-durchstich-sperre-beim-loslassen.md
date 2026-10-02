# Durchstich „höchstens um M ziehen“: Sperre beim Loslassen

03 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** Der empfohlene Durchstich ist technisch der richtige Start: der dünnste Schnitt
durch Fachlogik, Backend und Karte, die Fachlogik ist bei runden Bases klein, das Neuland
(Karte, Ziehen, Maßstab Zoll zu Bildschirm) liegt genau im Durchstich. Offen ist, was
„darüber gesperrt“ beim Ziehen heißt:
- (a) Das Modell bleibt schon beim Ziehen an der Grenze von M stehen.
- (b) Beim Loslassen prüft Arbiter; bei Sperre springt das Modell zurück und der Grund steht da.

**Kosten.** (a) braucht die Prüfung während des Ziehens: entweder die Geometrie ein zweites
Mal im Browser (zwei Wahrheiten, die auseinanderlaufen) oder eine Anfrage je Zeigerbewegung.
Beispiel Altbestand: `geometry.py:blocked_region_path` rechnet Sperrflächen als SVG-Pfad für
den Browser, `model_drag.js` klemmt damit; beides zusammen über 140.000 Zeichen.
(b) braucht eine Anfrage je Zug; die Fachlogik bleibt die einzige Prüfinstanz, und das Muster
für das Übergehen (Sperre mit Grund, Spieler bestätigen, Protokoll) entsteht gleich mit.

**Gegenvorschlag.**
- Durchstich mit (b). Während des Ziehens zeigt die Karte den Kreis der verbleibenden
  Bewegung als reine Anzeige; er entscheidet nichts.
- Maus und Touch über dieselben Zeigerereignisse (Pointer Events): Touch kostet im Code kaum
  mehr; nur der Bildschirmtest mit Touch darf später kommen.
- (a) als späteres Komfort-Item, wenn der Stakeholder es nach dem Durchstich will.

**Stellungnahme.**
