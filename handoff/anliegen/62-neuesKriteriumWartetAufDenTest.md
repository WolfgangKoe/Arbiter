# Rückverfolgung: Ein neues Kriterium wartet auf den Test

62 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Neue Kriterien bekommen die nächste freie Nummer
([`domaene/CLAUDE.md`](../../domaene/CLAUDE.md), aus
[Anliegen 59](59-kennungInDomaeneClaude.md)). Gibt es zur Anforderung schon eine Testdatei,
meldet [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py) „hat keinen Test“,
und `python3 -m pytest prozess/pruefungen` ist rot. Der Anforderungsautor schreibt in der
Domänenphase; der Testautor folgt erst nach `Freigabe Plan <n>`. So ist die Prüfung eine
ganze Phase lang für jede Rolle rot.

**Kosten.** Jeder Lauf verlangt „Prüfungen grün“ und trifft auf einen fremden, erwarteten
Befund; echte Verstöße gehen darin unter, oder Rollen lernen, Rot zu übergehen.

**Gegenvorschlag.** Ein Kriterium ohne Test ist erst rot, wenn ein Item eines freigegebenen
Plans es umfasst: `handoff/plan.md` verlinkt das Item, das Item nennt die Anforderung
(`AUF-1`) oder das Kriterium (`AUF-1.8`), und `Freigabe Plan <n>` ist committet. Vorher
nennt der Stand es als wartend („AUF-1.8 wartet auf den Testautor“). Ein Test ohne Kriterium
bleibt immer rot. Den Weg zum Testautor nach der Freigabe nennt schon der Stand.
Scheiter-Tests:
1. Testdatei zu AUF-1 da, AUF-1.8 neu, kein Plan umfasst es → grün, der Stand nennt es.
2. Wie 1, Plan n umfasst AUF-1 und ist freigegeben → rot.
3. Test zu AUF-1.9 ohne Kriterium → rot.

Die Zeile „Kriterium ↔ Test“ in `prozess/regeln.md` nennt danach, was wartet.

**Stellungnahme.**
