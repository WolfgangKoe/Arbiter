# Datenblätter im Glossar und in den Daten

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 4800 F2 B gewählt: je
Datenblatt seine Modellarten mit eigenem Profil, Zahlen in der Einheit des Glossars, der
*Durchmesser* bei der Modellart; die Ausgangslage nennt je *Einheit* Datenblatt und Zahl der
*Modelle*. Zu F3 A verlangt er eine Struktur, die sich jederzeit ergänzen oder füllen lässt,
ohne dass die Systematik bricht. Veraltet sind danach:
- [Glossar](../../domaene/glossar.md): Datenblatt, Profil und Modellart fehlen; *Einheit*
  (Zeile 26) und *Name* (Zeile 46) nennen das Datenblatt ohne Begriff, *B* (Zeile 18) und
  *Name* verweisen auf `ausgangslage.yaml`.
- [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml): `durchmesser` zehnmal je
  Einheit, `bewegungsweite` je Einheit statt je Modellart.
- [MIV-1.3](../../domaene/anforderungen/missionsvorbereitung/ausgangslage.md): „je Eintrag
  unter `durchmesser` ein *Modell*“ beschreibt das alte Format.

**Kosten.** Kommen weitere Einheiten (Plan 8 nennt Ork-Psioniker und Canoptek-Spinne für
Etappe 2) ins alte Format, wird jede einzeln umgebaut, samt `katalog/` und seinen Tests.

**Gegenvorschlag.** In der Domänenphase 9, vor neuen Einheiten:
1. Datenblatt (datasheet, `core_rules.txt:552`), Profil (profile, `:561`) und Modellart
   schlägst du dem Stakeholder als Begriffe vor; er gibt sie mit Plan 9 frei. Ob Modellart
   einen Regelbegriff hat, prüfst du am Regeltext (`:562`, „No.“).
2. Die vier Datenblätter schreibst du nach der Gliederung aus
   Anliegen 4880 (K1 bis K6) in
   `domaene/daten/katalog/orks/datenblaetter.yaml` und `.../necrons/datenblaetter.yaml`, nur
   mit `bewegungsweite` und `durchmesser`, je Wert mit Fundstelle.
3. `ausgangslage.yaml` nennt je *Einheit* Datenblatt und je Modellart die Anzahl; welche
   Modellarten die vier *Einheiten* haben, entscheidet der Regeltext oder der Stakeholder.
4. MIV-1.3 und die Glossarzeilen B, Einheit, Name ziehst du nach.

Wann: Domänenphase 9, als Teil des Items aus [4882](4882-itemKatalogwerteGliedern.md).

**Stellungnahme.**
