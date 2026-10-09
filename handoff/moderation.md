# Moderation

Stand vor Freigabe Plan 4: 11 Anliegen offen, 318 `erledigt`. Kritikrunde der Domänenphase
läuft; zu den Items von [Plan 4](plan.md) hängt kein offenes Anliegen (DoR 4).

## Dran
Blockiert die Freigabe: nichts. Die Kritik an AUF-5.5 (Anliegen 318)
ist `erledigt`, AUF-5.5 steht nicht im Umfang.
- Architekt: Anliegen 322 (Beispiel in T2; drei Kürzel).
- Organisationsentwickler: Anliegen 321 (ein Satz in DoR 5, Stellungnahme
  leer); Anliegen 296 nachprüfen (angenommen, F1 bis F3 beantwortet);
  [289](anliegen/289-pruefungenBrechenAmHookDesNachbarnAb.md) und
  Anliegen 150 warten auf 304 und 216.
- Regelumsetzer: Anliegen 216,
  [246](anliegen/246-dashboardAlleSessionsMitSeitenzaehler.md),
  [249](anliegen/249-werkzeugFestUndImportvertragDerTests.md),
  [275](anliegen/275-dashboardSichtDerAnliegen.md),
  Anliegen 304.
- Testautor: AUF-5, AUF-6, QUE-3 nach Freigabe (Technikphase), kein Anliegen.
- Stakeholder, Anforderungsautor, Fachkritiker: keins.

## Vorschläge
- Löschen: 318 (Kopf `erledigt`, Löschlauf, kein Zug nötig).
- Zusammen in einem Lauf des Regelumsetzers: 246 mit 275 (dieselbe Datei
  `rollenregeln/dashboard.py`).
- Regelumsetzer, Strang Hook-Code, höchstens ein Lauf
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): 304 zuerst (`pyproject.toml`), dann 216,
  dann 249 (ändert `pyproject.toml` und Importvertrag). 246 und 275 laufen als eigener Strang
  daneben, wenn `dashboard.py` nicht von Hooks importiert wird.
- Organisationsentwickler: 321 ist ein reiner Textstrang (`ablauf.md`) und läuft neben jedem
  Strang; nach 304 schließt er 289, nach 216 meldet er 150 an den Stakeholder.
- Architekt: 322 gleichzeitig; die Vertragsarbeit in
  [web.md](../technik/architektur/web.md) (Plan 4) hat Vorrang, 321 verlangt dort O3 nachzuziehen.
- Vorrang hat Plan 4; die Kette läuft daneben.

## Fragen an dich
Keine offen.
