"""Hook (PreToolUse): Eine Rolle schreibt nur in ihren Schreibpfaden; manches ist nur lesbar."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import istNurLesbar, projektordner
from lesen.agenten import darfSchreiben, schreibpfade

schreibwerkzeuge = ("Write", "Edit", "NotebookEdit")


def vorDemSchreiben(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    # Warum: Ohne Rolle spricht die Hauptsitzung, für sie gilt keine Grenze.
    rolle = eingabe.rolle
    if not rolle or eingabe.werkzeug not in schreibwerkzeuge:
        return None
    angaben = eingabe.angaben
    ziel = Path(angaben.get("file_path") or angaben.get("notebook_path") or "")
    ziel = (wurzel / ziel).resolve() if not ziel.is_absolute() else ziel.resolve()
    if ziel.is_relative_to(wurzel):
        relativ = ziel.relative_to(wurzel).as_posix()
        if istNurLesbar(relativ):
            return verweigerung(
                f"Schreibgrenze: {relativ} ist nur lesbar, für alle Rollen und den Koordinator. "
                "Löschen und ändern tut nur der Stakeholder."
            )
        if darfSchreiben(relativ, schreibpfade(rolle, wurzel)):
            return None
    else:
        relativ = str(ziel)
    return verweigerung(
        f"Schreibgrenze: {rolle} darf {relativ} nicht schreiben. "
        "Kritik an fremden Artefakten wird ein Anliegen."
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    return vorDemSchreiben(eingabe, wurzel) if eingabe.ereignis == "PreToolUse" else None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
