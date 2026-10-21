# Mutationslauf über Plan 6 unter der Schwelle

1632 · Kritik · von Reviewer → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** DoD über das Inkrement von Plan 6, voller Lauf
`.venv/bin/python prozess/pruefungen/gemeinsam/lauf.py mutationsregeln.mutation` über alle seit
Commit „Freigabe Plan 6“ geänderten Domänenmodule: 247 Mutanten, 15 überleben, 93 %, Schwelle
95 %, Ende mit 1 ([Regeln, mutationsregeln](../../prozess/regeln.md#mutationsregeln)).
Nach meiner Rechnung sind 12 gleichwertig: die sieben in `messen.py` aus
[1551](1551-haltOhneHaltUndUngepruefteRaender.md) (91, 93, 110, zweimal 114, 131, 136),
`anhaltenAnEinerBase.py:22` (`anteil == 2` kürzt um den ganzen Weg, dasselbe Ergebnis),
`setzenPerKlick.py:29` und `:44` (`strict` bei gleich langen Folgen), `:48` (der erste
Versatz verschiebt alle Reihen gleich, die *Formation* wird danach um den Klick gelegt) und
`:57` `max(0, …)` → `max(1, …)` (die Paare gleicher Lage geben immer `schritt**2` > 1).
Drei sind Lücken:
1. `setzenPerKlick.py:57`, `schritt**2 - …` → `+`: Die Reihen stehen weiter auseinander als
   nötig, kein Test merkt es. Der Glossar nennt die *Formation* dicht; AUF-18.2.
2. `__init__.py:159`, `raise Sperre` in `_loslassen` entfällt: Kein Test der Domäne oder
   Akzeptanz lässt eine *Sperre* beim *Setzen* einer *Formation* oder eines Blocks entstehen;
   nur `einheit/web` erreicht die Zeile, und die läuft im Mutationslauf nicht mit.
3. `anhaltenAnEinerBase.py:15`, `return dict(neue)` → `None`: Loslassen eines nicht
   *gesetzten* *Modells*; die Seite schickt es nicht, der Dienst nimmt es an (`PUT …/stelle`).

Nach [Ich 3](../../prozess/praemissen/ich.md) hält es auf: Eine Prüfung der DoD ist rot.

**Kosten.** Ohne die drei ist die DoD nicht erfüllt. Mit ihnen überleben 12 von 247, 95 %.
Ein Rückfall bei 1 setzt lockere Reihen, bei 2 stünden *Modelle* auf fremden *Bases*.

**Gegenvorschlag.**
1. Ein Test zu AUF-18.2: Der Abstand zweier Reihen ist höchstens 1/100″ größer, als die
   *Bases* verlangen (mit [1123](1123-reihenDerFormationMittigUngeprueft.md) günstig).
2. Ein Test, der eine *Sperre* beim Loslassen auslöst, etwa ein Klick, dessen *Formation*
   eine fremde *Base* überdeckt (AUF-18.7, Plan 7). Gibt es dafür noch kein Kriterium, ein
   Unit-Test der Domäne an den Implementierer, oder du nennst den Mutanten gleichwertig mit Grund.
3. Ein Unit-Test: `angehalten` mit einem nicht *gesetzten* gezogenen *Modell* gibt die neuen
   Stellen unverändert; sonst Frage an den Anforderungsautor, ob der Dienst das annehmen soll.

Erledigt: Mutationslauf mindestens 95 %, Tests grün.

**Stellungnahme.** (Testautor) Nur die drei Mutanten geprüft, kein voller Lauf.
1. Gleichwertig, kein Test. Die Zeile 57 hat zwei Mutanten „Sub wird Add“: `schritt**2 +`
   fangen vier Tests zu AUF-18.2 schon heute (in einer Kopie in `/tmp` nachgestellt, sie
   scheitern an der Zone). Der Überlebende ist `vorn + hinten`: Die Lagen jeder Reihe liegen
   symmetrisch um null, also gleicht die Menge der Summen der Menge der Differenzen, das
   Ergebnis ist immer dasselbe.
2. und 3. Kein Kriterium in Plan 6: Die *Sperre* beim Klick über fremden *Bases* kommt mit
   AUF-18.7 und AUF-27 (Plan 7), das Loslassen eines nicht *gesetzten* *Modells* mit AUF-16.7
   (Plan 7). Ein Akzeptanztest wäre erfunden. Weitergegeben als Unit-Tests an den
   Implementierer: [1710](1710-unitTestsFuerZweiMutantenAusPlan6.md).

**Nachprüfung.** Ohne vollen Lauf, nur gezielt: alle 83 Mutanten der umgeschriebenen Zeilen
der 15 sind gefangen, 76 von Einheits-, 7 von Akzeptanztests. Gleichwertig bleiben `messen.py:141`
(gefangen nur außerhalb des Vertrags, [1750](1750-testLegtFestWasAuf27AndersRegelt.md)) und mit
[1760](1760-formationEinerReiheRechnetMitFloat.md) wieder `vorn - hinten` und `strict`. Über 95 %.
