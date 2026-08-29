#!/usr/bin/env node
/*
 * Wrap the master-data geo calls in the envelope this service expects.
 *
 * The portal's proxy posts the body contents at the top level:
 *
 *     { pagination_request: {...}, request_payload: {...} }
 *
 * but the master-data service pinned here requires the G2P envelope:
 *
 *     { request_header: { sender_app_mnemonic, sender_app_url,
 *                         request_id, request_timestamp },
 *       request_body:   { pagination_request, request_payload } }
 *
 * and answers "Invalid Input. Field required" otherwise — which surfaces in the
 * portal as "There was an issue fetching data." on the cascading address
 * widget. This is a contract mismatch between two base images.
 *
 * Only the two geo routes are touched; everything else keeps the portal's own
 * shape. Exits non-zero if either route no longer matches, so a base-image
 * update fails the build rather than leaving a half-applied patch.
 */
const fs = require("fs");
const path = require("path");

const ROOT = "/app/.next/server/app/api/master-data";
const HEADER =
  'request_header:{sender_app_mnemonic:"registry-staff-portal",' +
  'sender_app_url:"",request_id:String(Date.now()),' +
  'request_timestamp:new Date().toISOString()}';

// buildPayload:a=>({ <inner> })   ->   buildPayload:a=>({ header, request_body:{ <inner> } })
const PATTERN = /buildPayload:a=>\(\{(pagination_request:\{[^}]*\},request_payload:\{[^}]*\})\}\)/g;

let patched = 0;
for (const dir of fs.readdirSync(ROOT)) {
  const file = path.join(ROOT, dir, "route.js");
  if (!fs.existsSync(file)) continue;
  const before = fs.readFileSync(file, "utf8");
  const after = before.replace(
    PATTERN,
    (_m, inner) => `buildPayload:a=>({${HEADER},request_body:{${inner}}})`
  );
  if (after !== before) {
    fs.writeFileSync(file, after);
    patched += 1;
    console.log("  wrapped " + dir + "/route.js");
  }
}

if (patched < 2) {
  console.error(
    `geo envelope patch wrapped ${patched} route(s), expected 2 ` +
      "(get-all-g2p-geo-levels and geo-level-values) — the base image changed"
  );
  process.exit(1);
}
console.log(`wrapped ${patched} master-data geo route(s) in the G2P envelope`);
