const { chromium } = require('playwright');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  console.log("Waiting 60 seconds for GitHub Actions to deploy...");
  await sleep(60000);
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.route('**', route => route.continue());
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  await context.clearCookies();
  
  let hasErrors = false;
  page.on('console', msg => {
      const text = msg.text();
      console.log('LOG:', text);
      if (text.includes('ERROR') && !text.includes('icon.svg')) {
          hasErrors = true;
      }
  });
  
  await page.goto('https://guige8211.github.io/GoldMiner/?bust=' + new Date().getTime(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000); // Wait for load
  
  console.log("Pressing K to trigger GM Collect...");
  await page.keyboard.press('k');
  await page.waitForTimeout(2000);
  
  if (hasErrors) {
      console.log("STILL HAS SCRIPT ERRORS WHEN PRESSING K");
  } else {
      console.log("GM TOOL TRIGGERED SUCCESSFULLY, NO ERRORS!");
  }
  
  await browser.close();
})();
