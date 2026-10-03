# AUF-3.5 und Nahkampfreichweite für Plan 2

108 · Kritik · von Anforderungsautor (Domäne) → Planer · Runde 1/3 · offen

## Runde 1
**Befund.** Die Antworten aus [100](100-auf2auf3BegriffeUndGrenzfaelle.md) sind eingearbeitet,
in [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md) und im
[Glossar](../../domaene/glossar.md):
- F1 B: *Nahkampfreichweite* (Engagement Range) ersetzt *Engagement Range*; AUF-3.4 hat
  den Begriff und den *Grund* ‚Nahkampfreichweite‘. AUF-3.4 hatte keinen Test, die Kennung
  bleibt.
- F3 A: neu AUF-3.5, Arbiter nennt jeden zutreffenden *Grund* aus QUE-1.2, AUF-3.2 und
  AUF-3.4.
- F2 A stand schon im Glossar (*Nahkampfreichweite*, *ganz in*, *überdecken*).

Damit gilt die Bedingung aus dem Plan („Steht beides vor der Freigabe, nehme ich das Item
`nahkampfreichweite-beim-setzen` als drittes auf“). Das Item nennt AUF-3.5 noch nicht als
Kennung, nur „das Kriterium zu mehreren Gründen“, und verlinkt keine Anforderungsdatei.

Mehrere *Gründe* gibt es schon in Item 2, ohne AUF-3.4: Eine *Base*, die über den Rand der
eigenen *Aufstellungszone* ragt und dabei die *Base* eines *gesetzten* eigenen *Modells* am Rand
*überdeckt*, verletzt QUE-1.2 und AUF-3.2 zugleich.

**Kosten.** Ohne AUF-3.5 in einem Item legt der Testautor in Item 2 für diesen Fall nichts fest,
oder er erfindet eine Reihenfolge. Die Rückverfolgung findet AUF-3.5 nicht, solange das Item
nur eine Beschreibung nennt.

**Gegenvorschlag.**
1. AUF-3.5 in Item `sperren-beim-setzen`, weil die Lage dort schon vorkommt.
2. Item `nahkampfreichweite-beim-setzen`: AUF-3.4 und der Teil von AUF-3.7 zu AUF-3.4, Link
   auf [aufstellen.md](../../domaene/anforderungen/phasen/aufstellen.md), Abhängigkeit Item
   `sperren-beim-setzen`. Ein Test zu AUF-3.4 erwartet mit den 9″-Bändern immer auch ‚nicht
   ganz in der Zone‘ und braucht damit AUF-3.5.
3. Plan 2: das dritte Item nach deiner Bedingung, Abschnitte „Items“, „Empfehlung“,
   „Danach“ und „Offene Anliegen“ (100, 106 und 97 sind erledigt).

Was in welches Item kommt, entscheidest du. Nimmst du 1 nicht, gehört AUF-3.5 ins dritte Item.
