# Prüfung der Mockups: Lücken bei `style=` und Absturz bei fremden Dateien

217 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von cef00fc (Anliegen 200). Die Tests laufen grün (81 passed);
ein Versuch mit `htmlVerstöße` und `verstöße` zeigt vier Lücken:
1. `prozess/pruefungen/mockups.py:15`: `kleinText.replace(" ", "")` entfernt nur
   Leerzeichen. `<p style\t="x">` und `<p\n style\n="x">` sind grün, obwohl die Stellungnahme
   zu 200 „auch mit Leerzeichen“ zusagt. Umgekehrt ist sichtbarer Text oder ein fremdes
   Attribut rot: `<p data-style="x">` und `<p>style=fett</p>` melden `style=`.
2. `mockups.py:25`: `read_text(encoding="utf-8")` läuft vor der Prüfung der Endung. Eine
   Datei, die kein UTF-8 ist (Bild, Swap-Datei des Editors), wirft `UnicodeDecodeError`;
   die Prüfung bricht ab, statt zu melden. Dasselbe in `hoechstmassTest.py:51`
   (`mockupFälle` ruft `zeichen` beim Sammeln): Dann fällt das Sammeln des ganzen Moduls aus,
   und kein Höchstmaß im Repo wird mehr geprüft.
3. `mockups.py:27,29`: Die Endung wird ohne Kleinschreibung verglichen, alles außer `.html`
   und `.css` bleibt ungeprüft und grün. `A.HTML`, `b.htm` oder `c.svg` mit `<script>` laufen
   durch. Die Rolle [UX](../../.claude/agents/ux.md) kennt nur `<kennung>.html` und
   `vorschlag.css`.
4. `mockups.py:32`: Die Meldung nennt `datei.name`, die Suche läuft aber rekursiv
   (`rglob`). Zwei gleichnamige Dateien in Unterordnern sind in der Meldung nicht zu
   unterscheiden; `kommentare.py` nennt den Pfad relativ zur Wurzel.

**Kosten.** Zu 1 und 3: Ein Verstoß, den die Prüfung laut `prozess/regeln.md` sperrt, erreicht
den Stakeholder doch, also genau die Kosten aus 200. Zu 2: Eine einzige fremde Datei im
Mockup-Ordner schaltet alle Höchstmaße des Repos ab, nicht nur die der Mockups. Zu 1
(falsch rot): Ein Mockup mit dem Wort im Text wird gesperrt, ohne gegen die Regel zu
verstoßen.

**Gegenvorschlag.**
1. Attribut nur innerhalb eines Tags suchen, mit jedem Leerraum:
   `re.compile(r"<[^>]*\sstyle\s*=", re.IGNORECASE)` (`[^>]` deckt auch Zeilenumbrüche).
2. und 3. Endung zuerst prüfen, klein geschrieben: `.html` und `.css` wie bisher, jede andere
   Datei ist ein Verstoß („nur .html und .css“) und wird nicht gelesen. `mockupFälle` zählt
   nur `.html` und `.css`; den Rest meldet `mockups.py`.
4. Meldung mit `datei.relative_to(wurzelOrdner).as_posix()`.

Je ein Scheiter-Fall in `mockupsTest.py`: Tab und Zeilenumbruch vor `=` rot, `data-style=`
und Text `style=` grün, `A.HTML` mit `<script>` rot, `bild.png` mit Bytes, die kein UTF-8
sind, rot ohne Ausnahme. `prozess/regeln.md` (Zeile UX-Mockups) nennt dann „nur `.html` und
`.css`“.

Erledigt, wenn die Fälle grün laufen und `regeln.md` die Erweiterung nennt.

**Stellungnahme.** Umgesetzt, alle vier Punkte.
