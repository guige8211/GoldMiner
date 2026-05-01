const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  let hasErrors = false;
  
  page.on('console', msg => {
      const text = msg.text();
      console.log('LOG:', text);
      if (text.includes('ERROR') || text.includes('Parse Error')) {
          hasErrors = true;
      }
  });
  
  page.on('pageerror', err => {
      console.log('PAGE ERROR:', err.message);
      hasErrors = true;
  });
  
  console.log("Navigating to game...");
  await page.goto('https://guige8211.github.io/GoldMiner/', { waitUntil: 'networkidle' });
  
  await page.waitForTimeout(15000); 
  
  await browser.close();
  
  if (hasErrors) {
      console.error("TEST FAILED: Godot threw script errors.");
      process.exit(1);
  } else {
      console.log("TEST PASSED: No script errors detected during runtime.");
      process.exit(0);
  }
})();
