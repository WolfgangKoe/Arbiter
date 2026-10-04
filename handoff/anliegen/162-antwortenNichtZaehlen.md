# Antworten des Stakeholders zählen nicht gegen das Höchstmaß

162 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 2/3 · offen

## Runde 1
**Befund.** `hoechstmassTest.py` zählt ein Anliegen samt den Antworten des Stakeholders. Mit
ihnen hatte [145](145-ersteOberflaecheImBrowser.md) 4.063 Zeichen, der Test war rot. Der
Stakeholder entscheidet die Regel in Anliegen 161, F1; empfohlen
ist A. Dieses Anliegen gilt für A, sobald 161 beantwortet ist (auch mit „.“); bis dahin
wartet es. Bei B oder C ändere ich es in einer neuen Runde.

**Kosten.** Ohne Mechanismus wird jede ausführliche Antwort zum roten Commit der Freigabe,
und eine Rolle kürzt fremden Text.

**Gegenvorschlag.** Für Anliegen zählt `hoechstmassTest.py` jede Zeile, die auf
`anliegen.antwortZeile` passt, als `Antwort: .`; die übrigen Höchstmaße bleiben, wie sie sind.
Die Zählregel steht einmal, etwa als Funktion neben `zeichen`, der Ausdruck kommt aus
`anliegen.py`. Scheiter-Test: Ein Anliegen mit 3.990 Zeichen eigenem Text und einer Antwort
von 500 Zeichen ist grün; dasselbe mit 4.010 Zeichen eigenem Text bleibt rot.
`prozess/regeln.md` nennt den Mechanismus; den Satz in `prozess/ablauf.md` (Anliegen) setze ich.

Erledigt, wenn beide Fälle des Scheiter-Tests so ausgehen, `python3 -m pytest
prozess/pruefungen` grün ist und der Reviewer den Code geprüft hat
([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)).

**Stellungnahme.** Umgesetzt: `zeichenOhneAntworten` in `hoechstmassTest.py`, Scheiter-Test mit 3.980 und 4.010 Zeichen
eigenem Text; Eintrag in `prozess/regeln.md`. Reviewer-Prüfung steht aus.

## Runde 2
**Befund.** Die Kritik am Code zu 4f9ce03 ([190](190-antwortRegelGreiftNicht.md)) zeigt:
`testDateiHältIhrHöchstmaß` zählt über `überschreitet` weiter samt Antworten; die Regel greift
nicht, die Scheiter-Tests gehen am echten Weg vorbei.

**Kosten.** Wie in Runde 1. Bis dahin steht die Regel in `prozess/ablauf.md` als nur Text.

**Gegenvorschlag.** Umsetzen nach 190. 3.980 statt 3.990 Zeichen nehme ich an (die Zeile
`Antwort: .` zählt mit). Erledigt, wenn 190 erledigt ist; den Mechanismus trage ich dann in
`prozess/ablauf.md` ein.
