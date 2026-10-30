import { ausVorlage, mitSpieler } from "./vorlage.js"

function eintrag(protokollEintrag) {
  const zeile = mitSpieler(ausVorlage("protokollEintrag"), protokollEintrag.spieler)
  zeile.querySelector(".protokollEinheit").textContent = protokollEintrag.name
  zeile.querySelector(".protokollSpieler").textContent = `Spieler ${protokollEintrag.spieler}`
  for (const grund of protokollEintrag.gründe) {
    const text = ausVorlage("protokollGrund")
    text.textContent = grund
    zeile.append(text)
  }
  return zeile
}

export function protokoll(einträge) {
  const liste = ausVorlage("protokoll")
  liste.append(...einträge.map(eintrag))
  return liste
}
