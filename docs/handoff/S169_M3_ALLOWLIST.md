STATUS: NEEDS-DECISION

# S169 — Retro-M3: Bash-Allowlist kann nur der Stakeholder eintragen

Lebensdauer: bis der Stakeholder die Regeln eingetragen (oder verworfen) hat, danach löschen.

## Befund

Retro-M3 (S168) ist freigegeben, aber **nicht durch Claude umsetzbar**: Der
Auto-Mode-Permission-Classifier blockiert sowohl den Subagent-Start als auch das
`update-config`-Skill, sobald `.claude/settings.json` (Permission-Konfiguration) das Ziel
ist — Selbst-Erweiterung der eigenen Rechte ist im Auto-Modus gesperrt. Ein direkter
Datei-Edit würde die Sperre umgehen und unterbleibt bewusst.

## Bitte an den Stakeholder

In `.claude/settings.json` unter `permissions.allow` ergänzen (alternativ interaktiv beim
nächsten Prompt „immer erlauben" wählen):

```json
"Bash(rm docs/handoff/:*)",
"Bash(curl -s -o /dev/null -w \"%{http_code}\" http://localhost:8501)"
```

Zweck (S168-Retro): Handoff-Lifecycle (`rm docs/handoff/*`) und App-Health-Check
(`curl :8501`, Briefing-Pflicht) hingen in S168 am Classifier.

## Konsequenz für S169

Der Handoff-Aufräum-Task (Task 6, Screenshot-/Mockup-Löschung) versucht das Löschen
regulär; wird `rm` erneut blockiert, legt der Koordinator die endgültige Lösch-Liste als
DONE-Handoff ab und der Stakeholder löscht manuell.
