// Anliegen 53, Weg C: Kriterium und Test als Links; das Ziel liefert rueckverfolgung.py.
// Start ohne Installation: code --extensionDevelopmentPath=prozess/pruefungen/sprung .
const { execFileSync } = require("child_process");
const vscode = require("vscode");

const orte = [
  { sprache: "markdown", ordner: "domaene/anforderungen/", muster: /\b[A-ZÄÖÜ]+-\d+\.\d+\b/g, ziel: "Test" },
  { sprache: "python", ordner: "technik/tests/akzeptanz/", muster: /\btest[A-ZÄÖÜ][a-zäöüß]*\d+_\d+/g, ziel: "Kriterium" },
];

function treffer(text, muster) {
  return [...text.matchAll(muster)].map((t) => ({ eingabe: t[0], index: t.index }));
}

function links(dokument) {
  const pfad = vscode.workspace.asRelativePath(dokument.uri);
  const ort = orte.find((o) => o.sprache === dokument.languageId && pfad.startsWith(o.ordner));
  if (!ort) return [];
  return treffer(dokument.getText(), ort.muster).map((t) => {
    const bereich = new vscode.Range(
      dokument.positionAt(t.index), dokument.positionAt(t.index + t.eingabe.length));
    const link = new vscode.DocumentLink(bereich);
    link.eingabe = t.eingabe;
    link.ziel = ort.ziel;
    return link;
  });
}

function ziel(link) {
  const wurzel = vscode.workspace.workspaceFolders[0].uri.fsPath;
  const ausgabe = execFileSync(
    "python3", ["prozess/pruefungen/rueckverfolgung.py", link.eingabe, "--json"], { cwd: wurzel });
  const stelle = JSON.parse(ausgabe).find((s) => s.art === link.ziel);
  if (!stelle) return undefined;
  return vscode.Uri.file(`${wurzel}/${stelle.pfad}`).with({ fragment: `L${stelle.zeile}` });
}

function activate(kontext) {
  const anbieter = { provideDocumentLinks: links, resolveDocumentLink: (link) => ((link.target = ziel(link)), link) };
  kontext.subscriptions.push(vscode.languages.registerDocumentLinkProvider(
    [{ language: "markdown" }, { language: "python" }], anbieter));
}

module.exports = { activate, treffer, orte };
