# Fortschritt

Etappe, Zyklus, Phase und nächsten Schritt nennt der Stand. Mechanismus:
`standregeln/phasenfolge.py` ([Standregeln](../regeln/standregeln.md)).

Wo ein Plan umgesetzt wird, zeigt der Abschnitt `## Fortschritt` vor `## Freigabe`, wie weit
die Phase ist und was sie aufhält (Anliegen 421): im Review für die Domänenphase danach (sie
setzt sein Zyklusziel um; ohne Review, in Zyklus 1, entfällt er), im Plan für die
Technikphase, in der Retro für die Prozessphase. Er steht ab dem Schreiben der Datei, vor
ihrer Freigabe, alle Zeilen offen bis zum Beginn der Phase; beginnt die nächste Phase, erhält
die Datei der vorigen ihren Endstand (Anliegen 740, 982). Er wächst mit der Phase und zählt nicht zum
Höchstmaß. Ihn schreibt nur das Skript, der Autor lässt ihn beim Ändern stehen. Keine Rolle
liest ihn für ihre Arbeit: Ihre offenen Schritte nennt ihr der Hook beim Start.

Eine Zeile je Schritt nach der Tabelle, `- [ ] <Rolle>: <Schritt>`, abgehakt `- [x]`.
Darunter eingerückt, was ihn aufhält, `Hindernis: <Text> (Anliegen <nr>)`, angenommen mit
`; beseitigt: Commit „<Betreff>“`, und ein Kommentar des Stakeholders
`Kommentar: <Text> (Anliegen <nr>)`.
- Fakt: Ein Hook hakt nach jedem Rollenlauf ab, was die Tabelle als Fakt nennt.
- Befehl: Die Rolle hakt ihren Schritt am Ende ihres Laufs mit dem Befehl ab, als Kritiker,
  wenn keiner seiner Befunde mehr aufhält ([Kritik](kritik.md)). Hält sie etwas auf, meldet
  sie es mit dem Befehl und nennt die Rolle, die es beseitigen kann; das Skript legt das Anliegen an (Kritik, an den
  Stakeholder Fragen) und schreibt die Zeile `Hindernis:`.
- Dashboard: Der Fortschritt der laufenden Phase steht als kompakte Liste neben dem
  Anliegenboard. Der Stakeholder hakt eine Zeile, die kein Fakt abhakt, mit einem Klick ab;
  ein gesetzter Haken bleibt, alle Haken sehen gleich aus und heben sich deutlich vom leeren
  Kästchen ab. Ein Klick auf ihren Text öffnet das Kommentarfeld (Anliegen 1670, 2060). Der
  Kommentar wird ein Anliegen von ihm an die Rolle der Zeile.

Phase · Schritt | Zeile | abgehakt durch
---|---|---
Domäne 1 bis 3, nur ohne Etappe | Planer: Etappe · Architekt: Kritik an der Etappe · Stakeholder: Freigabe Etappe | Fakt: Etappendatei neu · Befehl · Fakt: Commit
Domäne 4 | Anforderungsautor: Happy Paths zum Zyklusziel · UX: Mockups, bei einer Oberfläche | Befehl
Domäne 5 | Fachkritiker: Kritik an Anforderungen und Mockups | Befehl
Domäne 6 | Planer: Plan geschrieben | Fakt: `# Plan · Zyklus <n>`
Domäne 7 | je Kritiker: Kritik am Plan | Befehl
Domäne 8 | Stakeholder: Freigabe Plan | Fakt: Commit
Technik 1 je Item mit beiden Hälften | Architekt: Vertrag zu Item <k>, bei beiden Hälften | Befehl
Technik 1, 2 je Item | Testautor: Tests zu Item <k> · je Kritiker: Kritik daran | Fakt: jedes Kriterium des Items hat einen Test · Befehl
Technik 3 je Item | Implementierer: Tests zu Item <k> grün · Architekt, Reviewer: je Kritik am Code | Befehl
Technik 4 | Reviewer: DoD über das Inkrement | Befehl
Technik 5 je Item | Fachkritiker: Item <k> abgenommen · Planer: Item <k> gelöscht | Befehl · Fakt: Datei weg
Technik 6, 7 | Reviewer: Review geschrieben · je Kritiker: Kritik am Review · Stakeholder: Freigabe Review | Fakt: `# Review · Zyklus <n>` · Befehl · Fakt: Commit
Prozess 1 | Organisationsentwickler: Retro geschrieben | Fakt: `# Retro · Zyklus <n>`
Prozess 2, 3 | je Kritiker: Kritik an der Retro · Organisationsentwickler: Nachkorrektur | Befehl
Prozess 4 | Stakeholder: Freigabe Retro | Fakt: Commit
Prozess 5 je Prozess-Item | Rolle des Items: P<k> | Fakt: Commit `P<k>:`
Prozess 6 | Koordinator: nach `dev` gepusht | Fakt: `origin/dev` enthält den letzten Commit

Mechanismus: `standregeln/fortschritt.py` (Zeilen und Fakten, `nächsteLage`, `alleOffen`, [Standregeln](../regeln/standregeln.md);
die Zeilen „Kritik am Review“ nur Text, Anliegen 3660);
Befehl zum Abhaken: `standregeln/abhaken.py` (Retro 5, P2); Hindernis: `standregeln/hindernis.py`,
`standregeln/beseitigt.py`; Dashboard: `rollenregeln/dashboardFortschritt.py` (Liste, Haken,
Sperre der Zeilen mit Fakt), `standregeln/zeilenZug.py` (weist den Haken darauf ab; Anliegen
2061); ob sich die Haken deutlich abheben: Urteil des Stakeholders.
