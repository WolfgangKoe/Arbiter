# Moderation

Stand vor Freigabe Retro 5. Erledigt und zu löschen: 687, 693, 694, 695, 696, 697 (Links
auf 687 in `685` Zeile 35 gehen dann ins Leere; Verfasser Ux bei der Nachprüfung). Offen
bleiben 21 Anliegen, davon blockiert keins die Freigabe. Blockiert Zyklus 6: 684 vor 681
(Aufstellen per Klick).

## Dran
- Stakeholder: keine Frage offen. Freigabe und Kommentar in der
  [Retro](retro.md); sein Kommentar verweist auf 692.
- Anforderungsautor: [684](anliegen/684-anforderungenFuerKlickenBlockUndGrund.md) zuerst,
  das Item in Plan 6 hängt daran; dazu [670](anliegen/670-karteSpringtWennEinGrundErscheint.md).
- Ux: [681](anliegen/681-zeigenWasDerSpielerTunKann.md) nach 684;
  [620](anliegen/620-mockupsNachDemEinbauLoeschen.md); Nachprüfung
  [683](anliegen/683-aufstellenKlickenOderZiehen.md) (deine Antwort A liegt vor) und
  [685](anliegen/685-bedienungVorDemBildschirmTestPruefen.md).
- Implementierer: [680](anliegen/680-markierterTextSperrtDasZiehen.md),
  [682](anliegen/682-gezogeneKarteVerschwindetAmSpaltenrand.md).
- Reviewer: [640](anliegen/640-review5BelegeUndWorteDesSpielers.md),
  [660](anliegen/660-klickpfadZeigtNichtAllesNeue.md).
- Testautor: [621](anliegen/621-restDerEinheitOhneGesperrte.md),
  [622](anliegen/622-zugschwelleUngeprueft.md); Nachprüfung
  [580](anliegen/580-auswahlPyAlsHilfsmodul.md).
- Regelumsetzer: Anliegen 650 und
  [601](anliegen/601-commitHooksNachPfad.md) (halten jede Rolle auf, Retro nennt sie),
  [686](anliegen/686-wartetAufImKopf.md) (P2),
  [490](anliegen/490-fortschrittInPlanReviewRetro.md) (P1; Teil 2 erst Prozessphase 6);
  Nachprüfung [610](anliegen/610-erledigteLoeschenImPreCommitVernichtetArbeit.md).
- Organisationsentwickler: [421](anliegen/421-schritteAbhaken.md), deine Antworten liegen
  vor, es wartet auf 490.
- Architekt: Nachprüfung [550](anliegen/550-auswahlGehoertNichtZumZiehen.md) und
  Anliegen 692 (deine Antworten A, A liegen vor).

## Vorschläge
- Zusammen (Anforderungsautor): 684 und 670 in einem Lauf; 670 erweitert QUE-2.5.
- Zusammen (Reviewer): 640 und 660, gleiche Datei `review.md`.
- Zusammen (Testautor): 621 und 622, getrennte Testdateien.
- Zusammen (Implementierer): 680 und 682 ein Lauf, wenn dieselbe Frontend-Datei; sonst
  gleichzeitig nach `git status`. Beide hängen nicht an 684.
- Schließen (Verfasser nach Nachprüfung): 550, 580, 610, 683, 685, 692; 421 nach 490.
- Löschen: die erledigten 687, 693 bis 697 löscht `anliegenregeln/erledigteLoeschen.py`.
- Stränge Regelumsetzer, ein Hook-Code-Lauf zugleich
  ([Ablauf](../prozess/ablauf.md#gleichzeitige-läufe)): Kette 650, 601, dann 686 (P2) und
  490 (P1).
- Stränge Zyklus 6 gleichzeitig: Anforderungsautor (684/670), Implementierer (680/682),
  Testautor (621/622), Reviewer (640/660); Ux ist eine Kette (684, dann 681), 620 sofort.

## Fragen an dich
Keine offen. 687 und 693 sind beantwortet und erledigt.
