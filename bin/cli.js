#!/usr/bin/env node

import { existsSync, cpSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const pkgRoot = resolve(__dirname, '..');

const args = process.argv.slice(2);
const isGlobal = args.includes('-g') || args.includes('--global');
const isHelp = args.includes('-h') || args.includes('--help');

if (isHelp) {
  console.log(`
GO-FRONT CLI

Использование:
  npx @gocharly/go-front          Установить скилл в текущий проект (.agents/skills/go-front)
  npx @gocharly/go-front -g       Установить скилл глобально для AI-ассистентов (~/.agents/skills/go-front)
  npx @gocharly/go-front --help   Показать справку
`);
  process.exit(0);
}

const targetBase = isGlobal 
  ? join(homedir(), '.agents', 'skills', 'go-front')
  : join(process.cwd(), '.agents', 'skills', 'go-front');

console.log(`[go-front] Установка скилла в: ${targetBase}...`);

try {
  mkdirSync(targetBase, { recursive: true });

  const itemsToCopy = ['SKILL.md', 'README.md', 'references', 'scripts', 'updates'];

  for (const item of itemsToCopy) {
    const src = join(pkgRoot, item);
    const dest = join(targetBase, item);

    if (existsSync(src)) {
      cpSync(src, dest, { recursive: true, force: true });
    }
  }

  console.log(`[go-front] Скилл успешно установлен в ${targetBase}`);
  console.log(`[go-front] Теперь ваши AI-агенты (Antigravity, Claude Code, Cursor) будут использовать стандарт GO-FRONT.`);
} catch (error) {
  console.error(`[go-front] Ошибка при установке:`, error.message);
  process.exit(1);
}
