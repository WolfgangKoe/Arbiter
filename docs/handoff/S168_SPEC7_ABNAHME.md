STATUS: NEEDS-DECISION

# S168 — Abnahme §7 `design_system.md` (Pflicht-Trigger-Kachel / Explodes, B-028c1)

Lebensdauer: bis Stakeholder-Entscheidung. Bei Abnahme: diese Datei löschen, Mockup-Dateien
(`docs/handoff/S166_MOCKUP_EXPLODES.md`, `docs/handoff/S166_MOCKUP_EXPLODES_V2.html`,
`docs/handoff/S167_MOCKUP_EXPLODES_V3.html`) löschen, B-028c1-Blocker in
`docs/goals/backlog_details.md`/`backlog.md` aufheben, Code-Umsetzung für S169 freigeben.
Bei Ablehnung/Korrektur: §7 wird entsprechend überarbeitet, diese Datei bleibt bis zur
nächsten Runde stehen.

## Zusammenfassung §7

`docs/spec/design_system.md` §7 (neu) überführt Mockup V3 in verbindliche Spec — **keine
neue Bauform**: Pflicht-Trigger-Kachel = GO-Karten-Bauform (§6.1) ohne `[Use]`/CP, Wurf über
eine abgewandelte Tisch-Wurf-Eingabe (§6.3, zwei Buttons statt Zahlenfeld), Ziel-Auswahl im
Heroic-Intervention-Toggle-Stil (Bestandscode), unitCard unverändert, Hinweiskasten über die
bestehende `info`-Konvention (§3). Anker bleibt inline am Eintrag der zerstörten Einheit
(§6.2), nie Vollbreite, nie in der zentralen Stratagems-Liste. `auto_explode` ist eine
gewöhnliche GO-Karte mit YAML-Titel.

## Auflage → Umsetzung in §7

| V3-Auflage (S167 §h-Antwort, wörtlich) | Wo in §7 |
|---|---|
| 1. EIN Hinweiskasten, UNTER der GO-Karte; Blau = Hinweis-Semantik, KEIN eigener „Resolved"-Zustand | §7.1 Schritt 4 + §7.3 — ein Kasten für beide Ausgänge (Erfolg/Fehlschlag), explizit als `info`-Typ der Hinweis-Konvention §3 benannt, `--arb-blue`-Token wiederverwendet statt neu vergeben, keine dritte Zustandsklasse |
| 2. armyList NICHT in derselben Spalte wie Auswahlliste/Effekt-Ausführung; Seitenleisten-Layout (`first_player`/`second_player`) bleibt unangetastet | §7.5 — belegt anhand `src/app.py` (3-Spalten-Struktur `left`/`center`/`right`), Kachel-Gruppe + Panel rendern ausschließlich in `center`; beide Fraktionsgruppen erscheinen nebeneinander INNERHALB der center-Kachel, nicht in den Sidebars |
| 3. „D6 Mortal Wounds" steht ÜBER den Schadens-Zahlenfeldern | §7.2 — Spaltenüberschrift muss über der tatsächlichen Zahlenfeld-Spalte stehen (festes Zwei-Spalten-Layout je Zeile), nicht nur über der Gesamtliste; V3-Fehler (Header über dem ganzen Panel, Felder nur inline bei ausgewählten Zeilen) explizit benannt |

## Bewusste §6.3-Abweichung

§7.4: Explodes-Gate nutzt zwei Buttons „Explodes!" / „Does not explode" statt des
Zahlenfelds aus §6.3. Begründung: der genaue Würfelwert hat keinen Folgezweck in der App —
nur die Schwellen-Erreichung zählt (binärer Ausgang), anders als z. B. beim Deny-Wurf, dessen
Wert weiterverrechnet wird. Auf ausdrücklichen Stakeholder-Wunsch (§g Korrektur 4), Wortlaut
„Does not explode" bereits bestätigt. Kein Präzedenzfall für andere Tischwürfe mit echtem
Zahlenwert — §6.3 bleibt dort Standard.

## Entscheidungsfrage

**§7 abnehmen?** Bei Abnahme werden die Mockup-Dateien gelöscht und B-028c1-Code für S169
freigegeben. Bei Korrekturwunsch bitte konkret benennen (Abschnitt/Zeile), analog zu den
Korrekturrunden V1→V2→V3.

Also ich hätte mir eine Darstellung in der spec vorgestellt wie in UI-Layout §1 für die UI. Wir betrachten hier ja eine UI-Komponente:


Beispiele: 
Three-column layout with a fixed top header. Each column scrolls independently.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              gameHeader                                      │
├──────────────────────┬───────────────────────────────┬───────────────────────┤
│   firstPlayer        │      gameActionsArea          │   secondPlayer        │
│   (armyList)         │      (phase-dependent)        │   (armyList)          │
│                      │                               │                       │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │   armyCard     │  │                               │  │    armyCard     │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │  ┌─────────────────┐  │
│  │detachmentCard  │  │                               │  │ detachmentCard  │  │
│  │  ┌──────────┐  │  │───────────────────────────────│  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │       gameProtocoll           │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │       (collapsible)           │  │  └───────────┘  │  │
│  │  ┌──────────┐  │  │                               │  │  ┌───────────┐  │  │
│  │  │ unitCard │  │  │                               │  │  │ unitCard  │  │  │
│  │  └──────────┘  │  │                               │  │  └───────────┘  │  │
│  └────────────────┘  │                               │  └─────────────────┘  │
│  ┌────────────────┐  │                               │                       │
│  │detachmentCard  │  │                               │                       │
│  └────────────────┘  │                               │                       │
└──────────────────────┴───────────────────────────────┴───────────────────────┘
```

**Column widths:** TBD — estimate ~25% / ~50% / ~25%
**Scroll:** Each column independent.
**Target devices:** Tablet/desktop landscape. No mobile optimization.


```
┌─────────────────────────────────────────────────────────────────────────────┐
│  VP  X=0    │  Arbiter · gameTitel  │  gameSize  │  gameType  │  VP  X=0   │
│  CP  Y=…    │                       │            │            │  CP  Y=…   │
└─────────────────────────────────────────────────────────────────────────────┘
```


```
┌──────────────────────────────────────────────┐
│  armyName                                    │
│  (default: "{faction} — {subfaction}")       │
│  ──────────────────────────────────────────  │
│  [{faction}]  [{subfaction}]                 │
│  ──────────────────────────────────────────  │
│  [Ability Button]   (phase-dependent)        │
│  [Ability Button]   (phase-dependent)        │
└──────────────────────────────────────────────┘
```

Und da sind noch mehr. 

Warum überträgst du nicht die Rückmeldung zum Mockup in so eine Spec-Darstellung? Dann verstehe selbst ich das auf einen Blick?

Oh Mann, und schon wieder eine Session, in der kein Mehrwert in der APp geschaffen wurde. NUR TEXT in einer Datei, der wieder gelöscht wird. Ich bin sehr unzufrieden. WO IST DAS PROBLEM? DRÜCKE ICH MICH NICHT KLAR GENUG AUS?

Es muss doch klar sein. Es SOLL AUSSEHEN WIE in ... und damit ist ein Bild gemeint. Warum schreibst du es NUR in Textform hin. Es muss doch auch möglich sein, dass ich sage. Nutze die Komponente zur UI aus der Nahkampfphase .... Und dann sollte eine graphische Darstellung in die Handoff und ggf. in die spec Dateien. das haben wir schon so oft hier gemacht. WO IST DAS PROBLEM???