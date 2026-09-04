import { createWriteStream } from "node:fs";
import { mkdir, rm } from "node:fs/promises";
import { resolve } from "node:path";
import { pipeline } from "node:stream/promises";
import { createGunzip } from "node:zlib";
import { spawn } from "node:child_process";

const root = resolve(import.meta.dirname, "..");
const target = resolve(root, "datos_OE");
const url = process.env.DATA_BUNDLE_URL;
if (!url) throw new Error("Falta DATA_BUNDLE_URL: URL HTTPS del ZIP de datos institucionales.");
if (!url.startsWith("https://")) throw new Error("DATA_BUNDLE_URL debe usar HTTPS.");

const headers = process.env.DATA_BUNDLE_TOKEN
  ? { Authorization: `Bearer ${process.env.DATA_BUNDLE_TOKEN}` }
  : {};
const response = await fetch(url, { headers });
if (!response.ok || !response.body) throw new Error(`No se pudo descargar el paquete de datos (HTTP ${response.status}).`);

const tmp = resolve(root, "data-bundle-download.zip");
await pipeline(response.body, createWriteStream(tmp));
await mkdir(target, { recursive: true });

await new Promise((resolvePromise, reject) => {
  const child = spawn("unzip", ["-o", tmp, "-d", target], { stdio: "inherit" });
  child.on("error", reject);
  child.on("exit", code => code === 0 ? resolvePromise() : reject(new Error(`unzip terminó con código ${code}`)));
});
await rm(tmp, { force: true });
console.log("Paquete de datos descargado y extraído.");
