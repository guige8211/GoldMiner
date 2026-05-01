const { chromium } = require('playwright');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  console.log("Waiting 60s for deploy...");
  await sleep(60000);
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.route('**', route => route.continue());
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  await context.clearCookies();
  
  page.on('console', msg => {
      console.log('LOG:', msg.text());
  });
  
  await page.goto('https://guige8211.github.io/GoldMiner/?bust=' + new Date().getTime(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000); 
  await browser.close();
})();
