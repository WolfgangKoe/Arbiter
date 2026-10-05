import kommentare from "./prozess/pruefungen/frontendregeln/eslintKommentare.mjs";

// Regel: prozess/praemissen/wir.md 1, 5, 8 und prozess/ablauf.md (Werkzeuge) für technik/frontend/.
const meldung = "Markup aus einer <template> der Seite klonen (Architektur, Web, O1)";
const verboteneAufrufe = ["createElement", "createElementNS", "write"].map((property) => ({
  object: "document",
  property,
  message: meldung,
}));
const verboteneSyntax = [
  {selector: "AssignmentExpression[left.property.name=/^(innerHTML|outerHTML)$/]", message: meldung},
  {selector: "CallExpression[callee.property.name='insertAdjacentHTML']", message: meldung},
];

export default [
  {
    files: ["technik/frontend/**/*.js"],
    languageOptions: {ecmaVersion: 2024, sourceType: "module"},
    plugins: {arbiter: {rules: {kommentare}}},
    rules: {
      camelcase: ["error", {properties: "always"}],
      "id-length": ["error", {min: 3, exceptions: ["x", "y"]}],
      "no-var": "error",
      "prefer-const": "error",
      eqeqeq: "error",
      "no-unused-vars": "error",
      complexity: ["error", 15],
      "no-restricted-properties": ["error", ...verboteneAufrufe],
      "no-restricted-syntax": ["error", ...verboteneSyntax],
      "arbiter/kommentare": "error",
    },
  },
];
