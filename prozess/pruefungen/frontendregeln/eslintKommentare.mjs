// Regel: prozess/praemissen/es.md 8: Kommentare nur einzeilig als `// Regel:` oder `// Warum:`.
const erlaubterKommentar = /^ (Regel|Warum): \S/;
const werkzeugkommentar = /^\s*(eslint|global|globals|exported)\b/;
const offenerPunkt = /\b(TODO|FIXME)\b/;

function verstoßGrund(kommentar) {
  if (offenerPunkt.test(kommentar.value)) {
    return "offenerPunkt";
  }
  if (werkzeugkommentar.test(kommentar.value)) {
    return null;
  }
  const istErlaubt = kommentar.type === "Line" && erlaubterKommentar.test(kommentar.value);
  return istErlaubt ? null : "form";
}

export default {
  meta: {
    type: "suggestion",
    schema: [],
    messages: {
      form: "Kommentar nur einzeilig als `// Regel: …` oder `// Warum: …`",
      offenerPunkt: "Kein TODO oder FIXME",
    },
  },
  create(kontext) {
    return {
      Program() {
        for (const kommentar of kontext.sourceCode.getAllComments()) {
          const grund = verstoßGrund(kommentar);
          if (grund) {
            kontext.report({loc: kommentar.loc, messageId: grund});
          }
        }
      },
    };
  },
};
