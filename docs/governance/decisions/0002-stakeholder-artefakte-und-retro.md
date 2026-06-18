# 0002 — Stakeholder-Artefakte sind für den Leser; Retro ist fester Teil von Event 5

**Datum:** 2026-06-18
**Status:** angenommen

## Kontext

In S57 zeigte sich zweimal dasselbe Muster: Der Leitstand-Eintrag zum Token-Report war erst nur ein Link (kein Einblick an der „Tür"), und der Report selbst arbeitete mit rohen Session-UUIDs und unbeschrifteten Summen. Beide Male wurde für den **Mechanismus** gebaut (was technisch korrekt zusammenzufassen ist), nicht für den **Stakeholder als Leser**. Der Report beantwortet die naheliegenden Fragen des Stakeholders nicht (Welche Session ist die jüngste? Was bedeutet die Summe? Wie viele Subagenten, für welche Aufgabe?).

Gleichzeitig kam der **Retro-Anteil** des Session-Ende-Events (Event 5) zu kurz — er wurde mehr beiläufig im Agenten-Arbeitsfluss erledigt als bewusst **mit dem Stakeholder**.

Zwei Spannungen also: (1) Wofür/für wen sind Artefakte da? (2) Ist der Retro ein fester Schritt oder optional?

## Entscheidung

1. **Stakeholder-gerichtete Artefakte sind für den Leser.** Alles, was dem Stakeholder vorgelegt wird — Leitstand, Reports, Gate-Ausgaben (Debt-Scoreboard, Rule-Catalog-Prozente etc.) — muss **für ihn verständlich** sein und **seine** Fragen beantworten. Tabellen sind die Grundlage; Diagramme sind, wo sinnvoll, besser. Rein agenten-interne Kommunikation (Subagent-Routing, Zwischenstände) muss diesen Anspruch **nicht** erfüllen.
2. **Der Retro ist fester, nicht überspringbarer Teil von Event 5.** Wenn der Stakeholder involviert ist, muss der Retro für ihn nachvollziehbar sein: Was lief gut, wo war Reibung, welche Wurzel, was sollte sich ändern.
3. **Bedarf erfragen statt raten.** Bevor ein stakeholder-gerichtetes Artefakt gebaut oder umgebaut wird, fragt der Orchestrator den Stakeholder nach seinem konkreten Bedarf (welche Fragen soll es beantworten?) — statt ihn aus dem Mechanismus abzuleiten. Optionen werden nicht fälschlich als Entweder-oder präsentiert, wenn sie kombinierbar sind.
4. **Session-Ende: beendete Session gegen die nächste Aufgabe.** Im Retro vergleicht der Orchestrator die beendete Session — auch ihre Effizienz (Peak-Kontext vs. 150k-Korridor, Modell-Mix, Subagent-Anteil) — mit der erwarteten nächsten Aufgabe und hält, wenn ein Learning folgt, dieses in `next_session.md` fest. Proaktiv, ungefragt; je früher der Orchestrator es selbst bemerkt, desto besser.

## Konsequenzen

- **Einfacher / sicherer:** Klares Kriterium für Report-/Gate-Design (beantwortet es die Fragen des Lesers?). Der Retro liefert verlässlich Verbesserungs-Input statt unterzugehen.
- **Schwieriger / teurer:** Mehr Aufwand bei Report-/Gate-Ausgaben (Aufbereitung, Diagramme, lesbare Labels). Bestehende Gates sind nachzuziehen → Backlog.
- **Folgefragen:** Token-Report v2 (lesbare Labels, jüngste oben, Σ-Beschriftung, Subagenten-Anzahl + Aufgabe, Diagramm) und ein leser-orientierter Review der übrigen Gates. Beide im Backlog.

## Review-Termin

Nächste Retrospektive — Frage: Beantworten die überarbeiteten Artefakte die Stakeholder-Fragen messbar besser, und hat der feste Retro-Schritt Mehrwert gebracht?
