import { execSync } from "node:child_process";
import { readdirSync, statSync, writeFileSync, mkdirSync } from "node:fs";
import { join, posix, relative } from "node:path";

const ROOT = process.cwd();
const ENTRIES_DIR = join(ROOT, "entries");
const OUT_DIR = join(ROOT, "assets");
const OUT_FILE = join(OUT_DIR, "last-updated.json");

function listMdFiles(dir) {
  const result = [];
  for (const name of readdirSync(dir)) {
    const filePath = join(dir, name);
    const stats = statSync(filePath);
    if (stats.isDirectory()) {
      result.push(...listMdFiles(filePath));
    } else if (name.toLowerCase().endsWith(".md")) {
      result.push(filePath);
    }
  }
  return result;
}

function gitLastCommitInfo(fileAbs) {
  const quotedPath = fileAbs.replace(/"/g, '\\"');
  const dateCmd = `git log -1 --format=%cI -- "${quotedPath}"`;
  const hashCmd = `git log -1 --format=%H -- "${quotedPath}"`;
  try {
    const updated = execSync(dateCmd, {
      stdio: ["ignore", "pipe", "ignore"],
    })
      .toString()
      .trim();
    const commit = execSync(hashCmd, {
      stdio: ["ignore", "pipe", "ignore"],
    })
      .toString()
      .trim();
    return { updated, commit };
  } catch (error) {
    return null;
  }
}

function toRepoPath(absPath) {
  const rel = relative(ROOT, absPath);
  return posix.normalize(rel.split("\\").join("/"));
}

function main() {
  mkdirSync(OUT_DIR, { recursive: true });

  let files = [];
  try {
    files = listMdFiles(ENTRIES_DIR);
  } catch (error) {
    console.error(`无法读取词条目录 ${ENTRIES_DIR}:`, error.message);
    process.exit(1);
  }

  const map = {};
  for (const abs of files) {
    const info = gitLastCommitInfo(abs);
    if (!info) continue;
    const key = toRepoPath(abs);
    map[key] = info;
  }

  const orderedKeys = Object.keys(map).sort();
  const ordered = {};
  for (const key of orderedKeys) {
    ordered[key] = map[key];
  }

  writeFileSync(OUT_FILE, JSON.stringify(ordered, null, 2), "utf8");
  console.log(
    `已写入 ${OUT_FILE}，共记录 ${orderedKeys.length} 个词条的更新时间。`
  );
}

main();
