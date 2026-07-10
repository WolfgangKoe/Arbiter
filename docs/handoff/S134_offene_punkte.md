STATUS: NEEDS-DECISION

# S134 — Offene Punkte zur Diskussion (Stakeholder)

Sammel-Datei für alles, was nach dem S134-Planning **nicht** entscheidungsreif ist.
Je Punkt: was zu entscheiden ist, Optionen, Empfehlung. Antworten gern direkt hier
hineineditieren (bewährter Rückkanal).

---

## B2 — Spielvorbereitungsscreen überarbeiten

**Zu entscheiden:** Zielbild des Screens, bevor ein Konzept-Handoff entsteht.

1. **Struktur:**
   - Option A — **Ein Screen, entrümpelt:** heutige Abschnitte behalten (Roster-Wahl,
     Roll-Off, Faction-Ability-Wahl, Armee-Durchsicht), nur Redundanzen raus (B5 erledigt
     das teilweise) und Reihenfolge glätten. Kleinster Eingriff.
   - Option B — **Geführte Schritte (Wizard):** Setup als Schrittfolge (1 Roster → 2
     Roll-Off → 3 Faction-Abilities → 4 Armee-Durchsicht → Start), pro Schritt nur das
     Nötige sichtbar. Größerer Umbau, aber deckt sich mit B9 (Subphasen-Sichtbarkeit)
     als durchgängiges Muster „Schritte explizit machen".
   - Option C — Option A jetzt, Option B als Ziel nach dem profileCard-Refinement (B4),
     weil die Armee-Durchsicht (Datenkarte) ohnehin neu entsteht.
   - **Empfehlung: C** — nicht zweimal umbauen; B5/B6/B8 räumen jetzt auf, das
     Wizard-Zielbild entsteht zusammen mit der Datenkarte.
