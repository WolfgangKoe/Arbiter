# Kritik

Je Artefakt prüft jeder seiner Kritiker einmal und ordnet jeden Befund nach
[Ich 3](../praemissen/ich.md) ein. Die aufhaltenden Befunde an einen Autor stehen in einem
Anliegen, die wartenden in einem zweiten mit `Wartet auf: <Phase>` der Perspektive des
Autors; was entfällt, schreibt er nicht, ohne Befund keine Datei. Der Autor bessert nach
oder widerspricht; eine weitere Runde öffnet der Kritiker nur für, was weiter aufhält, nach
Runde 3 entscheidet der Stakeholder ([Status der Anliegen](anliegenStatus.md)). Die Kritiker eines Artefakts
laufen gleichzeitig. Befunde stehen nur in Anliegen, nie nur in einer Schlussantwort
([Ich 5](../praemissen/ich.md)). Wer kritisiert (Anliegen 730):

Artefakt | Autor | Kritiker
---|---|---
Anforderungen, Mockups (Domäne 5) | Anforderungsautor, UX | Fachkritiker (Ziel, Regeltext, Happy Path)
Plan, Items, Anforderungen, Mockups (Domäne 7) | Planer, Anforderungsautor, UX | Architekt (prüfbar, Kosten, Schnitt, vorhandene Komponenten), Fachkritiker (Etappe)
`technik/tests/akzeptanz/` | Testautor | Fachkritiker (Kriterium), Architekt (Schnittstelle, Lesbarkeit)
`technik/arbiter/`, `technik/tests/einheit/`, `technik/frontend/` | Implementierer | Architekt (Architektur), Reviewer (Lesbarkeit)
Review | Reviewer | Fachkritiker (Klickpfad und Zyklusziel gegen Plan und Etappe), Organisationsentwickler (Form nach Technikphase 6, Rundgang vollständig, [Wir 5](../praemissen/wir.md))
Retro | Organisationsentwickler | Fachkritiker, Architekt
`pyproject.toml`, Linter-Konfiguration | Regelumsetzer | Architekt (schränkt sie die Technik richtig ein?)

Mechanismus: nur Text.

## Kritik am Code
Nach jeder Änderung von Code nach der Tabelle prüfen ihn seine Kritiker, bevor die nächste
Rolle darauf aufbaut; sie lesen die Änderung seit dem Commit, den der Auftrag nennt
(`git diff <commit>`). Den Code
der Prüfskripte und Hooks kritisiert niemand je Änderung; dafür gibt es den Rundgang
([Technikphase](technikphase.md), Schritt 6). Mechanismus: nur Text.
