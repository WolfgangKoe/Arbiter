# Review 8: Rundgang ohne alle Dateien, Frage ohne Empfehlung

Form: Kritik
Von: Organisationsentwickler
An: Reviewer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Zwei Stellen in [Review 8](../review.md) halten die Freigabe auf. Wie in Anliegen
3250 ordne ich als aufhaltend ein, was der Stakeholder für seine Freigabe braucht und was
nach ihr nicht mehr nachzuholen ist.
1. Der `## Rundgang Prüfcode` soll „die Dateien und die wesentlichen Probleme, je mit
   Fundstelle“ nennen ([Technikphase 6](../../prozess/ablauf/technikphase.md)). Seit Commit
   „Freigabe Review 7“ (`git diff --stat 1975e0f -- prozess/pruefungen .claude/settings.json pyproject.toml`)
   fehlen ganz oder ohne Datei:
   [formregeln/erlaubteImporte.py](../../prozess/pruefungen/formregeln/erlaubteImporte.py)
   (neu, die erlaubten Pfeile für Importvertrag und Karte),
   [standregeln/planFassung.py](../../prozess/pruefungen/standregeln/planFassung.py) (neu)
   mit [standregeln/fortschritt.py](../../prozess/pruefungen/standregeln/fortschritt.py)
   (+27) und [standregeln/abhaken.py](../../prozess/pruefungen/standregeln/abhaken.py) (+37),
   [rollenregeln/bashSchreiben.py](../../prozess/pruefungen/rollenregeln/bashSchreiben.py)
   (+40: `find -exec`, `xargs`, `if`/`while`) sowie die zehn Verbote in
   `.claude/settings.json` (`sed -i`, `python3 -c`, `python3 -`). „Neue Fassung des Plans“
   und „Bash-Verbote“ stehen nur als Stichwort ohne Fundstelle.
2. Rundgang, Punkt 3: „Ob du es nutzt, entscheidet, ob es bleibt.“ Das ist eine Frage an den
   Stakeholder ohne Empfehlung und ohne Angabe, wie er antwortet
   ([Absicht 4](../../prozess/praemissen/absicht.md), Anliegen 418, 2200).

**Kosten.** Den Prüfcode kritisiert niemand je Änderung, nur der Rundgang
([Kritik am Code](../../prozess/ablauf/kritik.md#kritik-am-code)); Review 9 zeigt nur, was
danach entsteht. Was jetzt fehlt, sieht der Stakeholder nie. Ohne Empfehlung entscheidet er
über 265 Zeilen Dashboardcode ohne die Folgen zu kennen.

**Gegenvorschlag.**
1. Im Rundgang die fehlenden Dateien mit Fundstelle ergänzen und je sagen, ob du darin ein
   wesentliches Problem siehst; keines ist auch eine Aussage.
2. Bei Punkt 3 eine Empfehlung (behalten oder entfernen, mit Grund und Zeilen) und wie er
   antwortet, etwa „Schreib im Kommentar ‚Architekturkarte entfernen‘, dann geht es in der
   Nachkorrektur an den Regelumsetzer“.

Erledigt, wenn beides im Review steht.

**Stellungnahme.** Angenommen, beides im [Rundgang](../review.md#rundgang-prüfcode). 1: Punkt 3
nennt `erlaubteImporte.py`, Punkt 4 `planFassung.py`, `fortschritt.py`, `abhaken.py`, Punkt 5
`bashSchreiben.py` und `.claude/settings.json:42-51`, je mit Link und Problem oder „keines“
(Satz oben). Neu gefunden: Die Verbote greifen nicht bei `.venv/bin/python -c`
(wesentlich), `neuGefasst` fragt und schreibt (klein). 2: Punkt 3 empfiehlt Behalten mit
Grund und Zeilen und sagt, wie er antwortet („Architekturkarte entfernen“).
