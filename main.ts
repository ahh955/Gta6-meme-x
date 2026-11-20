// Entrypoint for the make.fun gta6-meme-x-01 meme entry ("Post a GTA 6
// meme on X"). Node 22 stdlib only.
//
// The grader runs this file; it copies POST.json -- the record of the X
// post carrying the meme -- into the output directory.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "POST.json");

// Validate the input before copying: the grader gets a clear failure
// instead of a half-copied or unreadable POST.json.
if (!existsSync(src)) {
  console.error(`error: ${src} not found (post the meme on X first)`);
  process.exit(1);
}
let post: unknown;
try {
  post = JSON.parse(readFileSync(src, "utf8"));
} catch (err) {
  console.error(`error: ${src} is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== "object" || post === null || Array.isArray(post) ||
    Object.keys(post).length === 0) {
  console.error(`error: ${src} must hold a non-empty JSON object`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "POST.json"));
console.log(`POST.json copied to ${outDir}`);
