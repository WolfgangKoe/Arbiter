import { ausSvgVorlage, flächeSetzen, mitSpieler } from "./vorlage.js"

function kreis(daten) {
  const neu = ausSvgVorlage("grenzeKreis")
  neu.setAttribute("cx", daten.x)
  neu.setAttribute("cy", daten.y)
  neu.setAttribute("r", daten.radius)
  return neu
}

export function grenze(eintrag, nummer, { breite, länge }) {
  const kennung = `grenze-${nummer}`
  const maske = ausSvgVorlage("grenzeMaske")
  maske.setAttribute("id", kennung)
  for (const fläche of [maske, maske.querySelector("rect")]) {
    flächeSetzen(fläche, { x: 0, y: 0, breite, länge })
  }
  maske.append(...eintrag.kreise.map(kreis))
  const gruppe = mitSpieler(ausSvgVorlage("grenze"), eintrag.spieler)
  gruppe.setAttribute("mask", `url(#${kennung})`)
  gruppe.classList.toggle("nahkampfreichweite", Boolean(eintrag.nahkampfreichweite))
  gruppe.classList.toggle("wählbar", Boolean(eintrag.wählbar))
  gruppe.append(...eintrag.kreise.map(kreis))
  return [maske, gruppe]
}
