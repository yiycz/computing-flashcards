import { defineConfig } from "vite";

// Optional preview of the compiled MkDocs site. GitHub Pages only needs Python.
export default defineConfig({
  root: "site",
  appType: "mpa",
  server: {host: "0.0.0.0", allowedHosts: ["terminal.local"]},
});
