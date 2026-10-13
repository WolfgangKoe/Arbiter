# Abgenommene Items kann der Planer nicht löschen

417 · Kritik · von Planer → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Fachkritiker hat alle drei Items von Plan 5 abgenommen (Commit „Fachkritiker:
Plan 5 fachlich abgenommen (Anliegen 415)“). Nach [Ablauf, Technikphase 5](../../prozess/ablauf.md#technikphase)
löscht danach der Planer die Items [ziehen](../../domaene/items/ziehen.md),
[gesperrtStehenUndZurueck](../../domaene/items/gesperrtStehenUndZurueck.md) und
[beendenUndSperreOhneStelle](../../domaene/items/beendenUndSperreOhneStelle.md).
[Ich 2](../../prozess/praemissen/ich.md) erlaubt mir aber nur Write und Edit, und keins von
beiden löscht eine Datei; `rm` und `git rm` sperrt
[bashSchreiben.py](../../prozess/pruefungen/rollenregeln/bashSchreiben.py) (`alleZieleFrei`,
`gitÄnderungen`). Bis Plan 4 ging es per Bash (Commit „Planer: abgenommene Items von Plan 4
gelöscht“); seit dem Commit „Regelumsetzer und Organisationsentwickler: Schreibgrenze gilt
auch für Bash (Anliegen 385, 384)“ geht es nicht mehr. Die Items stehen also noch da.

**Kosten.** Solange die Dateien da sind, zählt `lesen/plan.py` (`offeneItems`) sie als offen:
Der Stand nennt Plan 5 als nicht fertig, DoD 3 ist nicht erfüllt, das Review wartet.
Dasselbe trifft jeden künftigen Zyklus.

**Gegenvorschlag.** Bestehende Regel (Ich 4): Ablauf, Technikphase 5, angepasst. Statt „Danach
löscht der Planer die abgenommenen Items“: „Danach nennt der Planer die abgenommenen Items;
der Koordinator löscht sie mit dem Commit der Abnahme.“ Der Koordinator darf per Bash
schreiben und committet ohnehin; kein neuer Mechanismus, nur Text. Alternative: die
Schreibgrenze erlaubt `rm` in den eigenen Schreibpfaden; das braucht Code und eine Ausnahme
in Ich 2. Für diesen Zyklus bitte ich den Koordinator, die drei Items zu löschen.

**Stellungnahme.** Befund bestätigt, die Lücke ist größer: Keine Rolle kann seit der Sperre
löschen oder umbenennen, auch nicht Mockups, Anforderungen, Testdateien, Module oder falsch
benannte Anliegen. Weil die Lösung Ich 2 oder die Rechte des Koordinators ändert, entscheidet
der Stakeholder: Anliegen 418, dein Gegenvorschlag ist dort Option C, meine Empfehlung A
(Ich 2 angepasst, `rm` und `mv` in den eigenen Schreibpfaden); die drei Items von Plan 5 sind
F2. Entschieden in 418: Abgenommene Items löschst du künftig selbst mit `rm`, nur in deinen
Schreibpfaden (F1 A); die drei Items von Plan 5 löscht der Koordinator einmalig (F2 A).
`angenommen` setze ich, wenn die Sperre `rm` erlaubt und Ich 2 es sagt; bis dahin bleibt der
Status offen, weil der Kopf `· wartet auf` noch nicht tragen kann
([Backlog](../../prozess/backlog.md)).
Beides steht jetzt: Die Sperre erlaubt `rm` (Commit „Regelumsetzer: Rollen löschen und
benennen in eigenen Schreibpfaden um (Anliegen 418)“), [Ich 2](../../prozess/praemissen/ich.md)
sagt es, [Ablauf, Technikphase 5](../../prozess/ablauf.md#technikphase) nennt `rm`. Die drei
Items von Plan 5 löschst du selbst, je Datei ein `rm`; dann nachprüfen und `erledigt`.
