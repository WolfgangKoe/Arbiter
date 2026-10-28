# Prozessphase

Auslöser: `Freigabe Review <n>`. Prozessregeln (`prozess/` außer dem Backlog), Prämissen und
Rollen (`.claude/`, CLAUDE.md) ändern sich nur in dieser Phase und erst nach `Freigabe Retro
<n>`; davor beschreibt die Retro die Änderung. Ausnahme: Seine Zeilen in `prozess/regeln/`
trägt der Regelumsetzer in jeder Phase ein (Anliegen 731, 1900). Mechanismus: `rollenregeln/regelnNurInProzessphase.py`
in `rollenregeln/schreibgrenze.py` (Write und Edit, samt Ausnahme; [Standregeln](../regeln/standregeln.md)).
1. Organisationsentwickler: `handoff/retro.md` (`# Retro · Zyklus <n>`, darunter der Absatz
   „Dashboard öffnen“ aus dem vorigen Retro unverändert, Anliegen 405) aus Anliegen an den
   Prozess, Kennzahlen (`prozess/kennzahlen.md`) und Auslösezählern (nur Text). Sie beginnt
   mit dem Fortschritt des Produkts: Etappe, belegte Kriterien, was am Bildschirm neu geht.
   Höchstens zwei Prozess-Items aus Befunden, die das Produkt aufgehalten haben, dazu die
   Aufträge des Stakeholders (Anliegen 630, 730, 1671); jedes in Worten beschrieben: was
   danach anders geschieht. Die Lücken des vollen Mutationslaufs ([DoD](dod.md)) schreibt
   der Reviewer als Anliegen: ein fehlendes Kriterium in die Domänenphase, sonst in die Technikphase
   (Anliegen 1671, F2). Dazu: Neuerungen von Claude Code, die einen eigenen
   Mechanismus ersetzen; wiederholte Entscheidungen des Stakeholders als Vorschlag für eine
   Prämisse; eine wiederholt verletzte Prämisse ohne Mechanismus als Prozess-Item. Ist eine
   Etappe erreicht, legt er `doku/` an oder pflegt es: für Menschen, keine CLAUDE.md verweist
   darauf; grafisch und kurz, nur Seltenes (Perspektiven, Rollen, Ordner), Rollentabelle und
   Ordnerbaum per Skript. Mechanismus: nur Text.
   Prozess-Items stehen im Abschnitt `## Prozess-Items` als `- P<k> <Titel> (<Rolle>): …`,
   die Rolle setzt es um; dort nur, was auf
   den nächsten Zyklus wirkt oder der Stakeholder vorher will, die übrigen im
   [Backlog](../backlog.md) bis zur nächsten Prozessphase. Mechanismus: nur Text.
2. Kritik an der Retro ([Kritik](kritik.md)).
3. Nachkorrektur: Kommentare in der Retro und Antworten in den Anliegen, auf die sie verweist,
   arbeitet der Organisationsentwickler ein, bis Befunde, Prozess-Items und Empfehlung zu
   ihnen passen; auch nach der Freigabe ([Freigabe und Kommentare](freigabe.md)).
4. Freigabe ([Freigabe und Kommentare](freigabe.md)) → Koordinator committet
   `Freigabe Retro <n>`.
5. Die Rolle des Prozess-Items setzt es um: Organisationsentwickler Regeln, Prämissen und
   Rollen, Regelumsetzer Mechanismen je mit Scheiter-Test; ein Item je Lauf, damit die
   Belegung unter 120.000 Token bleibt. Den Lauf, der ein Item abschließt, committet der Koordinator mit dem Betreff `P<k>: …`, einen Zwischenstand mit
   `P<k> Zwischenstand: …`; Items, die sich Dateien teilen, liefert ein Commit
   `P<j>, P<k> und P<l>: …` (Anliegen 740). Hat jedes Item der Retro seinen Commit `P<k>:` seit
   `Freigabe Retro <n>` (auch als `Retro <n> P<k>: …`), folgt die
   [Domänenphase](domaenenphase.md) mit Plan n+1.
   Mechanismus: `standregeln/phasenfolge.py` (`hatItemCommit`), sonst nur Text.
6. Der Zyklus endet nach Schritt 5; dann pusht der
   [Koordinator](../../.claude/agents/koordinator.md) nach `dev`. Mechanismus: nur Text.

Nach jeder Freigabe empfiehlt der Koordinator einen neuen Chat mit Startprompt
([Koordinator](../../.claude/agents/koordinator.md)); den Stand bringt der Hook mit.
Mechanismus: nur Text.
