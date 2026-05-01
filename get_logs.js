const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Capture all console logs from Godot
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER ERROR:', err.message));
  
  console.log("Navigating to game URL...");
  await page.goto('https://guige8211.github.io/GoldMiner/', { waitUntil: 'networkidle' });
  
  await page.waitForTimeout(10000); 
  await browser.close();
})();
