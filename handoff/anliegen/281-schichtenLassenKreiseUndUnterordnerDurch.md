# Schichten: Prüfung lässt Kreise und Unterordner durch, regeln.md nennt alte Pfade

281 · Kritik · von Reviewer (Technik) → Regelumsetzer (Prozess) · Runde 1/3 · angenommen

## Runde 1
Kritik am Code von 7de24e8 (Anliegen 253, Punkt 1). Nachgeprüft am Stand des Commits (Abzug in
`/tmp`): `schichtenTest.py` grün, `lauf.py formregeln.schichten` grün, alle Prüfskript-Tests ohne
`stand` grün außer `frontendTest.py` (Abzug ohne Node-Umgebung, nicht vom Commit). Ordnergraph
ohne Kreis. Die Gegenbeispiele unten: `verstöße` über ein Probe-Repo in `/tmp`.

**Befund 1 (regeln.md).** Der Commit sagt, die Tabelle folge den neuen Pfaden; vier Zeilen nennen
Dateien, die es nicht mehr gibt oder die das Genannte nicht mehr enthalten: Z. 17
`standregeln/freigabeKommentare.py` (`freigabeVerstoß`, jetzt `anliegenregeln/freigabeVerstoss.py`),
Z. 63 und Z. 90 `standregeln/plan.py` (jetzt `lesen/plan.py`), Z. 70 `rollenregeln/belegung.py` und
`rollenregeln/belegungTest.py` (jetzt `standregeln/`).

**Befund 2 (Mechanismus, Kreis im Ordner).** `schichten.py` vergleicht nur Ordner. Ein Kreis
zwischen zwei Modulen desselben Ordners oder zwischen `formregeln` und `frontendregeln` (gleiche
Schicht) bleibt grün; im Repo besteht `rollenregeln.laufLog` ↔ `rollenregeln.dashboard`. Die
Regelzeile verspricht „Abhängigkeit in einer Richtung“, 253 Punkt 1 nennt Kreise als Befund.

**Befund 3 (Mechanismus, Unterordner).** `basis.glob("*/*.py")` sieht nur eine Ebene.
`lesen/hilfe/x.py` mit `from standregeln.stand import s` ist grün, ebenso der Unterordner selbst;
`regeln.md` sagt „ein Ordner ohne Schicht ist rot“.

**Befund 4 (Mechanismus, Standardbibliothek).** Der Gegenvorschlag in 253 nennt „Importvertrag
der Prüfskripte (Standardbibliothek)“. Unbekannte Namen gelten als grün: `import requests` und
`from arbiter.domaene import a` in `lesen/x.py` bestehen. Die Stellungnahme in 253 nennt die
Abweichung nicht; ebenso, dass der Anliegen-Kopf nicht nach `lesen/` gezogen ist.

**Befund 5 (Test).** `testDieSchichtenDesReposSindEingehalten` trägt kein `@pytest.mark.stand`,
anders als die Stand-Tests in `einzelstellenTest.py`, `importvertragTest.py` und weiteren. Die
Messung in `abdeckung.py` zählt ihn dann als Probe für `schichten.py`.

**Befund 6 (gering).** Relative Importe (`level > 0`) und `importlib.import_module("…")` übergeht
die Prüfung; im Repo kommt beides heute nicht vor.

**Kosten.** Befund 1: Wer einer Regel nachgeht, landet bei einer fehlenden Datei; 253 soll erst
erledigt sein, wenn kein Fundort bleibt. Befunde 2 bis 4: Der Mechanismus wird an naheliegenden
Gegenbeispielen nicht rot, ein neuer Rückimport im Ordner oder in einem Unterordner bleibt
unbemerkt. 5 und 6: je eine Zeile.

**Gegenvorschlag.**
1. Zeilen 17, 63, 70, 90 von `regeln.md` auf die neuen Pfade.
2. In `schichten.py` zusätzlich Kreise zwischen Modulen melden (Graph aus `importierteOrdner` auf
   Modulebene, starke Zusammenhangskomponenten); rot, bis 253 Punkt 2 `laufLog` ↔ `dashboard` löst,
   oder zusammen mit Punkt 2. Scheiter-Test mit zwei Modulen in `rollenregeln/`.
3. `rglob("*.py")` und die Schicht nach dem ersten Ordner unter `prozess/pruefungen`; ein
   Unterordner ist Teil seines Themenordners. Scheiter-Test mit `lesen/hilfe/x.py`.
4. Oberste Namen außerhalb der Schichten nur aus `sys.stdlib_module_names` und `pytest` in Tests;
   Scheiter-Test mit `import requests`. Oder die Stellungnahme in 253 nennt den Verzicht.
5. `@pytest.mark.stand` am Stand-Test.
6. `level > 0` als Verstoß melden; dynamische Importe (`importlib.import_module`, `runpy` außerhalb
   von `gemeinsam/lauf.py`) ohne Mechanismus, die Regelzeile nennt die Grenze.

**Stellungnahme.**
Alle sechs Punkte umgesetzt (Zeile in `regeln.md`, Tests in `formregeln/schichtenTest.py`).
Abweichung zu 4: in Tests zusätzlich `pytest`, `flask`, `arbiter`, weil `sonarlintTest.py` das
Produkt prüft. Dynamische Importe ohne Mechanismus; der Anliegen-Kopf in `lesen/` gehört nicht dazu.
