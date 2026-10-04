# Name der Einheit fehlt im Glossar

244 · Fragen · von Testautor (Technik) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** AUF-4.3 verlangt jede *Einheit* „unter ihrem Namen“. Das [Glossar](../../domaene/glossar.md)
kennt keinen Namen der *Einheit*, und `Einheit` im Code hat keinen (`ausgangslage.yaml` nennt ihn
unter `Einheit:`, `katalog/ausgangslage.py` liest ihn nicht). Der Test prüft die Namen
„Boyz“, „Warboss“, „Necron Warriors“ und „Overlord“ wörtlich aus der YAML; er braucht keinen
Code-Bezeichner. Der Implementierer aber braucht einen, und die Prüfung Code → Glossar
verlangt dort einen Eintrag. Außerdem: AUF-4.6 sagt „vor der Wahl nach AUF-1.1“. Ich lese es als
„solange keine *Aufstellungszone* gewählt ist“ und prüfe die *Ausgangslage*; nach der Wahl des
*Gewinners* allein gehört noch keine Zone jemandem.

**Kosten.** Ohne Eintrag erfindet der Implementierer den Bezeichner, oder die Glossarprüfung
sperrt ihn.

**Gegenvorschlag.**
- A: Glossarzeile „Name“ (`name`) für den Namen der *Einheit* aus dem Datenblatt, Werte aus
  `ausgangslage.yaml`; AUF-2.6 nennt ihn bei den *Einheiten* der *Armeen*.
- B: Kein Begriff; der Implementierer wählt den Bezeichner und trägt ihn selbst ein.
Dazu: Stimmt meine Lesart von AUF-4.6?
Empfehlung: A.

**Stellungnahme.** A angenommen. Neue Glossarzeile „Name | unit name | name“: Name der
*Einheit* aus ihrem Datenblatt, jede *Einheit* hat einen (`core_rules.txt:552`, `:553`), Werte
in `ausgangslage.yaml` unter `Einheit`. Das Wort stand schon im freigegebenen AUF-4.3; dort ist
*Namen* jetzt kursiv, sonst unverändert. AUF-2.6 bleibt, wie es ist: Die Glossarzeile nennt
die Quelle der Werte, eine Neufassung gegen bestehende Tests wäre ein neues Kriterium.

AUF-4.6: Lesart stimmt. „Die Wahl nach AUF-1.1“ ist die der *Aufstellungszone*; erst sie
lässt eine Zone jemandem gehören. Das Kriterium gilt damit auch nach der Wahl des *Gewinners*
allein. Der Test prüft nur die *Ausgangslage*; ob er das Kriterium trifft, beurteilt der
Fachkritiker. Mein Hinweis: Ein zweiter Fall nach `gewinnerWählen` ohne Zonenwahl deckte es ganz.
