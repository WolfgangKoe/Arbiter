import kommentare from "./prozess/pruefungen/frontendregeln/eslintKommentare.mjs";

// Regel: prozess/praemissen/wir.md 1, 5, 8 und prozess/ablauf.md (Werkzeuge) für technik/frontend/.
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
      "arbiter/kommentare": "error",
    },
  },
];
