# Antworten des Stakeholders nach der Freigabe aufgreifen

119 · Kritik · von Architekt (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · erledigt

## Runde 1
**Befund.** [83](83-sprungErproben.md) blieb nach `Freigabe Plan 2` liegen: Der Stakeholder
hatte unter F1 geantwortet, der Kopf stand wie verlangt auf `offen` (→ Stakeholder). Laut
[Ablauf, Anliegen](../../prozess/ablauf.md#anliegen) setzt der Absender `beantwortet` „nach
der Freigabe“, aber nichts nennt ihn dann: `stand.py` (`wartetAuf`) liest nur den Kopf und
meldet weiter den Stakeholder. Die Moderation hatte es vermerkt, der Stand nicht. Gleiches
droht bei `eskaliert`: Schreibt der Stakeholder seine Entscheidung und lässt den Kopf stehen,
bleibt er dran.

**Kosten.** Antworten des Stakeholders warten unbemerkt, bis er nachfragt; bei 83 hielt er
das für wichtig, bevor das Inkrement weiter wächst.

**Gegenvorschlag.** Eins von beiden, deine Wahl:
- Der Stand meldet den Absender, wenn ein Anliegen mit Fragen an den Stakeholder (`offen`
  oder `eskaliert`) älter ist als die letzte Freigabe oder eine Zeile `Antwort:` mit mehr als
  „.“ trägt. Mechanismus in `stand.py` und `anliegen.py`, je ein Scheiter-Test.
- Der Koordinator setzt beim Commit einer Freigabe den Kopf jedes beantworteten Anliegens auf
  `beantwortet` (Recht dafür in `statusrecht.py`).

Erledigt, wenn ein beantwortetes Anliegen nach der Freigabe den Absender als dran meldet,
mit Test.

**Stellungnahme.** Erster Vorschlag, enger gefasst. Der zweite scheidet aus: Der Koordinator
schreibt keine Dateien. Regel in [Ablauf, Anliegen](../../prozess/ablauf.md#anliegen): Ein
Anliegen an den Stakeholder mit Status `offen`, seit der letzten Freigabe unverändert, hat
die Freigabe beantwortet; dran ist der Absender. Das deckt auch eine Zeile `Antwort:` mit
mehr als „.“, denn die Freigabe beantwortet jede Frage der Vorlage; vor der Freigabe bleibt
der Stakeholder dran. `eskaliert` bleibt bei ihm: Mit seiner Entscheidung setzt er den Kopf
selbst (nur er darf `eskaliert` ändern), bis dahin nennt ihn der Stand zu Recht.
Umgesetzt mit Anliegen 121 (89364ab): `anliegen.py` (`wartetAuf`),
`gitAufruf.py` (`seitFreigabeUnverändert`), Fälle in `anliegenTest.py`.

**Nachprüfung.** In Ordnung: 83 meldete nach der Freigabe den Absender. Dass jede spätere
Änderung der Datei die Antwort kippt, verfolgt
[125](125-importvertragRelativUndFreigabeAntwort.md), Punkt 2.
