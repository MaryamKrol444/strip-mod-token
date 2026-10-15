/* Browser QA dependencies are development-only; no browser assets ship to readers. */
import chromium from '@sparticuz/chromium';
import { chromium as playwright } from 'playwright-core';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import zlib from 'node:zlib';
import { execFileSync } from 'node:child_process';
// The npm Chromium bundle includes NSS/NSPR for minimal Linux containers.
const libs = `${process.cwd()}/.cache/chromium-libs`;
fs.mkdirSync(libs, {recursive:true});
if (!fs.existsSync(`${libs}/lib/libnspr4.so`)) {
  const packed = fs.readFileSync('node_modules/@sparticuz/chromium/bin/al2023.tar.br');
  execFileSync('tar', ['xf', '-', '-C', libs], {input:zlib.brotliDecompressSync(packed)});
}
process.env.LD_LIBRARY_PATH = `${libs}/lib:${process.env.LD_LIBRARY_PATH || ''}`;
const base = process.env.PREVIEW_URL || 'http://127.0.0.1:3000';
const browser = await playwright.launch({executablePath: await chromium.executablePath(),args:chromium.args.filter(arg=>arg!=='--single-process' && arg!=='--disable-web-security'),headless:true});
const routes=['/','/stripchat-token-generator/','/stripchat-live/','/strip-chat-sites/','/about/','/contact/','/privacy-policy/','/terms/','/disclaimer/'];
const errors=[];fs.mkdirSync('.cache/qa',{recursive:true});
for (const width of [1440,390]) {
  const context=await browser.newContext({viewport:{width,height:1000}});
  const page=await context.newPage();
  const connections=[];
  page.on('request',r=>{if(!r.url().startsWith(base))connections.push(r.url());});
  for(const route of routes){
    const response=await page.goto(base+route,{waitUntil:'networkidle'});
    if(response.status()!==200)errors.push(`${width} ${route} HTTP ${response.status()}`);
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    if(overflow)errors.push(`${width} ${route} horizontal overflow`);
    const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    for(const v of audit.violations)errors.push(`${width} ${route}: ${v.id} ${v.nodes.map(n=>n.target.join(' ')).join(', ')}`);
    if(connections.length)errors.push(`${width} ${route} unexpected third-party request ${connections.join(', ')}`);
    await page.keyboard.press('Tab');
    const focused=await page.evaluate(()=>document.activeElement?.textContent);
    if(focused!=='Skip to content')errors.push(`${width} ${route} first focus is not skip link`);
    await page.keyboard.press('Enter');
    if(await page.evaluate(()=>location.hash)!=='#main')errors.push(`${width} ${route} skip link does not work`);
    if(route==='/'){
      await page.goto(base+route,{waitUntil:'networkidle'});
      await page.screenshot({path:`.cache/qa/home-${width}.png`,fullPage:false});
    }
    console.log(`Checked ${width}px ${route}`);
  }
  // Local anchor, image sizing, and opt-in video behavior.
  await page.goto(base+'/stripchat-token-generator/',{waitUntil:'networkidle'});
  const firstAnchor=page.locator('.toc a').first();
  const target=await firstAnchor.getAttribute('href');await firstAnchor.click();
  if(await page.evaluate(()=>location.hash)!==target)errors.push('TOC anchor did not navigate');
  const images=page.locator('article img');
  for(let i=0;i<await images.count();i++){
    await images.nth(i).scrollIntoViewIfNeeded();
    await images.nth(i).evaluate(img=>img.decode());
  }
  // Intercept the external player so QA never contacts YouTube.
  let videoRequests=0;
  await page.route('https://www.youtube-nocookie.com/**',async route=>{
    videoRequests++;
    await route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>Player intercepted for QA</title>'});
  });
  const playerResponse=page.waitForResponse(r=>r.url().startsWith('https://www.youtube-nocookie.com/'),{timeout:10000});
  await page.locator('.video-load').click();
  await page.waitForSelector('.video-slot iframe');
  await playerResponse;
  if(!videoRequests)errors.push('Video opt-in did not create the player request');
  if(await page.locator('.video-load').count())errors.push('Video load button remains after playback choice');
  await context.close();
}
const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
const page=await context.newPage();await page.goto(base);
if(await page.locator('h2').count()<10)errors.push('No-JS content missing');
if(await page.locator('noscript a').count()!==1)errors.push('No-JS video fallback missing');
await page.locator('.toc a').first().click();
if(!(await page.evaluate(()=>location.hash)))errors.push('No-JS TOC failed');
const secret=await page.request.get(base+'/.git/config');if(secret.status()!==404)errors.push('Server exposes repository metadata');
await context.close();await browser.close();
if(errors.length){console.error(errors.join('\n'));process.exit(1)}
console.log('PASS: 18 responsive page checks, WCAG A/AA axe scans, keyboard skip links, TOC, images, no pre-consent third-party requests, opt-in video, no-JS content and private-file denial.');
