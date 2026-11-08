import { grenze } from "./grenze.js"
import { knopfGruppe } from "./knopfGruppe.js"
import { sperrmeldung } from "./sperrmeldung.js"
import { ausSvgVorlage, ausVorlage, flächeSetzen, mitSpieler } from "./vorlage.js"

function modellKreis(modell) {
  const kreis = mitSpieler(ausSvgVorlage("modell"), modell.spieler)
  kreis.setAttribute("cx", modell.x)
  kreis.setAttribute("cy", modell.y)
  kreis.setAttribute("r", modell.radius)
  kreis.classList.toggle("ausgewählt", modell.ausgewählt)
  if (modell.modellebene) kreis.dataset.modellebene = "ja"
  Object.assign(kreis.dataset, { spieler: modell.spieler, einheit: modell.einheit, nummer: modell.nummer })
  return kreis
}

export function spielfeld(spielstand, gründe, knöpfe) {
  const { breite, länge } = spielstand.spielfeld
  const mitte = ausVorlage("spielfeld")
  const zeichnung = mitte.querySelector(".spielfeld")
  zeichnung.setAttribute("viewBox", `0 0 ${breite} ${länge}`)
  flächeSetzen(zeichnung.querySelector(".spielfläche"), { x: 0, y: 0, breite, länge })
  for (const zone of spielstand.zonen) {
    const fläche = mitSpieler(ausSvgVorlage("aufstellungszone"), zone.spieler)
    flächeSetzen(fläche, zone)
    zeichnung.append(fläche)
  }
  const grenzen = spielstand.schlacht?.grenzen ?? []
  zeichnung.append(...grenzen.flatMap((eintrag, nummer) => grenze(eintrag, nummer, spielstand.spielfeld)))
  zeichnung.append(...spielstand.modelle.map(modellKreis))
  if (gründe.length > 0) mitte.append(sperrmeldung(gründe))
  if (knöpfe.length > 0) mitte.append(knopfGruppe(knöpfe))
  return mitte
}
