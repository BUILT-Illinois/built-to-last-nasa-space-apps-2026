// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const { execFileSync } = require('node:child_process');
const { existsSync, readFileSync, readdirSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const root = join(__dirname, '../..');
const dataRoot = join(root, 'app/public/data');
const version = process.env.GITHUB_SHA ??
  execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
if (!/^[a-f0-9]{40}$/.test(version)) throw new Error('Expected a full Git SHA for API health');

const regions = [];
for (const entry of readdirSync(dataRoot, { withFileTypes: true }).sort((a, b) =>
  a.name.localeCompare(b.name))) {
  if (!entry.isDirectory()) continue;
  const id = entry.name;
  const dir = join(dataRoot, id);
  const manifestPath = join(dir, 'manifest.json');
  if (!existsSync(manifestPath)) continue; // Only advertise published regions.
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const landmarks = JSON.parse(readFileSync(join(dir, 'landmarks.json'), 'utf8'));
  if (manifest.region?.id !== id || landmarks.regionId !== id) {
    throw new Error(`Region IDs in ${dir} must match the directory name`);
  }
  regions.push({ manifest, landmarks });
}

writeFileSync(join(root, 'api/dist/bundle.json'), JSON.stringify({ version, regions }));
