import { armeeKarte } from "./komponenten/armeeKarte.js"
import { karte } from "./komponenten/karte.js"
import { kopfzeile } from "./komponenten/kopfzeile.js"
import { protokoll } from "./komponenten/protokoll.js"

export function zeichnen(spielstand, gründe, knöpfe) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  document.querySelector(".kopfzeile").replaceChildren(...kopfzeile(spielstand))
  document.querySelector(".leisteLinks .leistenInhalt").replaceChildren(armeeKarte(ersterSpieler, knöpfe.armee))
  document.querySelector(".spalteMitte").replaceWith(karte(spielstand, gründe, knöpfe.mitte))
  document.querySelector(".leisteRechts .leistenInhalt").replaceChildren(armeeKarte(zweiterSpieler, knöpfe.armee))
  document.querySelector(".leisteUnten .leistenInhalt").replaceChildren(
    protokoll(spielstand.schlacht?.protokoll ?? []),
  )
}
