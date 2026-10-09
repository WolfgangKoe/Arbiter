# Review · Zyklus 4

Start der App: `.venv/bin/arbiter` aus der Wurzel ([Web, W5](../technik/architektur/web.md#aufbau)).

Inkrement: `technik/` seit Commit „Freigabe Plan 4“, Stand Commit „Architekt: Vertrag ohne
Link aufs Mockup (Anliegen 349), Nachprüfung 339“. Items aus [Plan 4](plan.md): *Vorläufiger
Start* (AUF-6.1), *Auswählen in der Ablage* (AUF-5, QUE-3.1), *Stand behalten* (QUE-3.2, QUE-3.3).

## Am Bildschirm prüfen
Jetzt per Maus oder Finger machbar: Einheiten in der *Ablage* auswählen und abwählen, sonst
nichts. Klickpfad, so am laufenden Arbiter durchgegangen:
1. In der Wurzel `.venv/bin/arbiter` starten, die genannte Adresse im Browser öffnen.
   Erwartet: links „Spieler 1“ mit Boyz (10) und Warboss (1), rechts „Spieler 2“ mit Necron
   Warriors (10) und Overlord (1); oben rechts „Spieler 2 · an der Reihe“; auf der *Karte*
   links eine blaue, rechts eine rote *Aufstellungszone*, kein *Modell*; nichts *ausgewählt*.
2. Auf „Boyz“ klicken: die Karte bekommt einen Rahmen in der Farbe ihres Spielers (*ausgewählt*). Auf „Warboss“
   klicken: beide gerahmt. Das geht auch beim Spieler, der nicht *an der Reihe* ist.
3. Die Seite neu laden: beide bleiben gerahmt.
4. Auf „Boyz“ klicken: nur noch „Warboss“ gerahmt. Wer *an der Reihe* ist, bleibt gleich.
5. Arbiter mit Strg+C beenden und neu starten: nichts *ausgewählt* (Stand von Schritt 1).

Nicht am Bildschirm zu sehen: das gerahmte *Modell* auf der *Karte* (AUF-5.7), weil sich noch
kein *Modell* setzen lässt; das prüft nur der Bildschirmtest.

## DoD
1. **Erfüllt.** `python3 -m pytest technik/tests`: 286 grün. Abdeckung `technik/arbiter`
   99 % Zeilen, 100 % Zweige; offen nur `__main__.py` 22–24 (Strg+C), wie in Review 3.
2. **Erfüllt.** `python3 -m pytest prozess/pruefungen`: 444 grün, darin ruff, eslint und
   stylelint; SonarLint: keine Funde. Nur Einheitstests erreichen `aufstellen.py` 32, 34,
   120, 125, 178, 216, 225, `katalog/ausgangslage.py` 21, 51, 53, 56 und `web/anwendung.py`
   31, 34: alles Vorbedingungen (`ValueError`; 404 nach V2). Glossar → Code: *ausgewählt*
   und *Ablage* stehen wörtlich in Domäne, `web/` und `seite.js`.
3. **Erfüllt.** Items gelöscht (Commit „Planer: abgenommene Items von Plan 4 gelöscht“);
   AUF-5, AUF-6 und QUE-3 beschreiben das Gebaute.
4. **Erfüllt.** Der Fachkritiker hat alle drei Items ohne Befund abgenommen.

Oberfläche: **Erfüllt.** Bildschirmtests grün, „ausgewählt“ in `komponenten.css` gleicht
`vorschlag.css`. Die fünf Mockups sind gelöscht, nur `domaene/mockups/vorschlag.css` bleibt;
V1 im Vertrag beschreibt `spielstand.json` selbst, die Datei stimmt damit überein (348 und
349 nachgeprüft, erledigt).

## Code
`/code-review` je Lauf als Kritik am Code; der Umbau nach 344 ist nachgeprüft (347 erledigt),
kein Befund offen. V2 hält: `PUT` und `DELETE` idempotent, 404 außerhalb der *Ablage*,
`TRUSTED_HOSTS` nach V4; die Seite zeichnet die Antwort. Die Domäne kennt Flask nicht.
Wiederverwendung, Vereinfachung, Effizienz, Flughöhe: kein Befund.

## Offene Anliegen zur Technik
[345](anliegen/345-spiegelZwischenAnforderungUndCode.md) (Spiegel, beim Anforderungsautor),
[249](anliegen/249-werkzeugFestUndImportvertragDerTests.md) (Regelumsetzer).

## Empfehlung
Freigeben: DoD 1 bis 4 und die Oberfläche erfüllt.

## Rundgang Prüfcode
Seit Commit „Reviewer: Empfehlung zu den Prüfungen der Codequalität im Rückbau“ vor allem
Rückbau: 50 Dateien gelöscht, 4.856 Zeilen weg, 336 neu. Neu oder geändert:
`rollenregeln/pfadsperren.py` (Schreibgrenze), `standregeln/phasenfolge.py` mit
`phasenfolgeTest.py`, `formregeln/abdeckung.py` (`aussetzung` ohne Phase), `pyproject.toml`
(Sammelfehler brechen nicht ab, 304; pytest und pre-commit fest, 346),
`.pre-commit-config.yaml` (Hook `sonarlint`, 216; `abdeckungPruefskripte` weg). Angepasst an
den Rückbau: `anliegenregeln/` `anliegen.py`, `anliegenDran.py` (Status `rückfrage`),
`formregeln/` `benennung.py`, `importvertrag.py`, `sonarlint.py`, `gemeinsam/` `gitAufruf.py`,
`pfade.py`, `lesen/` `anliegenKopf.py`, `plan.py`, `rollenregeln/` `dashboard.py`,
`laufLog.py`, `schreibgrenze.py`, `standregeln/` `anliegenText.py`, `stand.py`.
Hooks in `.claude/settings.json` von 18 auf 8: SessionStart `standregeln.stand`; PreToolUse
`standregeln.belegung` und, für Write und Edit, `rollenregeln.schreibgrenze`; PostToolUse
`standregeln.belegung` und, für Agent, `standregeln.stand`; SubagentStart
`rollenregeln.rollenkontext`; SubagentStop `rollenregeln.laufLog` und
`anliegenregeln.erledigteLoeschen`.
1. Rest des Rückbaus: `pyproject.toml:12` begründet den Marker `stand` mit der Messung der
   Prüfskripte, die es nicht mehr gibt; den Parameter `auswahl` von `abdeckungMessen` nutzt
   nur sein eigener Test (`abdeckungTest.py:80`). Vorschlag: Marker, Parameter, Test streichen.
2. `pfadsperren.py` ist eine Tabelle mit einem Eintrag; nach es.md 9 genügt ein `if`, bis ein
   zweiter kommt.
3. `laufLog.py:137` und `dashboard.py:100` lesen die Lage je Lauf zweimal (git und Plandateien);
   der Schutz, der einen Fehler darin vom Eintrag fernhielt, ist mit `zyklusUndPhase` gegangen.
   Vorschlag: `dashboardSchreiben` bekommt die Lage aus `protokollieren`.

## Nächstes Vorgehen
- **Produktziel:** Keine der 7 Etappen erreicht. Am meisten fehlt das *Setzen* am
  Bildschirm: Die Domäne setzt und sperrt (AUF-3, AUF-7), die Karte nimmt noch kein Modell an.
- **Etappenziel:** Es fehlt „Danach“ aus Plan 4: Ziehen (setzen, umsetzen, zurücklegen),
  Gewinner und Zone am Bildschirm statt AUF-6, zurück, gemeinsam übergehen, Protokoll,
  Beenden mit fehlenden Modellen und Kohärenz. Ohne Kriterium (grep in
  `domaene/anforderungen/`: kein Treffer): Ziehen samt Zurücklegen, „bleibt mit Grund
  stehen“, zurück, übergehen, Protokoll, Beenden mit fehlenden Modellen, Kohärenz.
  Schätzung: 3 Zyklen, mit Kohärenz (`core_rules.txt:434`) eher 4.
- **Zyklusziel:** Plan 5. Nach Zyklus 5 am Bildschirm machbar, mit Maus oder Finger:
  ein *Modell* der *Einheit*, die gerade aufgestellt wird, aus der *Ablage* auf die *Karte*
  ziehen (es erscheint als Kreis und die Zahl in der *Ablage* sinkt), es auf der *Karte*
  verschieben und zurück in die *Ablage* ziehen. Lässt man es außerhalb der eigenen Zone, auf
  einem anderen *Modell* oder zu nah an einem Gegner los, bleibt es gesperrt stehen und nennt
  den *Grund*; „zurück“ stellt es an die vorige Stelle, sonst in die *Ablage*
  ([Etappe 1](../domaene/etappen/01-aufstellen.md)). Ohne „zurück“ stünde das erste gesperrte
  *Modell* fest. Noch nicht machbar: „gemeinsam übergehen“ und das Protokoll (Plan 6, weil
  jedes Übergehen protokolliert wird, `domaene/ziel.md`), Gewinner und Zone wählen, das
  Aufstellen der *Einheit* beenden.
  Voraussetzungen: Vorher entscheiden 345 (Spiegel) und 340 (Schnitt der Anforderung), sonst
  ziehen Tests und Module nach dem Schreiben um; dann die Kriterien. Technik: Vertrag fürs
  Setzen mit der Antwort bei *Sperre*, Wegwerf-Versuch zum Ziehen (Neuland), 249 (Werkzeug
  fest für `server.py`). AUF-5.5 nach 320 B erst mit einer *Armee* von mehr als zwei
  *Einheiten*; die Auswahl als Klasse erst nach 345.

## Freigabe
Freigabe: ja
Kommentar: Den Startbefehl für die lokale App bitte dauerhaft in die Review schreiben und dort auch anpassen, wenn er geändert wird. Aktuell scheint es dieser hier zu sein
.venv/bin/arbiter
Stellungnahme: Der Befehl stimmt (W5, `[project.scripts]` in `pyproject.toml`); er steht jetzt unter der ersten Zeile mit Link auf W5. Dass jedes Review ihn trägt, regelt der Ablauf, Schritt 6: Anliegen Anliegen 353 an den Organisationsentwickler. Commits nenne ich mit ihrem Betreff statt der Kennung (Frage in 351, Regel für alle: Anliegen 354).
Weiterer Kommentar: Mir fehlt hier im Review noch eine manuelle Prüfungkomponente am Frontend für den Stakeholder. Idealerweise auch mit einem klaren Klickpfad. Und es fehlt auch eine Steuerungskomponente für die Fachlichkeit. Es ist ja nett, dass du immer schon Produkt- und Etappenziel benennst. Aber Zyklusziel Setzen, Umsetzen und Zurücklegen blablabla... ist irgendwie nicht wirklich verständlich. Was ist denn jetzt wirklich im Frontend per Maus machbar? Und was soll nach dem nächsten Zyklus machbar sein?
Stellungnahme: Neu ist der Abschnitt „Am Bildschirm prüfen“ unter dem Startbefehl: was jetzt per Maus machbar ist, als Klickpfad mit erwartetem Bild, am laufenden Arbiter durchgegangen. Das Zyklusziel unter „Nächstes Vorgehen“ sagt jetzt zuerst, was nach Zyklus 5 am Bildschirm machbar ist und was noch nicht; danach folgen die Voraussetzungen. Damit jedes Review beides hat, braucht es Schritt 6 im Ablauf: Anliegen Anliegen 355 an den Organisationsentwickler.
