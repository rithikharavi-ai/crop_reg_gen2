#!/usr/bin/env node
/*
 * Correct the master-data geo levels endpoint.
 *
 * The portal's proxy route posts to:
 *
 *     /geo/get_all_g2p_geo_levels
 *
 * but the master-data service pinned by this stack only exposes:
 *
 *     /geo/get_g2p_geo_levels        (and /geo/get_g2p_geo_level_values)
 *
 * so the geo-hierarchy widget fails its first call with "There was an issue
 * fetching data." The values endpoint already matches; only the levels one is
 * wrong. This is a mismatch between two base images, not a config error, so it
 * is corrected here.
 *
 * Exits non-zero if the string is absent, so a base-image update that fixes or
 * renames it fails the build rather than silently leaving a stale patch.
 */
const fs = require("fs");
const path = require("path");

const ROOT = "/app/.next";
const WRONG = "/geo/get_all_g2p_geo_levels";
const RIGHT = "/geo/get_g2p_geo_levels";

function* walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(full);
    else if (entry.name.endsWith(".js")) yield full;
  }
}

let patched = 0;
for (const file of walk(ROOT)) {
  const before = fs.readFileSync(file, "utf8");
  if (!before.includes(WRONG)) continue;
  fs.writeFileSync(file, before.split(WRONG).join(RIGHT));
  patched += 1;
  console.log("  patched " + file.replace(ROOT + "/", ""));
}

if (patched < 1) {
  console.error(
    `geo endpoint patch found no occurrence of ${WRONG} — the base image changed`
  );
  process.exit(1);
}
console.log(`pointed the geo levels call at ${RIGHT} in ${patched} bundle(s)`);
