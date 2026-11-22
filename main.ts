// GTA 6 meme on X (v6) -- entry program.
// The meme itself lives in meme.png (posted on X by the user); this
// program hands the grader the post's address. It reads POST.json,
// checks it names a real X post, and writes it to the output directory
// byte for byte. Node 22, standard library only.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

const postPath = join(botDir, "POST.json");
if (!existsSync(postPath)) {
  console.error(`POST.json not found in ${botDir}`);
  process.exit(1);
}

const raw = readFileSync(postPath, "utf8");
let post;
try {
  post = JSON.parse(raw);
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}
if (typeof post.url !== "string" || !post.url.startsWith("https://x.com/")) {
  console.error("POST.json does not name a real X post URL");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), raw);
console.log(`POST.json written to ${outDir}`);
