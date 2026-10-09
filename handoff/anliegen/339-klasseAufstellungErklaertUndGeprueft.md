# Die Klasse Aufstellung: Gedanke, Prüfung, Umbau

339 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · rückfrage

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** *Gedanke.* `Aufstellung` ([aufstellen.py](../../technik/arbiter/domaene/phasen/aufstellen.py))
ist der Schiedsrichter der Phase. Nur er hält den Stand: wer *an der Reihe* ist, wo jedes
*Modell* steht, was *aufgestellt* ist. Ändern lässt sich der Stand nur über seine Handlungen
(Gewinner und Zone wählen, `modellSetzen`, `aufstellenDerEinheitBeenden`), und jede prüft
erst alle Sperren, dann ändert sie ([Architektur](../../technik/architektur.md) D2, D3).
Darum liegt alles beisammen: Jede Sperre braucht den Stand; hielte ihn ein anderer, könnte
die Oberfläche an der Sperre vorbei schreiben.

*Prüfung, je Verantwortung: gehört sie hierher?*
- Gewinner, Zone (AUF-1.1, 1.2), *Einheit in Aufstellung* (AUF-7): ja, nur hier gibt es sie.
- *An der Reihe* (AUF-1.3, 1.7): heute ja, aber du hast recht: „abwechselnd, wer fertig
  ist, wird übersprungen“ kehrt im Nahkampf (`core_rules.txt:1941`) und bei der Moral
  (`:2095`) wieder. Ein Begriff des Spiels, nicht der Aufstellung allein.
- *Base überdeckt* (QUE-1.2): Die Regel liegt schon außerhalb, in `querschnitt.py`. Die
  Klasse sagt nur „gilt auch hier“, über eine überflüssige Umleitungsmethode.
- *Nahkampfreichweite* (AUF-3.4): nein. „Models cannot be set up within Engagement Range“
  (`core_rules.txt:450`) gilt für jedes *Setzen*, auch für Reinforcements. Der Code folgt der
  Anforderung, die sie zur Aufstellung stellt. Dein „quasi niemals“ stimmt: Die Zonen liegen
  26″ auseinander; greifen kann sie erst, wenn die Spieler ‚nicht ganz in der Zone‘ gemeinsam
  übergehen. Vorbild ohne Phase: `check_engagement_range` im Altbestand (`rule_checks.py`).
- *Ausgewählt* (AUF-5): nein, Bedienung statt Spielregel. AUF-5.5 (je Spieler höchstens
  zwei) würde sie weiter in die Klasse tragen.
- *Stellen* der Modelle: heute ja; Etappe 2 braucht sie auch.
- Zwei Spieler mit verschiedenen Armeen; zu welcher *Einheit* ein *Modell* gehört: Fragen an
  `Ausgangslage` und `Armee`.

*Lesbarkeit.* Modul und Klasse haben keinen Docstring, obwohl
[Es, S](../../prozess/praemissen/es.md#solid) einen verlangt; die Methoden folgen nicht der
Gliederung der Anforderung. 200 Zeilen ohne Landkarte.

*Urteil.* Der Gedanke trägt. Die Klasse mischt aber drei Arten Wissen: Regeln der Phase,
allgemeine Regeln des *Setzens*, Bedienzustand. Ein Umbau ist nötig, gezielt.

**Kosten.** Ohne Umbau wächst mit AUF-5.5 die Auswahl in die Klasse, und Etappe 2 löst
*Nahkampfreichweite* und *Stellen* unter Zeitdruck heraus.

**Gegenvorschlag.**

**F1 · Umfang des Umbaus.** Verhalten und Akzeptanztests bleiben.
- A Nur Landkarte: Docstrings, Methoden geordnet nach AUF-1, 3, 5, 7. Ein kurzer Lauf; die
  Mischung bleibt.
- B (Empfehlung) A und drei Schnitte vor AUF-5.5: Die Auswahl wird eine eigene kleine
  Klasse, die Aufstellung meldet ihr nur „aufgestellt“ (AUF-5.10); *Nahkampfreichweite*
  wird eine Funktion neben `baseÜberdeckt` in `querschnitt.py`, die Tabelle der Sperren
  zeigt direkt auf beide, die Umleitungen fallen weg; die Startprüfung zieht zu
  `Ausgangslage`, „Modell → Einheit“ zu `Armee`. Ein Lauf des Implementierers; die
  Architektur passe ich an. *An der Reihe* und *Stellen* bleiben, bis Etappe 5 und 2 sie
  brauchen (Architektur, Grundschnitt).
- C B und schon jetzt eigene Klassen für *an der Reihe* und *Stellen*. Zwei bis drei Läufe;
  ohne zweiten Nutzer drohen falsche Grenzen.

Antwort: .

**F2 · Anforderung.** Der Anforderungsautor überarbeitet gerade `aufstellen.md`. Soll ich
ihm vorschlagen, AUF-3.4 als allgemeine Regel des *Setzens* nach QUE-1 zu verschieben?
A ja (Empfehlung), B nein, sie bleibt bei der Aufstellung.

Antwort: Das würde ich nochmal infrage stellen. s. Stellungnahme.

**Stellungnahme.** Könntest du dich bitte mit dem Anforderungsautor abstimmen, wie wir es am besten machen? Ich habe 339 kommentiert und ihr sollt natürlich nicht unterschiedliche Strukturen aufbaut. Ich möchte, dass wir hier eine gemeinsame "Spiegelstruktur" aufbauen und die Einzelteile sollen lesbar und gut strukturiert sein. Daher finde ich F1-B einen guten Schritt. Schau bitte, was aus den Regeln heraus zusammengehört. Als Modell -> Einheit -> Armee könnte gut passen. Base und Nahkampfreichweite könnte auch irgendwie zusammengehören. Aber ich verstehe nicht viel davon, wie man Klassen, deren Eigenschaften, Methoden und Vererbungen gut aufbaut, damit alles gut strukturiert lesbar ist und so etwas wie SOLID erfüllt bleibt.
