import { ausVorlage, mitSpieler } from "./vorlage.js"

function amZugAnzeigen(feld, schlacht) {
  const anzeige = ausVorlage("kopfzeileAmZug")
  anzeige.textContent = `Schlachtrunde ${schlacht.schlachtrunde} · ${schlacht.phase}`
  feld.classList.add("amZug")
  feld.append(anzeige)
}

function kopfzeilenSpieler(spieler, schlacht) {
  const feld = mitSpieler(ausVorlage("kopfzeileSpieler"), spieler.nummer)
  feld.firstChild.nodeValue = spieler.name
  if (!spieler.anDerReihe) {
    feld.classList.remove("anDerReihe")
    feld.querySelector(".kopfzeileAnDerReihe").remove()
  }
  if (schlacht?.amZug === spieler.nummer) amZugAnzeigen(feld, schlacht)
  return feld
}

function kopfzeilenTitel(schlacht) {
  const titel = ausVorlage("kopfzeileTitel")
  if (schlacht?.beendet) titel.append(ausVorlage("kopfzeileSchlachtBeendet"))
  return titel
}

export function kopfzeile(spielstand) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  return [
    kopfzeilenSpieler(ersterSpieler, spielstand.schlacht),
    kopfzeilenTitel(spielstand.schlacht),
    kopfzeilenSpieler(zweiterSpieler, spielstand.schlacht),
  ]
}
