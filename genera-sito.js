// Costruisce la cartella _site/ con la pagina web e una copia dei PDF del progetto.
// La struttura del progetto NON viene modificata: i PDF vengono copiati (non spostati).
// Ogni cartella di primo livello (es. "TPS - 3 info") diventa una sezione della pagina.
// Uso: node genera-sito.js

const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const OUT = path.join(ROOT, "_site");

// Cartelle ignorate a qualsiasi profondità (per nome).
const CARTELLE_ESCLUSE = new Set([
    ".git", "node_modules", "_site", "web",
    "generate", "scripts", "chapter_images",
]);

// File PDF da NON pubblicare (espressioni regolari sul nome del file).
// Esempio per nascondere le soluzioni:  [/SOLUTION/i]
const ESCLUDI_FILE = [/SOLUTION/i];

const SEZIONE_DEFAULT = "Altri file";

function dimensione(byte) {
    if (byte < 1024 * 1024) return Math.max(1, Math.round(byte / 1024)) + " KB";
    return (byte / (1024 * 1024)).toFixed(1).replace(".", ",") + " MB";
}

function scansiona(dir, out = []) {
    for (const voce of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, voce.name);
        if (voce.isDirectory()) {
        if (!CARTELLE_ESCLUSE.has(voce.name)) scansiona(p, out);
        } else if (/\.pdf$/i.test(voce.name) && !ESCLUDI_FILE.some((re) => re.test(voce.name))) {
        out.push(p);
        }
    }
    return out;
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const files = scansiona(ROOT).map((p) => {
    const rel = path.relative(ROOT, p).split(path.sep);
    const dest = path.join(OUT, ...rel);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(p, dest);
    return {
        category: rel.length > 1 ? rel[0] : SEZIONE_DEFAULT,
        title: rel[rel.length - 1].replace(/\.pdf$/i, "").replace(/_+/g, " ").trim(),
        url: rel.map(encodeURIComponent).join("/"),
        size: dimensione(fs.statSync(p).size),
    };
});

const collator = new Intl.Collator("it", { numeric: true, sensitivity: "base" });
files.sort((a, b) => collator.compare(a.category, b.category) || collator.compare(a.title, b.title));

fs.copyFileSync(path.join(ROOT, "web", "index.html"), path.join(OUT, "index.html"));
fs.writeFileSync(
    path.join(OUT, "pdfs.json"),
    JSON.stringify({ generated: new Date().toISOString(), files }, null, 2)
);

console.log(`Sito generato in _site/ con ${files.length} PDF:`);
files.forEach((f) => console.log(`  [${f.category}] ${f.title}`));