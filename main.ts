import { copyFile, mkdir, readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

// Copies POST.json from the repository root (the bot directory) into the
// output directory so the make.fun runner can find the X post URL.
const botDir = resolve(process.env.MAKEFUN_BOT_DIR ?? "/bot");
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

const source = join(botDir, "POST.json");
const destination = join(outputDir, "POST.json");

try {
  // Fail fast on a missing or malformed POST.json instead of copying garbage.
  const raw = await readFile(source, "utf8");
  const parsed = JSON.parse(raw) as unknown;
  if (
    typeof parsed !== "object" ||
    parsed === null ||
    !("url" in parsed) ||
    typeof parsed.url !== "string" ||
    parsed.url.length === 0
  ) {
    throw new Error("POST.json must be a JSON object with a non-empty \"url\" string");
  }
  await mkdir(outputDir, { recursive: true });
  await copyFile(source, destination);
  console.log(`Copied ${source} to ${destination}`);
} catch (error) {
  console.error(`Failed to copy ${source} to ${destination}: ${error}`);
  process.exit(1);
}
