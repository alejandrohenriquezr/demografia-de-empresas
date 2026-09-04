import { createHash } from "node:crypto";
import { access, mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import { resolve, relative } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourceDir = resolve(root, "datos_OE/cuadros_estadisticos");
const cacheDir = resolve(root, "dist/cache");
const manifestPath = resolve(cacheDir, "manifest.json");

async function listFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const result = [];
  for (const entry of entries) {
    const absolute = resolve(dir, entry.name);
    if (entry.isDirectory()) result.push(...await listFiles(absolute));
    else if (entry.name.toLowerCase().endsWith(".xlsx")) result.push(absolute);
  }
  return result;
}

async function fingerprint(file) {
  const bytes = await readFile(file);
  const info = await stat(file);
  return {
    file: relative(sourceDir, file).replaceAll("\\\\", "/"),
    sha256: createHash("sha256").update(bytes).digest("hex"),
    size: info.size,
    modified_at: info.mtime.toISOString()
  };
}

await access(sourceDir);
const current = Object.fromEntries((await Promise.all((await listFiles(sourceDir)).map(fingerprint))).map(x => [x.file, x]));
let previous = {};
try { previous = JSON.parse(await readFile(manifestPath, "utf8")).files ?? {}; } catch {}

const changed = Object.keys(current).filter(file => !previous[file] || previous[file].sha256 !== current[file].sha256);
const removed = Object.keys(previous).filter(file => !current[file]);
const hasChanges = changed.length > 0 || removed.length > 0;

await mkdir(cacheDir, { recursive: true });
await writeFile(manifestPath, JSON.stringify({
  generated_at: new Date().toISOString(),
  has_changes: hasChanges,
  changed,
  removed,
  files: current
}, null, 2));

console.log(JSON.stringify({ hasChanges, changed, removed }, null, 2));
if (process.env.CACHE_CHECK_ONLY === "true" && hasChanges) process.exitCode = 2;
