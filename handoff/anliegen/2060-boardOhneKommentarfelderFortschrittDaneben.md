# Anliegenboard ohne Kommentarfelder, Fortschritt als Liste daneben

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der Stakeholder in [1670](1670-anliegenboardNachPhasen.md), letzte Zeile:
Kommentarfelder überall sind ihm zu offensiv, er kommentiert, wenn er ein Anliegen öffnet;
der Fortschritt soll kompakter sein und als kompakte Liste neben dem Anliegenboard stehen.
Gebaut ist mit P4: jede Karte des Boards trägt ein Kommentarfeld
(`rollenregeln/dashboardAnliegenSeiten.py`, `kommentarFeld`); der Fortschritt steht auf
einem eigenen Reiter, je Zeile mit Textfeld und Knopf „Abschicken“
(`rollenregeln/dashboardFortschritt.py`, `zeileHtml`). Die Regeln sind nachgezogen:
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) (Karten) und
[Ablauf, Fortschritt](../../prozess/ablauf.md#fortschritt) (Liste neben dem Board).
Einordnung nach Ich 3: kein Schritt des Happy Path, aber die Phase seiner Perspektive läuft;
darum ohne `Wartet auf:`.

**Kosten.** Der Stakeholder scrollt an einem Feld je Karte vorbei und wechselt den Reiter,
um zu sehen, wie weit die Phase ist; Board und Fortschritt stehen nie auf einem Blick.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): dieselben Stellen im Ablauf, kein neuer
Abschnitt; deine Zeilen zu Anliegen 1670 und 360 in `prozess/regeln.md` ziehst du nach.
1. Karte ohne Feld: Nummer und Titel als Link auf die Seite des Anliegens, darunter eine
   Zeile Form · Runde · von → an · wartet auf. Kommentar, Status und Antworten nur im
   Formular dieser Seite (`formular`, gibt es schon).
2. Die Startseite hat zwei Spalten: links das Board, rechts der Fortschritt der laufenden
   Phase als Liste, eine Zeile je Schritt mit Haken und Text; ein Hindernis eingerückt
   darunter, seine Nummer als Link auf die Seite des Anliegens. Im schmalen Fenster steht die
   Liste unter dem Board.
3. Der Haken gilt mit dem Klick, ohne Knopf; was ein Fakt abhakt, bleibt gesperrt. Ein Klick
   auf den Text der Zeile klappt ihr Kommentarfeld auf (`<details>`), sonst ist keins zu sehen.
4. Der Reiter „Fortschritt“ entfällt; `/fortschritt` bleibt Ziel der Formulare.

Erledigt, wenn Scheiter-Tests zeigen: Das Board enthält kein `name="kommentar"`, die Seite
eines Anliegens eins; die Startseite enthält jede Zeile des Fortschritts mit Haken, ihr
Kommentarfeld nur innerhalb von `<details>`; die Reiter sind Anliegen und Tokenbericht.

Bordmittel geprüft: keine; das Dashboard ist eigener Code und kein Hook-Code (kein Hook
importiert `dashboardAnliegen`, `dashboardAnliegenSeiten`, `dashboardFortschritt`,
`dashboardServer`), läuft also neben 2041.

**Stellungnahme.** Angenommen und umgesetzt. Karten ohne Feld (Kommentar nur auf der Seite des
Anliegens); die Startseite hat links das Board, rechts die Liste des Fortschritts, im schmalen
Fenster darunter; der Haken gilt mit dem Klick, ein Klick auf den Text klappt das Kommentarfeld
auf; ein Hindernis steht eingerückt, seine Nummer als Link; der Reiter „Fortschritt“ entfällt,
`/fortschritt` nimmt nur noch die Formulare an und leitet auf die Startseite. Scheiter-Tests:
`rollenregeln/dashboardFortschrittTest.py`, `dashboardAnliegenTest.py`, `dashboardServerTest.py`.
Mutationstest: Das Werkzeug mutiert nur Domänenmodule unter `technik/arbiter`; ein gezielter
Lauf auf die Dashboard-Dateien endete nicht innerhalb von zwei Minuten und blieb ungeprüft.
Kommentar: So sieht das schon besser aus, aber die unterschiedliche Formatierung der Haken in den Farben ergibt keinen Sinn. Außerdem ergibt es keinen Sinn, dass ich die Haken entfernen kann.
Stellungnahme: Eingearbeitet. Ein gesetzter Haken ist gesperrt und lässt sich nicht entfernen
(auch der Server setzt nur noch, nie zurück); alle Haken haben dieselbe Farbe, gesperrte wie
freie.
