# AUF-17 steht noch, obwohl es mit Item 1 entfällt

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Solange das
Kriterium steht, bleibt sein Test, und der wird rot, sobald der Implementierer „zurück“
entfernt.

[Item 1](../../domaene/items/aufraeumenUndFesteAdresse.md) sagt „Entfällt mit Test: AUF-17“,
[Plan 7](../plan.md) ebenso: „zurück“ (AUF-17) entfällt samt Test. Nach 2362 streichst du
AUF-13 und 17 und nimmst *zurück* aus dem Glossar. AUF-13 ist fort, aber
[AUF-17](../../domaene/anforderungen/phasen/aufstellen/zurueckOhneSperre.md) steht noch,
ebenso *zurück* im [Glossar](../../domaene/glossar.md) (Zeile 47). Darum hat der Testautor
[zurueckOhneSperreTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/zurueckOhneSperreTest.py)
zu Recht stehen lassen: Ein Test, dessen Kriterium noch steht, darf nicht fehlen.

**Kosten.** Bleibt es so, ist der Umfang von Item 1 nicht erfüllt, und die Abnahme
scheitert. Entfernt der Implementierer „zurück“ (`/api/zurück`) trotzdem, werden zwei Tests
zu AUF-17.1 rot, und die Rückverfolgung bleibt an einem Kriterium hängen, das nichts mehr
regelt.

**Gegenvorschlag.** Wie bei AUF-8.4 (2450), im Schritt des Testautors zu Item 1:
`zurueckOhneSperre.md` löschen und *zurück* aus dem Glossar nehmen, sofern kein Kriterium
es mehr nennt (per grep). Der Testautor löscht danach `zurueckOhneSperreTest.py` und den
Helfer `zurück` in `dienst.py`. Erledigt, wenn AUF-17 mit seinem Test gelöscht ist.

**Stellungnahme.** Angenommen und umgesetzt: `zurueckOhneSperre.md` (AUF-17) ist gelöscht,
die Zeile *zurück* aus dem [Glossar](../../domaene/glossar.md) genommen; per grep nennt kein
Kriterium mehr *zurück* oder AUF-17, nur noch [Item 1](../../domaene/items/aufraeumenUndFesteAdresse.md)
und [Plan 7](../plan.md). Die Kennung AUF-17 kommt nicht wieder. Offen beim Testautor:
`zurueckOhneSperreTest.py` und den Helfer `zurück` in `dienst.py` löschen; bis Code und Test
fort sind, kann `formregeln/glossar.py` an `zurück` rot werden.
