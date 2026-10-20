# Moderation

Stand vor Freigabe Plan 6. Die Freigabe hält kein offenes Anliegen auf: Plan 6 nennt jedes
Item bereit. Vor dem Bauen (Technikphase) hängen Item 1 an
[622](anliegen/622-zugschwelleUngeprueft.md) und Item 2 an
[830](anliegen/830-knopfInDerEinheitenkarteBekommtKeinenKlick.md).

## Dran
- Stakeholder: nichts. Anliegen 1000 ist mit
  A beantwortet und erledigt, der Plan nennt es unter „Offene Anliegen“ noch als an dich.
- Testautor: [622](anliegen/622-zugschwelleUngeprueft.md) zuerst (blockiert Item 1),
  [621](anliegen/621-restDerEinheitOhneGesperrte.md); Nachprüfung
  [580](anliegen/580-auswahlPyAlsHilfsmodul.md).
- Implementierer: [680](anliegen/680-markierterTextSperrtDasZiehen.md),
  [682](anliegen/682-gezogeneKarteVerschwindetAmSpaltenrand.md);
  [830](anliegen/830-knopfInDerEinheitenkarteBekommtKeinenKlick.md) wartet auf die
  Technikphase (blockiert Item 2).
- Reviewer: [640](anliegen/640-review5BelegeUndWorteDesSpielers.md),
  [660](anliegen/660-klickpfadZeigtNichtAllesNeue.md); Nachprüfung
  [620](anliegen/620-mockupsNachDemEinbauLoeschen.md).
- Regelumsetzer: [490](anliegen/490-fortschrittInPlanReviewRetro.md); Nachprüfung
  [610](anliegen/610-erledigteLoeschenImPreCommitVernichtetArbeit.md).
- Ux: Nachprüfung [683](anliegen/683-aufstellenKlickenOderZiehen.md),
  [684](anliegen/684-anforderungenFuerKlickenBlockUndGrund.md),
  [685](anliegen/685-bedienungVorDemBildschirmTestPruefen.md).
- Fachkritiker: Nachprüfung [681](anliegen/681-zeigenWasDerSpielerTunKann.md).
- Architekt: Nachprüfung [550](anliegen/550-auswahlGehoertNichtZumZiehen.md);
  [921](anliegen/921-zeileUnterDemGrundIstKeinGrund.md) wartet auf die Technikphase.
- Organisationsentwickler: Nachprüfung
  [730](anliegen/730-werKritisiertUndZurueckgenommeneRegeln.md), wartet auf die
  Prozessphase.
- Anforderungsautor: [978](anliegen/978-randfaelleKlickUndZiehenNachPlan6.md) hält Plan 6
  nicht auf (Lücken abseits des Happy Path, Plan 7); der Kopf sagt „wartet auf die
  Domänenphase“, der Stand führt ihn als dran. Ob jetzt oder erst nach Zyklus 6, ist nicht
  geklärt; ich entscheide nichts, der Koordinator ordnet zu.
- Wartend: [421](anliegen/421-schritteAbhaken.md) auf 490;
  [740](anliegen/740-commitFuerMehrereItemsImAblauf.md) und
  [991](anliegen/991-fortschrittVorDerPhaseVerwirftHakenUndHindernis.md) auf die
  Prozessphase (991 baut erst nach 490).

## Vorschläge
- Schließen (Verfasser, nach Nachprüfung): 550, 580, 610, 620, 681, 683, 684, 685;
  730 erst in der Prozessphase, 421 nach 490.
- Zusammen (Testautor): 622 und 621, getrennte Testdateien.
- Zusammen (Reviewer): 640 und 660, gleiche Datei `review.md`.
- Zusammen (Implementierer): 680 und 682, wenn dieselbe Frontend-Datei.
- Zusammen (Regelumsetzer): 490 und 991, beide im Fortschritt-Skript; 991 nach 490.
- Randfälle Plan 7 (Anforderungsautor): 978 deckt sich mit AUF-16.7, 22 und 23 im
  [Plan](plan.md#randfälle-plan-7); beim Schnitt von Plan 7 zusammen nehmen.
- Planer: „Offene Anliegen“ im Plan nennt 1000 noch, obwohl erledigt; streichen.
- Löschen: die Anliegen mit Status erledigt (670, 800 bis 820, 821 bis 1000) löscht
  `anliegenregeln/erledigteLoeschen.py`.
- Stränge gleichzeitig ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): Testautor,
  Implementierer, Reviewer, Regelumsetzer (490, danach 991); die Nachprüfungen der
  Verfasser getrennt. Kette: 622 vor Item 1, 830 vor Item 2.

## Fragen an dich
Keine offen. Annahmen ohne Antwort gibt es nicht.
