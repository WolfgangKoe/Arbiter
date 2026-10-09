# Review · Zyklus 4

Inkrement: `technik/` seit `Freigabe Plan 4` (`fcb42f8`), Stand `585e8b9`. Items aus
[Plan 4](plan.md): *Vorläufiger Start* (AUF-6.1), *Auswählen in der Ablage* (AUF-5, QUE-3.1),
*Stand behalten* (QUE-3.2, QUE-3.3).

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 286 grün. Abdeckung `technik/arbiter`
   99 % Zeilen, 100 % Zweige; offen nur `__main__.py` 22–24 (Strg+C), wie in Review 3.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 440 grün, darin ruff, eslint und
   stylelint; SonarLint: keine Funde. Nur Einheitstests erreichen `aufstellen.py` 32, 34,
   120, 125, 178, 216, 225, `katalog/ausgangslage.py` 21, 51, 53, 56 und `web/anwendung.py`
   31, 34: alles Vorbedingungen (`ValueError`; 404 nach V2). Glossar → Code: *ausgewählt*
   und *Ablage* stehen wörtlich in Domäne, `web/` und `seite.js`.
3. **Erfüllt.** Items gelöscht (`585e8b9`); AUF-5, AUF-6 und QUE-3 beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle drei Items ohne Befund abgenommen (`585e8b9`).

Oberfläche: Bildschirmtests grün, „ausgewählt“ in `komponenten.css` gleicht `vorschlag.css`.
**Nicht erfüllt:** „Mockup gelöscht“, fünf Mockups liegen noch
([348](anliegen/348-mockupsNachDemEinbauLoeschen.md), [349](anliegen/349-vertragOhneLinkAufsMockup.md)).

## Code
`/code-review` je Lauf als Kritik am Code; der Umbau nach 344 ist nachgeprüft (347 erledigt),
kein Befund offen. V2 hält: `PUT` und `DELETE` idempotent, 404 außerhalb der *Ablage*,
`TRUSTED_HOSTS` nach V4; die Seite zeichnet die Antwort. Die Domäne kennt Flask nicht.

## Offene Anliegen zur Technik
[339](anliegen/339-klasseAufstellungErklaertUndGeprueft.md) (an dich),
[345](anliegen/345-spiegelZwischenAnforderungUndCode.md) (Spiegel),
[249](anliegen/249-werkzeugFestUndImportvertragDerTests.md) (Regelumsetzer), 348, 349.

## Empfehlung
Freigeben: DoD 1 bis 4 erfüllt; 348 und 349 ändern kein Verhalten.

## Rundgang Prüfcode
Seit Review 3 (`38aae1f`) vor allem Rückbau: 50 Dateien gelöscht, 4.856 Zeilen weg, 336 neu;
Hook-Befehle in `.claude/settings.json` von 18 auf 8. Neu oder geändert:
`rollenregeln/pfadsperren.py` (Schreibgrenze), `standregeln/phasenfolge.py` mit
`phasenfolgeTest.py`, `formregeln/abdeckung.py` (`aussetzung` ohne Phase), `pyproject.toml`
(Sammelfehler brechen nicht ab, 304; pytest und pre-commit fest, 346),
`.pre-commit-config.yaml` (Hook `sonarlint`, 216; `abdeckungPruefskripte` weg).
1. Rest des Rückbaus: `pyproject.toml:12` begründet den Marker `stand` mit der Messung der
   Prüfskripte, die es nicht mehr gibt; den Parameter `auswahl` von `abdeckungMessen` nutzt
   nur sein eigener Test (`abdeckungTest.py:81`). Vorschlag: Marker, Parameter, Test streichen.
2. `pfadsperren.py` ist eine Tabelle mit einem Eintrag; nach es.md 9 genügt ein `if`, bis ein
   zweiter kommt.
3. Bash und Read haben keinen Hook mehr; die Schreibgrenze gilt nur für Write und Edit
   (ich.md 2).

## Nächstes Vorgehen
- **Produktziel:** Keine der 7 Etappen erreicht. Am meisten fehlt das *Setzen* am
  Bildschirm: Die Domäne setzt und sperrt (AUF-3, AUF-7), die Karte nimmt noch kein Modell an.
- **Etappenziel:** Es fehlt „Danach“ aus Plan 4: Ziehen (setzen, umsetzen, zurücklegen),
  Gewinner und Zone am Bildschirm statt AUF-6, zurück, gemeinsam übergehen, Protokoll,
  Beenden mit fehlenden Modellen und Kohärenz. Für Ziehen, zurück, übergehen, Protokoll und
  Kohärenz fehlen Kriterien (grep in `domaene/anforderungen/`: kein Treffer). Schätzung:
  3 Zyklen, mit Kohärenz (`core_rules.txt:434`) eher 4.
- **Zyklusziel:** Plan 5: Setzen durch Ziehen mit Maus und Touch, *Sperre* mit *Grund*.
  Vorher entscheiden 345 (Spiegel) und 340 (Schnitt der Anforderung), sonst ziehen Tests und
  Module nach dem Schreiben um; dann Kriterien fürs Ziehen. Technik: Vertrag fürs Setzen mit
  der Antwort bei *Sperre*, Wegwerf-Versuch zum Ziehen (Neuland), 249 (Werkzeug fest für
  `server.py`). AUF-5.5 und die Auswahl als Klasse erst nach 345.

## Freigabe
Freigabe: offen
Kommentar: .
