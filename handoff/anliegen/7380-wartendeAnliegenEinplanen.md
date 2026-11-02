# Wartende Anliegen für die nächste Phase einplanen

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Notiere für die passende Rolle, dass wartende Anliegen für die nächste Phase auch
eingeplant werden.“

Festgehalten vom Organisationsentwickler nach der [Moderation](../moderation.md),
Vorschläge. Anlass: Wartende Kriterien (AUF-29, AUF-22, AUF-27 und weitere) stehen in Items
außerhalb von Plan 9, und der Abschnitt „Danach“ des Plans nennt anhaltenAufDemWeg,
randfaelleDesAufstellens und gewinnerUndZone nicht.

Bestehende Regeln, die es abdecken oder angepasst abdecken können ([Ich 4](../../prozess/praemissen/ich.md)):
- [Domänenphase](../../prozess/ablauf/domaenenphase.md) 4 und 6: Der Anforderungsautor
  schreibt ohne Zyklusziel zum Abschnitt „Danach“ des vorigen Plans; der Planer stellt den
  Plan aus bereiten Items zusammen.
- [Kritik](../../prozess/ablauf/kritik.md): Befunde, die auf die nächste Phase der
  Perspektive des Autors warten, stehen in einem eigenen Anliegen mit `Wartet auf: <Phase>`.
- [Status der Anliegen](../../prozess/ablauf/anliegenStatus.md), letzter Punkt: Wartende
  sind nicht dran, bis die Phase läuft.

**Kosten.** Ein Lauf des Regelumsetzers und ein kurzer des Organisationsentwicklers (Retro 9, P8).

**Gegenvorschlag.** Keiner.

**Stellungnahme.** Umgesetzt mit P8 der [Retro 9](../retro.md). Wartet ein Anliegen auf die
Domänen- oder Technikphase, steht es dort als Zeile im Fortschritt: „<Rolle, die dran ist>:
Anliegen <nr> <Titel>“, im Review vor „Planer: Plan geschrieben“, im Plan vor der DoD,
abgehakt, sobald es `angenommen` ist ([Fortschritt](../../prozess/ablauf/fortschritt.md),
Tabelle). Wartet es auf die Prozessphase, nennt ein Prozess-Item der Retro seine Nummer
([Prozessphase](../../prozess/ablauf/prozessphase.md) 1). Zusammengefasst im letzten Punkt
von [Status der Anliegen](../../prozess/ablauf/anliegenStatus.md). Mechanismus:
`standregeln/wartendeSchritte.py` ([Standregeln](../../prozess/regeln/standregeln.md));
Prozess-Item: nur Text. `erledigt` folgt dem Haken von P8 im Fortschritt der Retro.
