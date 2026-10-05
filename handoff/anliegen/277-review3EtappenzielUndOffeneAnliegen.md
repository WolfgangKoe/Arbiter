# Review 3: Etappenziel ohne fehlende Kriterien, offene Anliegen veraltet

277 · Kritik · von Fachkritiker (Domäne) → Reviewer · Runde 1/3 · erledigt

## Runde 1

**Befund.** Zwei Stellen in `handoff/review.md` geben dem Stakeholder vor der Freigabe ein
falsches Bild der Domäne.

1. *Nächstes Vorgehen, Etappenziel:* „Wenn ein Punkt je Zyklus fertig wird, sind das 4
   Zyklen.“ Das zählt nur das Bauen. Für drei der vier Punkte aus „Danach“ gibt es weder
   Kriterium noch Glossareintrag: `grep -i "kohärenz\|protokoll\|übergeh\|zurück\|vernichtet\|ziehen"`
   über `domaene/anforderungen/` findet nichts, im Glossar steht nur *Sperre* mit Verweis
   aufs Ziel. [Etappe 1](../../domaene/etappen/01-aufstellen.md) verlangt aber Ziehen mit
   Maus und Touch, Zurücklegen in die *Ablage*, „zurück“ (vorige Stelle, sonst *Ablage*),
   „gemeinsam übergehen“, das stets einsehbare Protokoll, die *Sperre* beim Beenden bei
   fehlenden *Modellen* (übergangen gelten sie als vernichtet) und ohne Kohärenz. Kohärenz
   ist eine eigene Messregel mit zwei Fällen (2″ horizontal und 5″ vertikal zu einem
   anderen *Modell*, ab sechs *Modellen* zu zwei; `domaene/referenz/rules/core_rules.txt:434`,
   vernichtet bei fehlendem Platz `:441`); die Boyz der Ausgangslage fallen unter den
   zweiten Fall. Auch Wählen per Klick hat bisher nur Kriterien der Domäne (AUF-1.1, 1.2,
   1.5, 1.6), keines für die Handlung am Bildschirm und die Anzeige der *Sperre*
   ‚nicht wählbar‘.
2. *Offene Anliegen zur Technik und DoD 3* sind veraltet: 259, 260 und 269 („Grenzen der
   Zone in AUF-4.6“) stehen beim Testautor als offen, 261 als Nachprüfung des
   Implementierers; alle vier sind erledigt und gelöscht (`628381c`, `a82c85a`). DoD 3
   nennt das Löschen der Items „uncommittet“, es steht in `bb18997`. Das Inkrement nennt
   „Stand `9977e0e`“, danach haben `50ab353` die Akzeptanztests und `18d55b8`
   `technik/arbiter` geändert. Fachlich nachgeprüft: Die Akzeptanztests sind auf dem
   aktuellen Stand grün (175), und AUF-4.6 ist nicht mehr strittig.

**Kosten.** Zu 1: Der Stakeholder plant mit 4 Zyklen, ohne zu sehen, dass in jedem davon
erst Kriterien und Glossar entstehen müssen, für Kohärenz mit eigener Messung; das
Zyklusziel für Plan 4 verspricht eine Handlung, deren Bildschirmseite noch niemand
beschrieben hat. Zu 2: Er liest, AUF-4.6 sei beim Testautor offen, und gibt eine Abnahme
frei, die er für unvollständig halten muss.

**Gegenvorschlag.** Zu 1: Im Etappenziel ein Satz, dass für Ziehen, Zurück mit Übergehen
und Protokoll sowie Beenden mit Kohärenz die Kriterien fehlen und je Zyklus zuerst die
Domänenphase sie schreibt; Beleg der grep oben. Die Schätzung bleibt Sache des Reviewers.
Im Zyklusziel ergänzen, dass Plan 4 Kriterien für Wählen am Bildschirm braucht. Zu 2:
Erledigte Anliegen streichen, „uncommittet“ streichen, Stand auf den letzten geprüften
Commit setzen. Erledigt, wenn beides im Review steht.

**Stellungnahme.** Beides nachgeprüft und umgesetzt in `handoff/review.md`. Zu 1: Im
Etappenziel stehen die fehlenden Kriterien mit dem grep als Beleg und Kohärenz als eigene
Messregel (`core_rules.txt:434`); Schätzung 4 Zyklen, für Beenden mit Kohärenz womöglich
ein fünfter. Im Zyklusziel: Plan 4 schreibt zuerst Kriterien für Wählen am Bildschirm und
die Anzeige ‚nicht wählbar‘. Zu 2: 259, 260, 261, 269 gestrichen; DoD 3 nennt `bb18997`;
Stand `18d55b8` (Kritik `196e31c`). DoD 1 und 2 auf diesem Stand wiederholt: `technik/tests`
200 grün, Abdeckung 99 %/100 % unverändert; `prozess/pruefungen` jetzt 757 grün.
