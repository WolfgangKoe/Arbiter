"""Hook: Eine Rolle schreibt nur in ihren Schreibpfaden; manche Pfade sind für alle nur lesbar."""

from pathlib import Path

from gemeinsam.gitAufruf import geänderteDateien, kopfCommit
from gemeinsam.hookProtokoll import (
    HookEingabe,
    antwortAusgeben,
    eingabeLesen,
    verweigerung,
    zusatzkontext,
)
from gemeinsam.pfade import istNurLesbar, nurLesbar, projektordner
from lesen.agenten import darfSchreiben, schreibpfade

schreibwerkzeuge = ("Write", "Edit", "NotebookEdit")
kopfPräfix = "HEAD "


def standDatei(wurzel: Path, agentId: str) -> Path:
    return wurzel / ".git" / "arbiter-schreibgrenze" / f"{agentId}.txt"


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


def beimStart(eingabe: HookEingabe, wurzel: Path) -> dict:
    datei = standDatei(wurzel, eingabe.agentId)
    datei.parent.mkdir(parents=True, exist_ok=True)
    zeilen = [f"{kopfPräfix}{kopfCommit(wurzel)}", *sorted(geänderteDateien(wurzel))]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
    muster = schreibpfade(eingabe.rolle or "", wurzel)
    return zusatzkontext(
        "SubagentStart",
        "Deine Schreibpfade: "
        + (", ".join(muster) if muster else "keine, du schreibst nichts")
        + f". Für alle nur lesbar: {', '.join(nurLesbar)}.",
    )


def beimEnde(eingabe: HookEingabe, wurzel: Path) -> dict | None:
    datei = standDatei(wurzel, eingabe.agentId)
    zeilen = datei.read_text(encoding="utf-8").splitlines() if datei.exists() else []
    datei.unlink(missing_ok=True)
    kopfVorher = next(
        (zeile.removeprefix(kopfPräfix) for zeile in zeilen if zeile.startswith(kopfPräfix)), None
    )
    vorher = {zeile for zeile in zeilen if not zeile.startswith(kopfPräfix)}
    rolle = eingabe.rolle
    muster = schreibpfade(rolle, wurzel)
    meldungen = []
    verstöße = sorted(
        pfad
        for pfad in geänderteDateien(wurzel) - vorher
        if istNurLesbar(pfad) or not darfSchreiben(pfad, muster)
    )
    if verstöße:
        meldungen.append(
            f"Schreibgrenze verletzt: {rolle} hat außerhalb seiner Schreibpfade oder in nur "
            f"lesbaren Pfaden geändert: {', '.join(verstöße)}."
        )
    if kopfVorher is not None and kopfCommit(wurzel) != kopfVorher:
        meldungen.append(
            f"Während {rolle} lief, kam ein Commit hinzu. Hast du ihn nicht selbst gemacht, "
            f"hat {rolle} committet; das ist dem Koordinator vorbehalten."
        )
    if not meldungen:
        return None
    return zusatzkontext(
        "SubagentStop", " ".join(meldungen) + " Nicht committen, dem Stakeholder melden."
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if eingabe.ereignis == "PreToolUse":
        return vorDemSchreiben(eingabe, wurzel)
    if eingabe.ereignis == "SubagentStart" and eingabe.agentId:
        return beimStart(eingabe, wurzel)
    if eingabe.ereignis == "SubagentStop" and eingabe.agentId:
        return beimEnde(eingabe, wurzel)
    return None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
