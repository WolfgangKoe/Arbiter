# Retro 5: Maßstab „Sperre fehlt“ und die Frage nach leeren Tests

695 · Kritik · von Fachkritiker → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Die [Retro](../retro.md) wartet auf Freigabe; drei Stellen treffen den Maßstab,
mit dem ich ab Zyklus 6 prüfe.
1. P1, Kritik: „Hält auf: … Sperre greift zu Unrecht oder fehlt“ und „Wartet: Randfälle,
   Lücken abseits des Happy Path“. Eine fehlende *Sperre* ist fast immer ein Randfall: Der
   *Spieler* tut etwas Unerlaubtes. Das Ziel sagt „Was nicht erlaubt ist, wird gesperrt“.
   Ob eine fehlende *Sperre* das Item aufhält oder wartet, kann ich aus dem Text nicht
   entscheiden; jeder Kritiker legt es anders aus.
2. P1 gibt 693 F1 A nicht vollständig wieder: „Ablage von Hilfsfunktionen“ fehlt unter
   „wartet“. Die Empfehlung sagt aber, die Antworten aus 693 stünden in P1.
3. Der Stakeholder fragt in [692](692-architekturbildHexagonal.md) (Stellungnahme), ob es
   grüne Tests gibt, die nichts prüfen. Der Architekt empfiehlt dort, Mutationstests jetzt
   per Kommentar zur Retro 5 auszulösen. Die Retro, die er freigibt, nennt weder die Frage
   noch die Wahl; im Backlog steht weiter „spätestens zu Etappe 2“.

**Kosten.** Zu 1: Entweder hält jede fehlende *Sperre* am Rand das Item auf (der
Feinschliff von Zyklus 5 kehrt zurück), oder eine Regel des Ziels rutscht als „wartet“
durch. Zu 2: Der Stakeholder gibt einen Text frei, der von seiner Antwort abweicht. Zu 3:
Er muss sich selbst erinnern, die Entscheidung als Kommentar nachzutragen; sonst bleibt
seine Sorge ohne Antwort in der Retro.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): Ich 1, Ich 3, 693 F1 A und F2 A, Abschnitt
Backlog der Retro.
1. In P1: „Hält auf: … eine *Sperre* fehlt, die ein Kriterium des Items verlangt, oder greift
   zu Unrecht. Verbietet der Regeltext etwas, das kein Kriterium sperrt, ist das eine Lücke
   der Anforderung und wartet als Anliegen an den Anforderungsautor auf die nächste
   Domänenphase.“ Hältst du das für eine neue Entscheidung, frag den Stakeholder mit dieser
   Empfehlung.
2. „Ablage von Hilfsfunktionen“ unter „wartet“ ergänzen.
3. Im Abschnitt Backlog die Wahl nennen: Mutationstests jetzt (Empfehlung des Architekten,
   692) oder spätestens zu Etappe 2, mit Link auf 692. Fachlich dazu: Die beiden Beispiele
   dort prüfen ihr Kriterium wörtlich. AUF-17.1 ist selbst der Fall „ändert nichts“, OBJ-1.1
   eine Tatsache des Katalogs. Leer ist aus Sicht der Domäne ein Test, der weniger prüft als
   sein Kriterium verlangt; das prüfe ich in Schritt 2 und 5 je Test. Was dort durchrutscht,
   findet erst ein Mutationstest.

**Stellungnahme.** Umgesetzt in der [Retro](../retro.md):
1. P1, Kritik: Es hält auf, wenn eine *Sperre* zu Unrecht greift oder fehlt, obwohl ein
   Kriterium sie verlangt. Eine *Sperre*, die nur der Regeltext verlangt, wartet als Lücke
   auf die nächste Phase. Ich lese das als Auslegung von 693 F1 A, nicht als neue
   Entscheidung: Die Antwort stellt „Sperre fehlt“ in den Happy Path des Items, Lücken
   daneben lässt sie warten. Der Wortlaut steht in P1; der Stakeholder sieht ihn bei der
   Freigabe und kann ihn kommentieren.
2. „Ablage von Hilfsfunktionen“ steht unter „wartet“ (zugleich 697, 2).
3. Der Abschnitt Backlog nennt die Frage aus 692 und die Wahl: jetzt als P3 (Empfehlung
   des Architekten) oder spätestens zu Etappe 2, per Kommentar. Statt eines Links steht dort
   „Anliegen 692“, weil die Retro an ihrem Höchstmaß ist.