2. **Scope-Frage:** Gehört die Faction-Ability-Wahl (B6, Entscheid „in die
   Spieler-Spalten") noch zum Setup-Screen-Konzept oder wird sie unabhängig davon schon
   in Welle 2/S135 umgesetzt? **Empfehlung:** unabhängig umsetzen (Entscheid steht),
   das B2-Konzept übernimmt sie dann als gegeben.

## B4 — profileCard / Datenkarte (eigenes Refinement)

**Sofortteil läuft separat** (++/OC raus, s. Plan v3 Welle 2). Fürs Refinement zu entscheiden:

1. **Anmutung:** Wahapedia-Datacard-Stil (Kopfleiste, Profilzeile, Waffen-Tabelle,
   Abilities-Block — Screenshot `…20-58-07.png` als Inspiration) vs. App-Design-System
   (GO-Karten-Ästhetik aus `design_system.md`, Chips/Badges). **Empfehlung:**
   App-Design-System mit Wahapedia-**Informationsarchitektur** (gleiche Blöcke, eigene
   Optik) — konsistent zur restlichen App, kein Fremdkörper.
2. **Waffen-Tabelle:** Welche Spalten? 9E-Standard wäre Range/Type/S/AP/D (+Abilities).
   Offen: Attackenzahl-Herleitung (Rapid Fire etc.) mit anzeigen oder erst im Spiel?
   **Empfehlung:** nur die 9E-Datasheet-Spalten, keine berechneten Werte im Setup.
3. **Inhalt:** ausschließlich Roster-Auswahl (bestätigt) — offen ist, ob Wargear-/
   Relic-Auswahl auf der Karte sichtbar markiert wird. **Empfehlung:** ja, als Chip.
4. **Wiederverwendung:** Datenkarte nur im Setup, oder ersetzt sie mittelfristig auch
   die In-Game-Profilanzeige (`_common.py:2194`-Kontext) und wird Armybuilder-Baustein?
   **Empfehlung:** als Baustein in `design_system.md` spezifizieren (ein Renderer,
   mehrere Orte) — genau dafür ist das Refinement da.
   Antwort: Aktuell möchte ich die Profilcard nur im Setup Screen anzeigen lassen. Innerhalb des Spiels brauche ich nur die darin befindlichen WErte, die es dann braucht. ALso so wie es jetzt schon ist. 

## B6 — Faction-Ability-Wahl in die Spieler-Spalten (Entscheid steht, Detail offen)

Nur eine echte Layout-Alternative gefunden:

- Option A — **Voll-UI in der Spalte:** komplette Protokoll-/Canticle-Wahl (alle Buttons)
  in der jeweiligen Spieler-Spalte; Spalten sind schmal → wird hoch.
- Option B — **Kompakt in der Spalte:** Spalte zeigt Status („Command Protocols: 3/5
  zugewiesen") + öffnet die vorhandene Wahl-UI in einem Expander in der Spalte.
- **Empfehlung: B** — erfüllt „auf die Player-Ebene setzen" ohne die schmalen Spalten zu
  sprengen; kein neuer Screen (Stakeholder: „brauchen keine vollständige Seite").
  Antwort: B ist fein. Ich möchte allerdings, dass die aktuelle Funktionalität erhalten bleibt!

## B7/B9 — „Was gibt es hier zu klären?" (konkrete Antwort)

Umsetzbar ohne Klärung ist B8 (läuft, Welle 2). Bei B7/B9 sind DREI Design-Entscheidungen
offen, die der Executor nicht selbst treffen darf:

1. **B7 — Welcher Kopfbereich fällt weg und was bleibt als Phasen-Anker?** Der rot
   markierte Bereich (`…21-29-43.png`) enthält Phasenname + erklärenden Text; irgendein
   Element muss die Phase weiter identifizieren.
   - Option A: Bereich komplett weg, Phase steht ohnehin in der Phasen-Navigation.
   - Option B: einzeiliger Mini-Header (nur Phasenname), Erklärtext weg.
   - **Empfehlung: A**, WENN B9-Stepper kommt (der Stepper wird der neue Anker); bis
     dahin B (sonst ist die Phase im Content-Bereich unbenannt).
2. **B7 — Hinweis-Konvention:** Wie werden schwache Hinweise („Select unit", „No PSYKER
   unit available") gestärkt?
   - Option A: `st.info`/`st.warning`-Boxen (auffällig, aber laut — konterkariert das
     Entrümpeln).
   - Option B: eigener Hinweis-Baustein im Design-System (dezente Farbfläche +
     Symbol-Konstante aus `symbols.py`, eine Größe über Caption).
   - **Empfehlung: B** — als §-Erweiterung in `design_system.md`, dann überall gleich.
3. **B9 — Darstellung + Verhalten des Subphasen-Steppers:**
   - Option A: horizontale Stepper-Chips oben in der Phase („① Feldbewegungen →
     ② Reinforcements"), aktueller Schritt hervorgehoben, **manuell** weitergeschaltet.
   - Option B: vertikale Checkliste in der Seitenleiste/GameActionsArea, Schritte werden
     abgehakt (manuell oder automatisch, wenn die App den Zustand kennt — z. B. „alle
     Einheiten bewegt").
   - Option C: nur statischer Hinweistext je Phase (kein Zustand) — billigste Variante,
     macht die Schritte sichtbar, erzwingt aber nichts.
   - **Empfehlung: A mit Auto-Vorschlag, wo der Zustand bekannt ist** (Movement kennt
     „alle bewegt", Reinforcements-Schritt existiert seit S133 als eigener Zustand);
     C als Zwischenlösung, falls A das S135-Budget sprengt. Wichtig: Stepper ist
     Anzeige/Erinnerung, KEIN Zwang — App bleibt Begleiter (Grundannahme).

     Antwort: Lass uns mit C als Zwischenlösung anfangen. Dann Entscheidung wieder vorlegen, wenn ich das sehe. Eine vertikale Darstellung der Subphasenfolge fände ich besser.

4. **Schnitt:** B7+B9 als EIN Konzept-Handoff (ein Layout-Zusammenhang: was weg ist,
   ersetzt der Stepper) — B8 bleibt davon unabhängig. **Empfehlung:** ja, ein Handoff
   mit Grundannahmen-Block, Umsetzung S135+.

## B10 — Formulierungsvorschläge CLAUDE.md (freigabepflichtig, hier NUR Text)

**Vorschlag 1 — Kommentar-Konvention** (neuer Bulletpoint im Abschnitt „Clean Code"):

> - **Kommentar-Konvention:** Code erklärt sich selbst (sprechende Namen, kleine
>   Funktionen); Regel- und Design-Erklärungen gehören in die zuständige Spec unter
>   `docs/spec/`, nicht in Kommentare. Erlaubt sind nur: (a) ein kurzer
>   Verweis-Kommentar auf die Spec (`# → docs/spec/<datei>.md §<n>`), (b) ein
>   *Warum*-Kommentar für nicht offensichtliche Entscheidungen (Gotchas,
>   Regel-Randfälle) mit Quellenangabe. Docstrings bleiben für die öffentliche API,
>   erzählen aber keine Spec nach. Abbau bestehender Erklär-Kommentare als Ratchet:
>   bei jeder Modul-Berührung in die Spec verschieben — kein Big-Bang-Durchgang.

**Vorschlag 2 — Artefakt-Landkarte** (neue Zeile in der Tabelle „Artefakt-Landkarte"):

> | **Stakeholder-Beobachtungen (stehender Eingang)** | `docs/handoff/Stakeholder_Beobachtungen.md` |

Beide Änderungen werden erst nach expliziter Freigabe in CLAUDE.md eingetragen.
