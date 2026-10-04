# wir.md und DoD hinken den Prüfungen aus 2c5d09a nach

134 · Kritik · von Reviewer (Technik) → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
Gegenstand: 2c5d09a (Kritik am Code, Flughöhe: Regel im Mechanismus statt in der Prämisse).

**Befund.**
1. `benennung.py` (`koordinatenfelder`) lässt `x` und `y` als Felder von `Stelle` zu
   (Anliegen 128, erledigt und gelöscht, in git). wir.md 5 kennt keine Ausnahme, und wir.md
   sagt: „Ausnahmen nur über ihn“. Eine Entscheidung des Stakeholders fehlt; 128 selbst nannte
   die Alternative („Wäre der Stakeholder dagegen …“). Seit der Löschung verfolgt niemand
   die Frage.
2. wir.md 8 sagt „Mechanismus: nur Text“, `ablauf.md` DoD 2 „Nur Text: … Kommentare nach
   `prozess/praemissen/wir.md`“. Seit 2c5d09a prüft `kommentare.py` das im Lauf von
   `python3 -m pytest prozess/pruefungen`.
3. Typaliase in PascalCase prüft `benennung.py`; den Vermerk in wir.md 1 hast du in
   [114](114-pruefskripteOrdnenUndLesbarMachen.md) (C) zugesagt. Nur zur Vollständigkeit.

**Kosten.** Zu 1: Der Mechanismus setzt eine Ausnahme durch, die der Stakeholder nie
entschieden hat; wer wir.md liest, hält `x` für einen Verstoß. Zu 2: Die DoD führt eine
geprüfte Regel als Urteil; Kritiker prüfen von Hand, was schon automatisch rot wird.

**Gegenvorschlag.**
1. Frage an den Stakeholder in der nächsten Freigabevorlage: „`x` und `y` als Felder von
   `Stelle` zulassen (Architektur S1)?“, Empfehlung ja; dann wir.md 5 mit der Ausnahme und
   `koordinatenfelder` als Mechanismus. Lehnt er ab, geht es an Testautor und Architekt (128).
2. wir.md 8 und DoD 2 nennen `kommentare.py`; „Nur Text“ bleibt für toten Code.

Erledigt, wenn wir.md 5 und 8 und DoD 2 den Mechanismen entsprechen und die Ausnahme in 1
vom Stakeholder entschieden ist.

**Stellungnahme.** 2 und 3 umgesetzt: wir.md 1 nennt Typaliase, wir.md 8 und DoD 2 nennen
`kommentare.py`; nur Text bleiben toter Code und der Prozessverweis, den `kommentare.py` nicht
prüft. Zu 1: Frage an den Stakeholder in [135](135-koordinatenXundYAlsAusnahme.md); wir.md 5
folgt seiner Antwort. Wartet auf 135.
Nachtrag: 135 mit A beantwortet; wir.md 5 nennt die Ausnahme, Mechanismus `benennung.py`
(`koordinatenfelder`).
