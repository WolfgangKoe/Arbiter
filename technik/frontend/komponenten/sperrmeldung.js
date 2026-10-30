import { ausVorlage } from "./vorlage.js"

export function sperrmeldung(gründe) {
  const liste = ausVorlage("sperrmeldung")
  for (const grund of gründe) {
    const eintrag = ausVorlage("sperrmeldungGrund")
    eintrag.textContent = grund
    liste.append(eintrag)
  }
  return liste
}
