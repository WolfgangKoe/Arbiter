# Antworten des Stakeholders nach der Freigabe aufgreifen

119 · Kritik · von Architekt (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

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
