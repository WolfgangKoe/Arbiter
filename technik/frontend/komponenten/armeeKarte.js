import { knopfGruppe } from "./knopfGruppe.js"
import { ausVorlage, mitSpieler } from "./vorlage.js"

function einheitenKarte(spieler, einheit) {
  const karte = ausVorlage("einheitenKarte")
  karte.classList.toggle("ausgewählt", einheit.ausgewählt)
  Object.assign(karte.dataset, { spieler: spieler.nummer, einheit: einheit.nummer })
  karte.querySelector(".einheitenKartenName span").textContent = einheit.name
  if (einheit.nichtGesetzt > 0) {
    karte.querySelector(".einheitenKartenModelle").textContent = String(einheit.nichtGesetzt)
  } else {
    karte.querySelector(".einheitenKartenModelle").remove()
  }
  return karte
}

export function armeeKarte(spieler, knöpfe) {
  const karte = mitSpieler(ausVorlage("armeeKarte"), spieler.nummer)
  karte.querySelector(".armeeKartenName").textContent = spieler.name
  karte.dataset.spieler = spieler.nummer
  if (knöpfe.length > 0) karte.append(knopfGruppe(knöpfe, spieler.nummer))
  karte.append(...spieler.armeeliste.map(einheit => einheitenKarte(spieler, einheit)))
  return karte
}
