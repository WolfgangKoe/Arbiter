# Ideen-Eingang & Refinement

Dieser Ordner ist der aufbereitete Ideen-Eingang. Er bildet die zweite Station des Refinement-Flusses.

---

## Fluss: von der Skizze zum Backlog-Eintrag

```
Fotos/                  docs/inbox/              docs/goals/backlog.md
(roher Einwurf)  →  (strukturierter Text)  →  (priorisierter Backlog-Eintrag)
```

**Schritt 1 — Einwurf (Stakeholder):**
Rohe Gedanken, Skizzen, Fotos von handgeschriebenen Notizen landen in [Fotos/](../../Fotos/). Kein Format, kein Aufwand — einfach ablegen.

**Schritt 2 — Aufbereitung (Subagent, geplant Phase C):**
Ein Sonnet-Subagent liest neue Bilder aus Fotos/, extrahiert die Idee als strukturierten Text und legt eine Datei hier in docs/inbox/ an. Die Automatisierung ist **geplant (Phase C)** — aktuell wird manuell aufbereitet.

**Schritt 3 — Refinement-Event (Stakeholder + Orchestrator):**
Im Refinement-Event bespricht der Orchestrator die Idee mit dem Stakeholder, bis gemeinsames Verständnis besteht: Was genau ist gemeint? Welchen Umfang hat es? Welche Abhängigkeiten? Offene Fragen werden direkt im Inbox-Dokument beantwortet.

**Schritt 4 — Entscheidung:**
- **Akzeptiert:** Idee wandert als Backlog-Eintrag nach [docs/goals/backlog.md](../goals/backlog.md). Status hier auf `akzeptiert (→ Backlog)` setzen.
- **Verworfen:** Status auf `verworfen` + kurze Begründung. Das Dokument bleibt als Entscheidungsspur.

---

## Status-Konvention

Jede Idee in diesem Ordner trägt einen Status im YAML-Frontmatter oder als ersten Abschnitt:

| Status | Bedeutung |
|---|---|
| `neu` | Aufbereitet, noch nicht besprochen |
| `in-refinement` | Wird gerade mit dem Stakeholder geklärt |
| `akzeptiert (→ Backlog)` | Idee angenommen; Backlog-Eintrag angelegt |
| `verworfen` | Bewusst nicht weiterverfolgt (Begründung im Dokument) |

---

## Dateiformat (Empfehlung)

```markdown
---
status: neu
eingang: YYYY-MM-DD
quelle: Fotos/IMG_XXXX.jpeg
---

# Idee: Kurztitel

## Rohe Idee (aus Bild extrahiert)

Was steht/zu sehen ist auf dem Bild/der Skizze.

## Strukturierte Fassung

Präzisierte Beschreibung: Was soll gebaut werden? Warum?

## Offene Fragen

- [ ] Frage 1
- [ ] Frage 2

## Refinement-Notizen

Ergebnisse aus dem Gespräch mit dem Stakeholder.
```

---

*Dieser Ordner ist bewusst schlank gehalten — er ist Durchgangsstation, kein Archiv.*
