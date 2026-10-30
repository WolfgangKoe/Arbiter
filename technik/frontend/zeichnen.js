import { armeeKarte } from "./komponenten/armeeKarte.js"
import { karte } from "./komponenten/karte.js"
import { kopfzeile } from "./komponenten/kopfzeile.js"
import { protokoll } from "./komponenten/protokoll.js"
import { ausVorlage } from "./komponenten/vorlage.js"

function spalte(inhalt) {
  const neu = ausVorlage("spalte")
  neu.append(inhalt)
  return neu
}

export function zeichnen(spielstand, gründe, knöpfe) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  document.querySelector(".kopfzeile").replaceChildren(...kopfzeile(spielstand))
  document.querySelector(".spielbereich").replaceChildren(
    spalte(armeeKarte(ersterSpieler, knöpfe.armee)),
    karte(spielstand, gründe, knöpfe.mitte),
    spalte(armeeKarte(zweiterSpieler, knöpfe.armee)),
  )
  document.querySelector(".leisteUnten .leistenInhalt").replaceChildren(
    protokoll(spielstand.schlacht?.protokoll ?? []),
  )
}
