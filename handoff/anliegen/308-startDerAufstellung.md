# Start der Aufstellung: Vorbelegung oder Wahl von Gewinner und Zone

308 · Fragen · von Planer (Domäne) → Stakeholder · Runde 1/3 · angenommen

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Du fragst in [307](307-waehlenAmBildschirm.md), was stehen muss, bevor eine
Einheit wählbar ist. Nach Only War wählt der Gewinner des Roll-offs zuerst seine
Aufstellungszone, dann stellt der andere als Erster auf (`core_rules.txt:2322`). Arbiter lässt
nur eine Einheit des Spielers wählen, der an der Reihe ist, und an der Reihe ist jemand erst
nach diesen beiden Wahlen ([AUF-1.3, AUF-1.5](../../domaene/anforderungen/phasen/aufstellen.md)).
Die Domäne kann beide Wahlen schon, mit grünen Akzeptanztests; es fehlt nur der Bildschirm.
Heute zeigt Arbiter nach dem Start die Ausgangslage, handeln kann man nicht. Jede erste Wahl
am Bildschirm bringt dasselbe Neue mit: eine Handlung über HTTP und den Speicher, der sie
behält ([speicher.md](../../technik/architektur/speicher.md), Neuland laut
[Review 3](../review.md)).

**Kosten.** Ohne deine Wahl des Schnitts schreibe ich Plan 4 nicht, und der Anforderungsautor
weiß nicht, welche Fragen aus 307 er zuerst klären muss.

**Gegenvorschlag.** Drei Schnitte für Plan 4, jeder mit dem Speicher:
- V1, Vorbelegung (deine Idee): Arbiter beginnt mit gewähltem Gewinner und gewählter Zone.
  Plan 4 bringt die Wahl der Einheit per Klick in der Ablage (AUF-5) und dass Arbiter sie
  behält (QUE-3). Plan 5 bringt das Setzen durch Ziehen. Danach stellt ihr am Tisch eine
  Armee auf; nur Gewinner und Zone sind fest. Plan 6 bringt Gewinner und Zone an den
  Bildschirm und entfernt die Vorbelegung, zusammen mit „zurück“ und „gemeinsam übergehen“.
- V2, Reihenfolge der Regeln: Plan 4 bringt Gewinner und Zone an den Bildschirm. Am Ende
  sind die Zonen gefärbt und Spieler 2 ist an der Reihe, aber keine Einheit ist wählbar.
  Die Einheit folgt in Plan 5, das Ziehen in Plan 6. Keine Krücke, aber aufstellen könnt
  ihr einen Zyklus später.
- V3, alle drei Wahlen (Review 3): der größte Schnitt; mit dem Neuland Speicher reicht der
  Zyklus womöglich nicht.

Die Krücke kennzeichnen, ohne neue Regel ([ich.md](../../prozess/praemissen/ich.md) 4):
Die Vorbelegung wird ein eigenes Kriterium mit eigenem Akzeptanztest, geschrieben vom
Anforderungsautor. Das Item, das Gewinner und Zone an den Bildschirm bringt, löscht das
Kriterium; ein Test ohne Kriterium ist rot (`kriterienregeln/rueckverfolgung.py`), also geht
der Test mit. Die Kennung kommt nie wieder (`domaene/CLAUDE.md`). Solange die Vorbelegung
steht, ist [Etappe 1](../../domaene/etappen/01-aufstellen.md) nicht erreicht, denn dort
wählen die Spieler beide; jeder Plan nennt den Ersatz unter „Danach“. Wie der Test sich als
vorläufig zu erkennen gibt (Name, Markierung), entscheidet die Technik.

Aus 307 braucht Plan 4 bei V1 nur F3 (wo die Sperre einer Wahl steht), F4 (Neustart) und F5
(Begriff, wenn F3 A); F1 und F2 dort kommen erst mit Plan 6. Bei V2 und V3 braucht er alle.

**F1 · Schnitt für Plan 4.** A: V1. B: V2. C: V3.

Empfehlung A: Ihr könnt einen Zyklus früher am Tisch aufstellen, und die Fragen, bei denen du
nachgefragt hast, warten bis Plan 6. Das Neuland Speicher kommt mit der einfachsten Wahl,
einem Klick in der Ablage, die schon steht. Die Krücke kostet ein Kriterium und einen Test,
die Plan 6 wieder löscht.

Antwort: .

**F2 · Was ist vorbelegt?** Nur bei F1 A.
- A: Fest: Spieler 1 hat den Roll-off gewonnen und die linke Zone gewählt, die neben seiner
  Ablage; Spieler 2 ist zuerst an der Reihe.
- B: Der Startbefehl nimmt Gewinner und Zone entgegen.
- C: Du nennst eine andere feste Wahl.

Empfehlung A: Die kleinste Krücke, gleich für den Start und alle Tests. B kostet eine eigene
Eingabe, die Plan 6 wieder wegwirft.

Antwort: .

**Stellungnahme.** Ich habe diesen Vorschlag angenommen. Bitte in 307 notieren, was davon noch offen bleibt. Ansonsten beides auf "erledigt" setzen.
