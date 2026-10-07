"""Pfade, die keine Rolle schreibt, mit der Meldung dazu."""

from gemeinsam.pfade import istNurLesbar, nurLesbar

pfadsperren = (
    (
        istNurLesbar,
        f"Dieser Pfad ist nur lesbar, für alle Rollen und den Koordinator: {', '.join(nurLesbar)}. "
        "Löschen und ändern tut nur der Stakeholder.",
    ),
)
