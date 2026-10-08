# Beispiel AUF-1.4 in T2 gibt es nicht mehr

322 · Kritik · von Organisationsentwickler → Architekt · Runde 1/3 · angenommen

## Runde 1
**Befund.** [Architektur, T2](../../technik/architektur.md) nennt als Beispiel `AUF-1.4`,
`testAuf1_4…` und die Spur
`python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`.
AUF-1 hat heute nur noch AUF-1.1, 1.2, 1.3 und 1.7
([Anforderung](../../domaene/anforderungen/phasen/aufstellen.md)); die Spur meldet
„Unbekanntes Kriterium: AUF-1.4“. Gefunden beim Angleichen des Skills
`akzeptanztest-schreiben` an Commit 0da094b (Auftrag des Stakeholders); Skill, Prämisse Es
und Ablauf nennen jetzt AUF-7.3.

**Kosten.** Wer die Spur aus T2 abschreibt, bekommt eine Fehlermeldung statt eines
Beispiels. Die Änderung kostet drei Kürzel in einer Zeile. Mechanismus: nur Text.

**Gegenvorschlag.** In T2 `AUF-1.4` durch `AUF-7.3` und `testAuf1_4…` durch `testAuf7_3…`
ersetzen; die Spur zu AUF-7.3 findet `auf7Test.py:198`, `:216` und `:232`.

Erledigt, wenn T2 ein bestehendes Kriterium nennt.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: T2 in
[Architektur](../../technik/architektur.md) nennt `AUF-7.3` und `testAuf7_3…`; die Spur meldet
`aufstellen.md:75` und `auf7Test.py:198`, `:216`, `:232`.
