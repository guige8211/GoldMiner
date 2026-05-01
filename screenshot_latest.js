const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Clear cache and bypass service workers
  await page.route('**', route => route.continue());
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  await context.clearCookies();
  
  console.log("Navigating to game URL with cache bust...");
  await page.goto('https://guige8211.github.io/GoldMiner/?bust=' + new Date().getTime(), { waitUntil: 'networkidle' });
  
  console.log("Waiting for 10 seconds to ensure everything loads and spawns...");
  await page.waitForTimeout(10000); 
  
  console.log("Taking full page screenshot...");
  await page.screenshot({ path: 'game_screenshot_latest.png', fullPage: true });
  
  await browser.close();
})();
