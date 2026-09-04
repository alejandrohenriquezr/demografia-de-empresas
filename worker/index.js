const page = "__PAGE__";
const client = "__CLIENT__";
const xlsx = "__XLSX__";
const documents = __DOCUMENTS__;
const assets = __ASSETS__;

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    if (path === "/xlsx") return new Response(xlsx, { headers: { "content-type": "application/javascript; charset=utf-8", "cache-control": "public, max-age=31536000, immutable" } });
    if (path === "/client-dynamic") return new Response(client, { headers: { "content-type": "application/javascript; charset=utf-8", "cache-control": "no-store" } });
    if (path.startsWith("/assets/")) { const item = assets[path.slice("/assets/".length)]; if (!item) return new Response("No encontrado", { status: 404 }); const bytes = Uint8Array.from(atob(item.body), c => c.charCodeAt(0)); return new Response(bytes, { headers: { "content-type": item.type, "cache-control": "public, max-age=31536000, immutable" } }); }
    if (path.startsWith("/datos_OE/")) {
      const item = documents[path.slice(1)];
      if (!item) return new Response("No encontrado", { status: 404 });
      const bytes = Uint8Array.from(atob(item.body), c => c.charCodeAt(0));
      return new Response(bytes, { headers: { "content-type": item.type, "content-disposition": "attachment; filename*=UTF-8''" + encodeURIComponent(item.name), "cache-control": "public, max-age=3600" } });
    }
    if (path !== "/") return new Response("No encontrado", { status: 404 });
    return new Response(page, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
  },
};

