// GTA 6 meme on X (v4) — entry program.
// Copies POST.json, which names the X post carrying the meme, to the
// output directory, byte for byte. Node 22, standard library only.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

const src = join(botDir, "POST.json");
if (!existsSync(src)) {
  console.error(`POST.json not found in ${botDir}`);
  process.exit(1);
}

// Validate before copying: POST.json must name a real X post URL.
let post;
try {
  post = JSON.parse(readFileSync(src, "utf8"));
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}
if (typeof post.url !== "string" || !post.url.startsWith("https://x.com/")) {
  console.error("POST.json has no valid X post URL");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "POST.json"));
console.log(`POST.json copied to ${outDir}`);
