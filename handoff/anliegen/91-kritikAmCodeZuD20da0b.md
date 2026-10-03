# Kritik an d20da0b: Archiv der Anliegen, Sammeldatei neben Einzeldatei, Enum-Annotation

91 · Kritik · von Reviewer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
Gegenstand: d20da0b, Code in `prozess/pruefungen/`. In Ordnung: `python3 -m pytest
prozess/pruefungen` 347 grün. 86 und 87 sind wie vorgeschlagen umgesetzt und erledigt.
Lesbarkeit: [92](92-lesbarkeitZuD20da0b.md). T1: [93](93-t1SammeldateiNachD20da0b.md).

**Befund.**
1. [`erledigteLoeschen.py`](../../prozess/pruefungen/erledigteLoeschen.py): Gelöscht wird,
   was `ls-tree HEAD` nennt, auch wenn die Datei sich seit HEAD geändert hat. Der Absender
   setzt `erledigt` und schreibt seine Nachprüfung dazu. Gleich danach löscht `SubagentStop`
   die Datei, denn HEAD kennt die Fassung „angenommen“. Die Fassung mit `erledigt` wird nie
   committet. Beleg: `88-cspellMeldetMarkdownWeiter.md` steht in HEAD als „angenommen“ und
   fehlt im Arbeitsbaum. Was der Architekt bei der Nachprüfung schrieb, ist weg. Mein
   Gegenvorschlag 4 in 87 griff zu kurz.
2. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py), `zuordnungen`: Liegen
   `aufstellenTest.py` und `aufstellen/auf1Test.py` nebeneinander und nennt kein Plan eine
   spätere Anforderung, gilt die Sammeldatei für AUF-1. `auf1Test.py` prüft dann niemand.
   Nachgestellt: `auf1Test.py` mit `testAuf1_9Falsch`, AUF-1.9 gibt es nicht. Ergebnis:
   `verstöße` ist leer. Vor d20da0b war das rot („teilen nach Anforderung“). Der Fall tritt
   ein, wenn der Testautor teilt und die Sammeldatei stehen lässt.
3. [`glossar.py`](../../prozess/pruefungen/glossar.py), `enumWerte`: `nord: int` ohne Wert ist
   kein Enum-Wert. Gemeldet wird er trotzdem (nachgestellt: `[('nord', None)]`). Mein
   Gegenvorschlag 3 in 87 sagte: „`ast.AnnAssign` mit Wert“.

**Kosten.** Zu 1: Die Begründung, mit der ein Anliegen schließt, fehlt in git. Damit hält
die Regel in `regeln.md` nicht, was sie sagt („sonst bewahrt git die Begründung nicht“).
Das trifft jede Nachprüfung, auch 86 und 87 jetzt. Zu 2: Ein Test zu einem Kriterium, das es
nicht gibt, bleibt grün, und die DoD (Kriterium ↔ Test) gilt als erfüllt. Zu 3: Rot ohne
Fehler. Der Implementierer müsste ein Anliegen an den Anforderungsautor schreiben, für einen
Namen, der kein Enum-Wert ist.

**Gegenvorschlag.**
1. Gelöscht wird nur, was in HEAD steht und seit HEAD unverändert ist (`git diff --quiet HEAD
   -- <pfad>`). So landet die Fassung mit `erledigt` erst in einem Commit, und der nächste
   Lauf löscht sie. Scheiter-Test: „angenommen“ committet, im Arbeitsbaum `erledigt`, Datei
   bleibt; nach dem Commit wird sie gelöscht.
2. Jede vorhandene Einzeldatei `<pfad>/<kürzel><n>Test.py` wird gegen ihre Anforderung
   geprüft, auch wenn die Sammeldatei gilt. Liegen beide für dieselbe Anforderung vor, ist
   das rot. Scheiter-Test: der Fall oben ist rot.
3. In `enumWerte` `ast.AnnAssign` nur mit `anweisung.value is not None`. Scheiter-Test:
   `nord: int` ohne Wert ist grün.

**Stellungnahme.** Umgesetzt: 1 `erledigteLöschen` löscht nur Unverändertes (Scheiter-Test `testErledigtSeitDemLetztenCommitBleibtBisZumCommitLiegen`); 2 jede Einzeldatei wird geprüft, beide Dateien sind rot (`testEinzeldateiNebenGültigerSammeldateiWirdGeprüftUndIstRot`); 3 `nord: int` ist kein Enum-Wert (`testAnnotationOhneWertIstKeinEnumWert`).
