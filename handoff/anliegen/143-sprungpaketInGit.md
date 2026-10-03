# Sprung-Paket: gebaut in git oder vor jeder Installation gebaut

143 · Fragen · von Regelumsetzer → Stakeholder · Runde 1/3 · offen

## Runde 1
**Befund.** Die Sprung-Erweiterung ([124](124-sprungPerKlickErproben.md)) besteht aus
vier Quelldateien in `prozess/pruefungen/sprung/` und dem daraus gebauten Paket (`.vsix`,
eine Zip-Datei). In git steht bisher das Paket `arbiter-sprung.vsix`. Im Arbeitsbaum liegen
die Löschung (in der Staging-Area) und die Zeile `prozess/pruefungen/sprung/*.vsix` in
`.gitignore`, beides nicht committet. Das Paket in git war veraltet: Du hast eine Version
mit dem fehlerhaften Suchmuster installiert ([133](133-sprungpaketBeimStakeholderVeraltet.md)).

**Kosten.**
- Paket in git: Du installierst mit einem Befehl, ohne zu bauen. Aber das Paket ist eine
  Kopie der Quelle und veraltet bei jeder Änderung still, sobald jemand vergisst, es neu zu
  bauen. Genau das ist passiert. Jede Änderung braucht zwei Dateien im Commit; ein Test, der
  Paket und Quelle vergleicht, wäre nötig, und der Zip-Inhalt ändert sich mit jedem Bau,
  auch ohne Änderung der Quelle (Zeitstempel).
- Nur Quelle in git: Vor jeder Installation läuft `baue.py` (Python 3 hast Du, die
  Anleitung steht in 124): ein Befehl mehr in einer Zeile. Nichts kann veralten, git zeigt
  nur lesbare Änderungen. Wer das Paket nicht gebaut hat, hat keins.

**Empfehlung.** Nur Quelle in git. Die Erweiterung ist ein Wegwerf-Versuch; ein
abgeleitetes Binärpaket gehört nicht ins Archiv, und die Zeile mit `baue.py` kostet Dich
nichts, was die Fehlerquelle aufwiegt. Mit „.“ bleiben Löschung und `.gitignore`-Zeile, wie
sie sind; der Koordinator committet sie dann.

**F1 · .vsix in git?** Empfehlung: nein, nur Quelle, gebaut mit `baue.py`.
Antwort: .
