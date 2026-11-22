// news-image-20261121 entry runner (Node 22, standard library only).
//
// The entry image lives beside this file as entry.png. Running this program
// checks the image against the competition gate — PNG signature, at most
// 1 MiB, at most 1024x1024 — and copies it to the output directory
// (MAKEFUN_OUTPUT_DIR outside the grader, /output inside it).
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

class GateError extends Error {}

function fail(message) {
  throw new GateError(message);
}

function readPngSize(bytes) {
  // PNG: 8-byte signature, then IHDR chunk (length 4, type 4, then
  // width 4 and height 4, both big-endian).
  if (bytes.length < 33) fail('entry.png is too short to be a PNG');
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail('entry.png does not start with the PNG signature');
  }
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') {
    fail('entry.png has no IHDR chunk where one is expected');
  }
  return {
    width: bytes.readUInt32BE(16),
    height: bytes.readUInt32BE(20),
  };
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, 'entry.png');
  const bytes = readFileSync(source);
  const { width, height } = readPngSize(bytes);
  if (bytes.length > MAX_BYTES) {
    fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, 'entry.png');
  copyFileSync(source, target);
  const written = statSync(target).size;
  if (written !== bytes.length) {
    fail(`copied ${written} bytes but the source has ${bytes.length}`);
  }
  console.log(
    `entry.png ${width}x${height} ${bytes.length} bytes -> ${target}`,
  );
}

main();
