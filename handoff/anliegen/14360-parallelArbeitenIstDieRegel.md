# Parallel arbeiten ist die Regel, nicht die Ausnahme

Form: Kritik
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Halte für die Prozessphase fest, dass die Regel in Absicht zum parallelen Bearbeiten von Tasks scheinbar nicht ausreicht. Ja, es sollte unterbunden werden, wenn es wirklich zu Konflikten zwischen Subagenten kommt. Doch es kam zu oft vor, dass ich das triggern musste und siehe da - auf einmal können dennoch Arbeiten parallel ausgeführt werden. Parallel zu arbeiten sollte die regel und nicht die Ausnahme sein. Das muss konsequenter befolgt werden!“
„Die Reihenfolge kann ruhig so bleiben. Mir geht es ums Prinzip! Die Regel greift häufig nicht und nun, da ich mal wieder frage, scheint dafür wirklich ein Grund vorzuliegen.“

Beobachtungen des Koordinators aus diesem Lauf:
- Geprüft, was daneben laufen kann, hat er erst auf die Nachfrage des Stakeholders. Vorher arbeitete er nur die Schritte des Startprompts ab. Seine erste Antwort hielt 7151, 8041, 8641 und 8971 für frei; erst danach fand er die Reihenfolge im [Plan](../plan.md) (Aufräumen nach den Items, 8880 F2 A).
- Er committet nur, wenn keine Rolle läuft (11100). Jeder Commit hält alles andere an und bremst darum am stärksten.
- Der Gesamtlauf von `technik/tests` und `prozess/pruefungen` dauerte auf 53cc149 ohne Rolle daneben 16 Minuten 16 Sekunden. Die Annahme aus dem Startprompt, allein gut 3 Minuten, neben Rollen 17, trägt das Verbot „kein Lauf neben ihm“ also nicht. Ob er in dieser Sitzung wirklich allein lief, ist nur für die Rollen belegt.

Bestehende Regeln, die es berühren (Ich 4):
- [Absicht 2](../../prozess/praemissen/absicht.md): „Arbeitet parallel, wo nichts voneinander abhängt.“ Mechanismus: nur Text.
- [Gleichzeitige Läufe](../../prozess/ablauf/gleichzeitigeLaeufe.md) (Anliegen 279, 730) und [Koordinator](../../.claude/agents/koordinator.md): Was darf, startet er gleichzeitig. Nur Text, ohne Zeitpunkt der Prüfung.
- [Moderator](../../.claude/agents/moderator.md): nennt die Stränge, aber nur in der Moderation.
- [Commits](../../prozess/ablauf/commits.md) (Anliegen 2460, 11100): Commit nur, wenn keine Rolle läuft. Nur Text.
- [DoD, Belege](../../prozess/ablauf/dod.md) (Anliegen 8042, 8022): Abzug für Prüfungen neben Läufen. Das Verbot aus dem Startprompt steht in keiner Datei des Ablaufs.

**Kosten.** Der Stakeholder muss nachfragen und wartet länger auf das Inkrement. Geschätzt: A und C ein Lauf des Organisationsentwicklers, B dazu einer des Regelumsetzers.

**Gegenvorschlag.** Vorläufig, in der Prozessphase zu prüfen; die Reihenfolge von Plan 10 bleibt:
1. Die Prüfung, was daneben laufen kann, bekommt einen festen Zeitpunkt (F1).
2. Die Bremse durch den Commit und das Verbot „kein Lauf neben ihm“ auf ihren Grund prüfen: an einer Kopie in `/tmp` messen, ob ein Commit neben einer Rolle gelingt und wie lange der Gesamtlauf allein und neben Rollen dauert ([Ich 5](../../prozess/praemissen/ich.md)).

**Stellungnahme.**

Eingeplant als P4 der [Retro 10](../retro.md), mit B; Punkt 2: Commit im eigenen Arbeitsbaum.
Annahme: Bis zur Prozessphase ändert sich keine Regel.

**F1 · Wie wird paralleles Arbeiten zum Regelfall?**
A: Fester Schritt des Koordinators: Nach jedem Lauf prüft er alle offenen Items und Anliegen gegen die drei Bedingungen und startet, was frei ist; was liegen bleibt, begründet er mit der Bedingung. Nur Text (Anliegen 730)
B: Wie A, dazu nennt ihm der Hinweis nach jedem Rollenlauf, was nach `Wartet auf` frei ist. Die Reihenfolge im Plan und getrennte Dateien bleiben sein Urteil (neu; Grund: Absicht 2, die Regel als Text greift nicht)
C: Nur den Wortlaut der Regel schärfen, kein neuer Schritt (Absicht 2)
Empfehlung: B, denn die Regel steht schon zweimal als Text und griff trotzdem nicht; A allein bliebe wieder Text. Vorläufig und noch nicht an einer Kopie erprobt (Ich 5); Rückweg: Commit zurücknehmen.
Antwort: Wir nehmen B und zusätzlich machen wir die Aussagen aus Absicht 2 zu einem eigenen Punkt in dieser Prämisse
