# Gegenbeispiel „nur Spieler 1“ für den Testautor

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Dein Kommentar zu P1 in der [Retro 8](../retro.md). In Technikphase 8 ließen
die Tests des Testautors oft nur Spieler 1 handeln oder nur Schlachtrunde 1 spielen, obwohl
das Kriterium für beide Spieler oder jede Runde gilt. Ein Fehler, der nur Spieler 2 trifft,
blieb so unbemerkt; 6 von 12 Rückläufen gingen darum an ihn.

Was ein Gegenbeispiel ist: Die Anleitung des Testautors (Skill
[`akzeptanztest-schreiben`](../../.claude/skills/akzeptanztest-schreiben/SKILL.md)) zeigt
einen guten Test und einen schlechten, „wie es nicht stehen soll“, mit dem Grund. Der
schlechte heißt Gegenbeispiel; heute zeigt er nur Formfehler (Namen, Indizes, lambda).

In [6431](6431-fragenDerRetro8.md), F2, standen zwei Wege: A Opus, B Sonnet mit dem
Gegenbeispiel. Meine Empfehlung war „A und das Gegenbeispiel“, beides zusammen. Du hast
„A“ geantwortet; ich las das als Opus ohne Gegenbeispiel. Das kann ein Missverständnis sein.

**Kosten.** Am Bildschirm: nichts. Code: nichts.

**Gegenvorschlag.** Beantworte F1; „.“ heißt, die Empfehlung gilt. Opus für den Testautor
ist schon umgesetzt, beide Antworten behalten es.

**F1 · Bekommt der Testautor zusätzlich das Gegenbeispiel?**
A: Nein, nur Opus (Anliegen 6431). Arbeit: Ob Opus allein die Fälle findet, zeigt Zyklus 9.
B: Ja, Opus und ein zweites Gegenbeispiel im Skill: ein Test, der nur Spieler 1 prüft, wo
das Kriterium beide Spieler nennt; darunter der Grund und dass beide Spieler als
`parametrize` gehören (Anliegen 6431, Empfehlung). Code: Tests prüfen beide Spieler und
jede Runde, auch wenn ein Lauf es übersieht. Arbeit: Der Skill wird rund 500 Zeichen
länger, die nur der Testautor liest; rund 1 % mehr Token je seiner Läufe.
Empfehlung: B. Der Fehler aus Technikphase 8 steht dann als Beispiel genau dort, wo der
Testautor nachschlägt; Opus allein sagt ihm nicht, worauf er achten soll. Sinken die
Rückläufe bis Retro 9 nicht, prüfe ich beides neu.
Antwort: B

**Stellungnahme.**
