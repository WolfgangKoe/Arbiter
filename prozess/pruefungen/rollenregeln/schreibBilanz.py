"""Hook (SubagentStart, SubagentStop): legt Änderungen außerhalb der Schreibpfade ab."""

from pathlib import Path

from gemeinsam.gitAufruf import geänderteDateien, kopfCommit
from gemeinsam.hookProtokoll import HookEingabe, antwortAusgeben, eingabeLesen, zusatzkontext
from gemeinsam.pfade import istNurLesbar, nurLesbar, projektordner
from lesen.agenten import darfSchreiben, schreibpfade
from rollenregeln.angefasstePfade import AngefasstePfade

kopfPräfix = "HEAD "


def standDatei(wurzel: Path, agentId: str) -> Path:
    return wurzel / ".git" / "arbiter-schreibgrenze" / f"{agentId}.txt"


def meldungsOrdner(wurzel: Path) -> Path:
    return wurzel / ".git" / "arbiter-meldungen"


def beimStart(eingabe: HookEingabe, wurzel: Path) -> dict:
    datei = standDatei(wurzel, eingabe.agentId)
    datei.parent.mkdir(parents=True, exist_ok=True)
    zeilen = [f"{kopfPräfix}{kopfCommit(wurzel)}", *sorted(geänderteDateien(wurzel))]
    datei.write_text("\n".join(zeilen), encoding="utf-8")
    muster = schreibpfade(eingabe.rolle, wurzel)
    return zusatzkontext(
        "SubagentStart",
        "Deine Schreibpfade: "
        + (", ".join(muster) if muster else "keine, du schreibst nichts")
        + f". Für alle nur lesbar: {', '.join(nurLesbar)}.",
    )


def pfadMeldungen(eingabe: HookEingabe, wurzel: Path, vorher: set[str]) -> list[str]:
    """Meldungen zu Änderungen außerhalb der Schreibpfade, getrennt nach Anfassen der Rolle."""
    rolle = eingabe.rolle
    muster = schreibpfade(rolle, wurzel)
    außerhalb = sorted(
        pfad
        for pfad in geänderteDateien(wurzel) - vorher
        if istNurLesbar(pfad) or not darfSchreiben(pfad, muster)
    )
    angefasst = AngefasstePfade(eingabe.rollenTranskript, wurzel)
    verstöße = [pfad for pfad in außerhalb if angefasst.enthält(pfad)]
    unklar = [pfad for pfad in außerhalb if pfad not in verstöße]
    meldungen = []
    if verstöße:
        meldungen.append(
            f"Schreibgrenze verletzt: {rolle} hat außerhalb seiner Schreibpfade oder in nur "
            f"lesbaren Pfaden geändert: {', '.join(verstöße)}."
        )
    if unklar:
        meldungen.append(
            f"Während {rolle} lief, änderte sich außerhalb seiner Schreibpfade, ohne dass er die "
            f"Pfade angefasst hat (unklar, wer): {', '.join(unklar)}."
        )
    return meldungen


def beimEnde(eingabe: HookEingabe, wurzel: Path) -> None:
    datei = standDatei(wurzel, eingabe.agentId)
    zeilen = datei.read_text(encoding="utf-8").splitlines() if datei.exists() else []
    datei.unlink(missing_ok=True)
    kopfVorher = next(
        (zeile.removeprefix(kopfPräfix) for zeile in zeilen if zeile.startswith(kopfPräfix)), None
    )
    vorher = {zeile for zeile in zeilen if not zeile.startswith(kopfPräfix)}
    rolle = eingabe.rolle
    meldungen = pfadMeldungen(eingabe, wurzel, vorher)
    if kopfVorher is not None and kopfCommit(wurzel) != kopfVorher:
        meldungen.append(
            f"Während {rolle} lief, kam ein Commit hinzu. Hast du ihn nicht selbst gemacht, "
            f"hat {rolle} committet; das ist dem Koordinator vorbehalten."
        )
    if not meldungen:
        return
    # Warum: Der Kontext eines SubagentStop erreicht nur die Rolle; `schreibMeldung` liefert ihn.
    ordner = meldungsOrdner(wurzel)
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / f"{eingabe.agentId}.txt").write_text(
        " ".join(meldungen) + " Nicht committen, dem Stakeholder melden.", encoding="utf-8"
    )


def entscheide(daten: dict, wurzel: Path) -> dict | None:
    eingabe = HookEingabe.aus(daten)
    if eingabe.ereignis == "SubagentStart" and eingabe.agentId and eingabe.rolle:
        return beimStart(eingabe, wurzel)
    if eingabe.ereignis == "SubagentStop" and eingabe.agentId and eingabe.rolle:
        beimEnde(eingabe, wurzel)
    return None


if __name__ == "__main__":
    antwortAusgeben(entscheide(eingabeLesen(), projektordner()))
