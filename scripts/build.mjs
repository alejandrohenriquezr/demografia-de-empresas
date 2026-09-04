import { mkdir, readFile, rm, writeFile, copyFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const [template, client, worker, xlsx] = await Promise.all([
  readFile(resolve(root, "index.html"), "utf8"),
  readFile(resolve(root, "worker/client.js"), "utf8"),
  readFile(resolve(root, "worker/index.js"), "utf8"),
  readFile(resolve(root, "worker/vendor/xlsx.full.min.js"), "utf8"),
]);
const typeFor = (name) => name.endsWith(".pdf") ? "application/pdf" : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const readDocuments = async (directory, prefix = "") => {
  const entries = await readdir(directory, { withFileTypes: true });
  const records = await Promise.all(entries.map(async (entry) => {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    const absolute = resolve(directory, entry.name);
    if (entry.isDirectory()) return readDocuments(absolute, relative);
    const contents = await readFile(absolute);
    return { [`datos_OE/${relative}`]: { name: entry.name, type: typeFor(entry.name), body: contents.toString("base64") } };
  }));
  return Object.assign({}, ...records);
};
const documents = await readDocuments(resolve(root, "datos_OE"));
const assetNames = ["logo-ine.jpg", "logo-rue.jpg"];
const assets = Object.fromEntries(await Promise.all(assetNames.map(async (name) => [name, { type: "image/jpeg", body: (await readFile(resolve(root, "assets", name))).toString("base64") }])));
const html = template
  // The supplied mockup does not include SheetJS.  Load the vendored reader
  // before any page script and before the dynamic data client executes.
  .replace("</head>", '<script src="/xlsx"></script></head>')
  .replace("</body>", '<script src="/client-dynamic"></script></body>');
const literal = (value) => JSON.stringify(value).replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");
const output = worker
  .replace('"__PAGE__"', () => literal(html))
  .replace('"__CLIENT__"', () => literal(client))
  .replace('"__XLSX__"', () => literal(xlsx))
  .replace("__ASSETS__", () => literal(assets))
  .replace("__DOCUMENTS__", () => literal(documents));
await rm(resolve(root, "dist"), { recursive: true, force: true });
await mkdir(resolve(root, "dist/server"), { recursive: true });
await mkdir(resolve(root, "dist/.openai"), { recursive: true });
await writeFile(resolve(root, "dist/server/index.js"), output);
await copyFile(resolve(root, ".openai/hosting.json"), resolve(root, "dist/.openai/hosting.json"));

