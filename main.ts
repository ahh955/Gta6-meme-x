// Gta6-meme-x entry program.
//
// Copies POST.json (the X post address for this entry) into /output.
// Node standard library only, no network, no wall clock: two runs write
// the same bytes, because this is a byte-for-byte copy.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, "POST.json");
const outDir = "/output";
const target = join(outDir, "POST.json");

if (!existsSync(source)) {
  console.error(
    "POST.json is not in the repository root yet: the X post has not been made."
  );
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`Copied POST.json to ${target}`);
