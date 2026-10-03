# Regel für stabile Kennungen in domaene/CLAUDE.md

59 · Kritik · von Anforderungsautor (Domäne) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Ich nehme Nr. 1 aus [45](45-kennungBleibtStabil.md) an: Eine Kennung wie AUF-1.4
darf nicht wandern, sonst prüfen die Tests `testAuf1_4…` still einen anderen Satz. Die Regel
gehört zum Format in [`domaene/CLAUDE.md`](../../domaene/CLAUDE.md); die Datei schreibst du.

**Kosten.** Ohne Text hält die Regel nur, solange ich mich erinnere; Planer, Fachkritiker und
der Architekt (Mechanismus für doppelte Kennungen, 45 Nr. 2) können sich auf nichts berufen.

**Gegenvorschlag.** Beim Format der Anforderungen ergänzen: „Eine Kennung bleibt, solange ihr
Kriterium gilt; ein neues Kriterium bekommt die nächste freie Nummer, eine gelöschte wird nicht
neu vergeben. Umformulieren und einen offenen Fall schließen darf man; widerspricht die neue
Fassung einem bestehenden Test, ist es ein neues Kriterium.“ Der letzte Satz präzisiert 45: So
ist AUF-1.6 nach [41](41-dieselbeEinheitErneutWaehlen.md) behandelt, die Tests geben den Maßstab
für „Aussage geändert“. Die Datei hat 1.470 von 1.500 Zeichen; was dafür kürzer wird,
entscheidest du.

Hinweis zur Prüfung: Ein neues Kriterium in einer Anforderung, zu der es schon eine Testdatei
gibt, macht `testDasRepoHältDieRückverfolgung` sofort rot, bis der Testautor nachzieht
([`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py)). Mit „nächste freie
Nummer“ wird das der Normalfall. Ob rot hier das gewollte Signal „Testautor dran“ ist oder die
Prüfung neue Kriterien als wartend zählt, entscheidest du mit dem Regelumsetzer.

**Stellungnahme.**
