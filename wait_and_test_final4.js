const { chromium } = require('playwright');
const { execSync } = require('child_process');

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
  
  page.on('console', msg => {
      console.log('LOG:', msg.text());
  });
  
  await page.goto('https://guige8211.github.io/GoldMiner/?bust=' + new Date().getTime(), { waitUntil: 'networkidle' });
  await page.waitForTimeout(15000); 
  
  await page.screenshot({ path: 'game_screenshot_final7.png', fullPage: true });
  await browser.close();
  
  const testCode = `
const fs = require('fs');
const { PNG } = require('pngjs');
fs.createReadStream('game_screenshot_final7.png')
  .pipe(new PNG({ filterType: 4 }))
  .on('parsed', function() {
    let yellow = 0;
    for (let y = 80; y < this.height; y++) {
        for (let x = 0; x < this.width; x++) {
            let idx = (this.width * y + x) << 2;
            let r = this.data[idx];
            let g = this.data[idx+1];
            let b = this.data[idx+2];
            if (r > 200 && g > 150 && b < 50) yellow++;
        }
    }
    console.log('Yellow Pixels:', yellow);
  });
      `;
  fs.writeFileSync('temp_test4.js', testCode);
  execSync('node temp_test4.js', {stdio: 'inherit'});
})();
