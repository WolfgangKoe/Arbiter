// Warum: Die Suche liest die Dateien selbst, denn Pylance fand beim Stakeholder nichts.
const fs = require("fs");
const path = require("path");

const kriteriumMuster = /[A-ZÄÖÜ]+-\d+\.\d+/;
const testMuster = /test[A-ZÄÖÜ][a-zäöüß]*\d+_\d+[\wÄÖÜäöüß]*/;
const testKriteriumMuster = /^test([A-ZÄÖÜ][a-zäöüß]*)(\d+)_(\d+)/;

function dateien(ordner, endung) {
  if (!fs.existsSync(ordner)) return [];
  return fs.readdirSync(ordner, { withFileTypes: true }).flatMap((eintrag) => {
    const pfad = path.join(ordner, eintrag.name);
    if (eintrag.isDirectory()) return eintrag.name === "__pycache__" ? [] : dateien(pfad, endung);
    return pfad.endsWith(endung) ? [pfad] : [];
  });
}

function stellen(ordner, endung, muster) {
  const gefunden = [];
  for (const datei of dateien(ordner, endung)) {
    fs.readFileSync(datei, "utf8").split("\n").forEach((text, zeile) => {
      const treffer = muster.exec(text);
      if (treffer) gefunden.push({ datei, zeile, spalte: treffer.index });
    });
  }
  return gefunden;
}

function testsZu(wurzel, kriterium) {
  const [, kürzel, anforderung, nummer] = /^([A-ZÄÖÜ]+)-(\d+)\.(\d+)$/.exec(kriterium);
  const name = kürzel[0] + kürzel.slice(1).toLowerCase();
  const muster = new RegExp(`def (test${name}${anforderung}_${nummer})(?!\\d)`, "i");
  return stellen(path.join(wurzel, "technik/tests/akzeptanz"), ".py", muster);
}

function kriteriumZu(wurzel, testName) {
  const [, name, anforderung, nummer] = testKriteriumMuster.exec(testName);
  const muster = new RegExp(`^- ${name.toUpperCase()}-${anforderung}\\.${nummer}(?!\\d)`);
  return stellen(path.join(wurzel, "domaene/anforderungen"), ".md", muster);
}

module.exports = { kriteriumMuster, testMuster, testsZu, kriteriumZu };
