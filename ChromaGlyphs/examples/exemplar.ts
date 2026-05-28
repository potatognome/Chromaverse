#!/usr/bin/env ts-node
/**
 * examples/exemplar.ts – ChromaGlyphs exemplar mock entry point.
 *
 * Run with:  npx ts-node examples/exemplar.ts
 *
 * Exercises the full public API across normal and adversarial scenarios.
 */

import { generateGlyph, encode, decode, validate, renderSVG, ChromaGlyphError } from '../src/index';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function log(key: string, msg: string): void {
  const icons: Record<string, string> = {
    '!info': 'ℹ️ ',
    '!proc': '⚙️ ',
    '!done': '✅',
    '!warn': '⚠️ ',
    '!error': '❌',
    '!data': '📊',
    '!test': '🧪',
    '!pass': '✔️ ',
    '!fail': '✖️ ',
  };
  const icon = icons[key] ?? '  ';
  console.log(`${icon} [${key}] ${msg}`);
}

function section(title: string): void {
  console.log();
  console.log('─'.repeat(60));
  console.log(`  ${title}`);
  console.log('─'.repeat(60));
}

// ---------------------------------------------------------------------------
// Demo sections
// ---------------------------------------------------------------------------

function demoGenerate(): void {
  section('1. generateGlyph – normal cases');

  const g1 = generateGlyph(['#FF6B6B', '#4ECDC4', '#45B7D1'], {
    author: 'ChromaTutor',
    tags: ['warm', 'cool'],
  });
  log('!done', `Generated glyph id=${g1.meta.id} palette=${g1.palette.length} colours`);

  const g2 = generateGlyph(['#000000']);
  log('!done', `Single-colour glyph id=${g2.meta.id}`);

  const large = Array.from({ length: 16 }, (_, i) =>
    `#${i.toString(16).padStart(2, '0').repeat(3)}`,
  );
  const g3 = generateGlyph(large);
  log('!done', `Max-size glyph (16 colours) id=${g3.meta.id}`);
}

function demoEncodeDecode(): void {
  section('2. encode → decode round-trip');

  const glyph = generateGlyph(['#FF6B6B', '#4ECDC4'], { author: 'exemplar', tags: ['test'] });
  const token = encode(glyph);
  log('!data', `Token: ${token.slice(0, 60)}…`);

  const decoded = decode(token);
  const match =
    decoded.meta.id === glyph.meta.id &&
    decoded.palette.length === glyph.palette.length &&
    decoded.palette.every((e, i) => e.hex === glyph.palette[i].hex);
  log(match ? '!pass' : '!fail', `Round-trip ${match ? 'PASSED' : 'FAILED'}`);
}

function demoValidation(): void {
  section('3. validate');

  const good = generateGlyph(['#AABBCC', '#112233']);
  const r1 = validate(good);
  log(r1.valid ? '!pass' : '!fail', `Valid glyph: ${r1.valid}`);

  const bad = generateGlyph(['#AABBCC']);
  (bad.palette[0] as { hex: string }).hex = 'notahex';
  const r2 = validate(bad);
  log(r2.valid ? '!fail' : '!pass', `Invalid hex detected: errors=${r2.errors.join('; ')}`);
}

function demoRendering(): void {
  section('4. renderSVG');

  const glyph = generateGlyph(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']);
  const svgRow = renderSVG(glyph, { layout: 'row', showLabels: true });
  log('!data', `Row SVG length: ${svgRow.length} chars`);
  log('!info', `Row SVG starts: ${svgRow.slice(0, 80).replace(/\n/g, ' ')}…`);

  const svgGrid = renderSVG(glyph, { layout: 'grid', gridColumns: 2 });
  log('!data', `Grid SVG length: ${svgGrid.length} chars`);
}

function demoEdgeCases(): void {
  section('5. Edge cases and adversarial inputs');

  // Empty palette
  try {
    generateGlyph([]);
    log('!fail', 'Expected error for empty palette – none thrown');
  } catch (e) {
    log('!pass', `Empty palette rejected: ${(e as ChromaGlyphError).message}`);
  }

  // Oversized palette
  try {
    generateGlyph(Array.from({ length: 17 }, () => '#AABBCC'));
    log('!fail', 'Expected error for 17-colour palette – none thrown');
  } catch (e) {
    log('!pass', `Oversized palette rejected: ${(e as ChromaGlyphError).message}`);
  }

  // Invalid hex
  try {
    generateGlyph(['notahex']);
    log('!fail', 'Expected error for invalid hex – none thrown');
  } catch (e) {
    log('!pass', `Invalid hex rejected: ${(e as ChromaGlyphError).message}`);
  }

  // Malformed token
  try {
    decode('GARBAGE_TOKEN' as import('../src/types').GlyphToken);
    log('!fail', 'Expected error for garbage token – none thrown');
  } catch (e) {
    log('!pass', `Malformed token rejected: ${(e as ChromaGlyphError).message}`);
  }

  // Unsupported format version
  try {
    const badPayload = Buffer.from(
      JSON.stringify({ v: 'cg99', id: 'x', ts: new Date().toISOString(), p: [{ h: '#000' }] }),
    ).toString('base64url');
    decode(`CG1:${badPayload}` as import('../src/types').GlyphToken);
    log('!fail', 'Expected error for unsupported version – none thrown');
  } catch (e) {
    log('!pass', `Unsupported version rejected: ${(e as ChromaGlyphError).message}`);
  }
}

// ---------------------------------------------------------------------------
// Menu
// ---------------------------------------------------------------------------

function printMenu(): void {
  console.log();
  log('!info', '1. Generate glyphs');
  log('!info', '2. Encode / Decode round-trip');
  log('!info', '3. Validation');
  log('!info', '4. SVG Rendering');
  log('!info', '5. Edge cases');
  log('!info', '6. Run all');
  log('!info', '0. Exit');
}

async function main(): Promise<number> {
  console.log('═'.repeat(60));
  console.log('  ChromaGlyphs Exemplar');
  console.log('═'.repeat(60));

  // In non-interactive mode (e.g. CI), run all demos automatically.
  const isInteractive = process.stdin.isTTY;

  if (!isInteractive) {
    log('!proc', 'Non-interactive mode – running all demos');
    demoGenerate();
    demoEncodeDecode();
    demoValidation();
    demoRendering();
    demoEdgeCases();
    log('!done', 'All demos complete.');
    return 0;
  }

  const readline = await import('readline');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  const prompt = (): Promise<string> =>
    new Promise((resolve) => {
      printMenu();
      rl.question('Select option (0-6): ', (ans) => resolve(ans.trim()));
    });

  let running = true;
  while (running) {
    const choice = await prompt();
    switch (choice) {
      case '1':
        demoGenerate();
        break;
      case '2':
        demoEncodeDecode();
        break;
      case '3':
        demoValidation();
        break;
      case '4':
        demoRendering();
        break;
      case '5':
        demoEdgeCases();
        break;
      case '6':
        demoGenerate();
        demoEncodeDecode();
        demoValidation();
        demoRendering();
        demoEdgeCases();
        break;
      case '0':
        log('!done', 'Exiting exemplar.');
        running = false;
        break;
      default:
        log('!error', `Unknown option: "${choice}"`);
    }
  }

  rl.close();
  return 0;
}

main().then(process.exit).catch((err) => {
  console.error(err);
  process.exit(1);
});
