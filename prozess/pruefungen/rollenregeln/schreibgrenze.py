"""Hook (PreToolUse): Eine Rolle schreibt nur in ihren Schreibpfaden; manches ist nur lesbar."""

from pathlib import Path

from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, verweigerung
from gemeinsam.pfade import projektordner, relativZurWurzel
from lesen.agenten import darfSchreiben, schreibpfade
from rollenregeln.pfadsperren import pfadsperren

schreibwerkzeuge = ("Write", "Edit")


def vorDemSchreiben(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    # Warum: Ohne Rolle spricht die Hauptsitzung, für sie gilt keine Grenze.
    rolle = eingabe.rolle
    if not rolle or eingabe.werkzeug not in schreibwerkzeuge:
        return None
    angaben = eingabe.angaben
    ziel = Path(angaben.get("file_path") or "")
    relativ = relativZurWurzel(ziel, wurzel)
    if relativ is None:
        relativ = str(ziel)
    for gesperrt, meldung in pfadsperren:
        if gesperrt(relativ):
            return verweigerung(f"Schreibgrenze: {relativ}: {meldung}")
    if darfSchreiben(relativ, schreibpfade(rolle, wurzel)):
        return None
    return verweigerung(
        f"Schreibgrenze: {rolle} darf {relativ} nicht schreiben. "
        "Kritik an fremden Artefakten wird ein Anliegen."
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    return vorDemSchreiben(eingabe, wurzel) if eingabe.ereignis == "PreToolUse" else None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
