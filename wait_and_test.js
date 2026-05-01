const { chromium } = require('playwright');
const { execSync } = require('child_process');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  console.log("Waiting 60 seconds for GitHub Actions to deploy...");
  await sleep(60000);
  
  console.log("Checking logs to see if bug is gone...");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Clear cache
  await page.route('**', route => route.continue());
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  await context.clearCookies();
  
  let hasErrors = false;
  page.on('console', msg => {
      const text = msg.text();
      if (text.includes('ERROR') || text.includes('Parse Error')) {
          console.log('LOG:', text);
          hasErrors = true;
      }
  });
  
  await page.goto('https://guige8211.github.io/GoldMiner/?bust=' + new Date().getTime(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(15000); 
  
  await page.screenshot({ path: 'game_screenshot_final2.png', fullPage: true });
  await browser.close();
  
  if (hasErrors) {
      console.log("STILL HAS SCRIPT ERRORS");
  } else {
      console.log("NO SCRIPT ERRORS DETECTED!");
      // Let's run our color test
      execSync("node test_ui_final.js");
  }
})();
