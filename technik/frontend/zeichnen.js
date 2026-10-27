function ausVorlage(name) {
  return document.getElementById(name).content.firstElementChild.cloneNode(true)
}

function ausSvgVorlage(name) {
  return ausVorlage(name).firstElementChild
}

function mitSpieler(element, nummer) {
  element.classList.replace("spieler1", nummer === null ? "ohneSpieler" : `spieler${nummer}`)
  return element
}

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

function kopfzeile(spielstand) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  return [
    kopfzeilenSpieler(ersterSpieler, spielstand.schlacht),
    kopfzeilenTitel(spielstand.schlacht),
    kopfzeilenSpieler(zweiterSpieler, spielstand.schlacht),
  ]
}

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

function armeeKarte(spieler, knöpfe) {
  const karte = mitSpieler(ausVorlage("armeeKarte"), spieler.nummer)
  karte.querySelector(".armeeKartenName").textContent = spieler.name
  karte.dataset.spieler = spieler.nummer
  if (knöpfe.length > 0) karte.append(knopfGruppe(knöpfe, spieler.nummer))
  karte.append(...spieler.armeeliste.map(einheit => einheitenKarte(spieler, einheit)))
  return karte
}

function spalte(inhalt) {
  const neu = ausVorlage("spalte")
  neu.append(inhalt)
  return neu
}

function flächeSetzen(element, { x, y, breite, länge }) {
  element.setAttribute("x", x)
  element.setAttribute("y", y)
  element.setAttribute("width", breite)
  element.setAttribute("height", länge)
}

function sperrmeldung(gründe) {
  const liste = ausVorlage("sperrmeldung")
  for (const grund of gründe) {
    const eintrag = ausVorlage("sperrmeldungGrund")
    eintrag.textContent = grund
    liste.append(eintrag)
  }
  return liste
}

function knopf(spielernummer, { text, handlung }) {
  const neu = ausVorlage("knopf")
  neu.textContent = text
  neu.addEventListener("click", handlung.bind(null, spielernummer))
  return neu
}

function knopfGruppe(knöpfe, spielernummer) {
  const gruppe = ausVorlage("knopfGruppe")
  gruppe.append(...knöpfe.map(knopf.bind(null, spielernummer)))
  return gruppe
}

function modellKreis(modell) {
  const kreis = mitSpieler(ausSvgVorlage("modell"), modell.spieler)
  kreis.setAttribute("cx", modell.x)
  kreis.setAttribute("cy", modell.y)
  kreis.setAttribute("r", modell.radius)
  kreis.classList.toggle("ausgewählt", modell.ausgewählt)
  if (modell.ebene) kreis.dataset.ebene = "ja"
  Object.assign(kreis.dataset, { spieler: modell.spieler, einheit: modell.einheit, nummer: modell.nummer })
  return kreis
}

function karte(spielstand, gründe, knöpfe) {
  const { breite, länge } = spielstand.spielfeld
  const mitte = ausVorlage("karte")
  const zeichnung = mitte.querySelector(".karte")
  zeichnung.setAttribute("viewBox", `0 0 ${breite} ${länge}`)
  flächeSetzen(zeichnung.querySelector(".spielfeld"), { x: 0, y: 0, breite, länge })
  for (const zone of spielstand.zonen) {
    const fläche = mitSpieler(ausSvgVorlage("aufstellungszone"), zone.spieler)
    flächeSetzen(fläche, zone)
    zeichnung.append(fläche)
  }
  zeichnung.append(...spielstand.modelle.map(modellKreis))
  if (gründe.length > 0) mitte.append(sperrmeldung(gründe))
  if (knöpfe.length > 0) mitte.append(knopfGruppe(knöpfe))
  return mitte
}

export function zeichnen(spielstand, gründe, knöpfe) {
  const [ersterSpieler, zweiterSpieler] = spielstand.spieler
  document.querySelector(".kopfzeile").replaceChildren(...kopfzeile(spielstand))
  document.querySelector(".spielbereich").replaceChildren(
    spalte(armeeKarte(ersterSpieler, knöpfe.armee)),
    karte(spielstand, gründe, knöpfe.mitte),
    spalte(armeeKarte(zweiterSpieler, knöpfe.armee)),
  )
}
