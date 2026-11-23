// Entrypoint for the gta6-meme-x-01 bounty entry (Node 22, stdlib only).
// The judging for this bounty happens on X, not in this container: the
// meme image is posted from a public account, and POST.json in the repo
// root names that post. This program has exactly one job — hand that file
// to the gate by placing an identical copy at /output/POST.json. Before
// copying it checks the file is a JSON object carrying a string url, so a
// malformed POST.json fails here with a plain message instead of reaching
// the gate and failing there.
// Outside the grader, the two directories can be pointed elsewhere:
//   mkdir -p /tmp/mf-out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=/tmp/mf-out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join as joinPath } from "node:path";

function dirFromEnv(name: string, fallback: string): string {
  const value = process.env[name];
  if (value === undefined || value === "") {
    return fallback;
  }
  return value;
} // dirFromEnv

function loadPost(location: string): Buffer {
  if (!existsSync(location)) {
    throw new Error(`no POST.json found at ${location}`);
  }
  const raw = readFileSync(location);
  const parsed: unknown = JSON.parse(raw.toString("utf8"));
  if (typeof parsed !== "object" || parsed === null) {
    throw new Error("POST.json is not a JSON object");
  }
  const url = (parsed as { url?: unknown }).url;
  if (typeof url !== "string") {
    throw new Error('POST.json has no string "url" field');
  }
  return raw;
} // loadPost

const repoRoot = dirFromEnv("MAKEFUN_BOT_DIR", "/bot");
const outRoot = dirFromEnv("MAKEFUN_OUTPUT_DIR", "/output");
const source = joinPath(repoRoot, "POST.json");
const target = joinPath(outRoot, "POST.json");

function deliver(): void {
  const contents = loadPost(source);
  mkdirSync(outRoot, { recursive: true });
  writeFileSync(target, contents);
} // deliver

try { // Deliver POST.json, or fail with a message.
  deliver();
} catch (problem) {
  console.error(`cannot deliver POST.json: ${(problem as Error).message}`);
  process.exitCode = 1;
} // deliver attempt
