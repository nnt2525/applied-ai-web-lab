import { readFile, readdir, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const root = fileURLToPath(new URL('../', import.meta.url));
const web = path.join(root, 'web');
async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  return (await Promise.all(entries.map(entry => entry.isDirectory() ? walk(path.join(directory, entry.name)) : path.join(directory, entry.name)))).flat();
}
let checked = 0;
for (const file of await walk(web)) {
  if (file.endsWith('.html')) {
    const html = await readFile(file, 'utf8');
    for (const match of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
      const target = match[1];
      if (/^(https?:|#|data:|mailto:)/.test(target)) continue;
      await stat(path.resolve(path.dirname(file), target.split('#')[0]));
    }
    if (!html.includes('name="viewport"') || !html.includes('<title>')) throw new Error(`${file} is missing page metadata`);
    checked++;
  }
  if (file.endsWith('.js')) {
    const check = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
    if (check.status !== 0) throw new Error(check.stderr);
    checked++;
  }
  if (file.endsWith('.json')) { JSON.parse(await readFile(file, 'utf8')); checked++; }
}
console.log(`Checked ${checked} HTML, JavaScript, and JSON files. Local asset links resolve.`);
