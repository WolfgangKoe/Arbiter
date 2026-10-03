# Kritik eines Entwicklers am Altbestand

31 · Anliegen · von Stakeholder → Organisationsentwickler · Runde 1/3 · angenommen

Bearbeitung in der Retro von Zyklus 1.

## Runde 1
**Befund.** Der Stakeholder hat die [Kritik eines Entwicklers](../kritik-entwickler.md) am
Altbestand abgelegt. Abgleich mit der Organisation:
- Geregelt: sprechende Namen ([Prämisse](../../prozess/praemissen/wir.md)), fachliche
  Akzeptanztests vor dem Code (`prozess/ablauf.md`), Glossar, kleine Root-CLAUDE.md mit
  Wissen in Rollen und Skills (Höchstmaße).
- Nur Text: Komplexität, Verschachtelung, Methodenlänge als Prüfung mit Schwelle
  (complexipy 15, ruff PLR in `VORGEHEN.md` E37); DoD 2 nennt sie ohne Mechanismus.
- Offen: `if`/`else` gegen Polymorphie nach Verständlichkeit statt als Regel; Domänenmodell
  vor dem Code über das Glossar hinaus (Beziehungen, Verantwortlichkeiten); Messung je
  Variante von Kontext und Codestil: Token, Erfolgsquote, Korrekturschleifen, Zeit bis zur
  akzeptierten Lösung.

**Kosten.** Ohne Schwelle wächst Komplexität unbemerkt wie im Altbestand; ohne Kennzahl
bleibt offen, ob Prämisse und Skills Korrekturschleifen sparen.

**Gegenvorschlag.** Für die Retro:
1. Prozess-Item an den Regelumsetzer: Komplexität und Verschachtelung mit Schwelle, die
   Sperre mindestens so streng wie SonarLint; der Architekt kritisiert.
2. Kennzahlen mit Bedeutung, Schwelle und Reaktion: Runden je Anliegen und Kritikläufe mit
   Befund je Codeänderung (aus git), Belegung je Rollenlauf ([22](22-dashboard-und-budget-am-kontextfenster.md)).
3. Leitplanke „Abstraktion nach Verständlichkeit“ als Prämisse, beobachtet statt geprüft.
4. Domänenmodell: Anliegen an den Anforderungsautor, sobald ein Befund es zeigt.

**Stellungnahme.** In der [Retro](../retro.md): 1 als P7, 2 als P8, 3 als Punkt 9 der
[Prämisse](../../prozess/praemissen/wir.md) (Anliegen 65, F3), 4 über Anliegen 71 an den
Anforderungsautor: Beziehungen stehen in der Definition im Glossar, wer festlegt oder ändert
im Kriterium ([`domaene/CLAUDE.md`](../../domaene/CLAUDE.md), Punkt `glossar.md`); der
prüfbare Teil als P9 (Anliegen 70).

Mit `Freigabe Retro 1` hast du nachgeprüft. `erledigt` trägst du selbst ein: `statusrecht.py`
lässt es nur dem Absender.
