// Renders promo.html to promo.mp4 (1280x720, 30fps). Usage: node render.js
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.join(__dirname, 'promo.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const fps = 30, dur = await page.evaluate(() => window.DURATION);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart',
    path.join(__dirname, 'promo.mp4')], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let f = 0; f < fps * dur; f++) {
    await page.evaluate(t => window.render(t), f / fps);
    ff.stdin.write(await page.screenshot({ type: 'jpeg', quality: 92 }));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  for (const [t, n] of [[2.4, 'still-intro'], [11, 'still-services'], [15.5, 'still-cta']]) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: path.join(__dirname, n + '.png') });
  }
  await browser.close();
})();
