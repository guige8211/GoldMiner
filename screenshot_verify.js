const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log("Navigating to game URL...");
  await page.goto('https://guige8211.github.io/GoldMiner/', { waitUntil: 'networkidle' });
  
  console.log("Waiting for 10 seconds to ensure everything loads and spawns...");
  await page.waitForTimeout(10000); 
  
  console.log("Taking full page screenshot...");
  await page.screenshot({ path: 'game_screenshot_final.png', fullPage: true });
  
  await browser.close();
})();
