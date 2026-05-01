const fs = require('fs');
const { PNG } = require('pngjs');

fs.createReadStream('game_screenshot_3.png')
  .pipe(new PNG({ filterType: 4 }))
  .on('parsed', function() {
    let yellowPixels = 0; 
    let darkGrayPixels = 0; 
    
    // UI Panel takes top 80 pixels out of 720
    for (let y = 80; y < this.height; y++) {
        for (let x = 0; x < this.width; x++) {
            let idx = (this.width * y + x) << 2;
            let r = this.data[idx];
            let g = this.data[idx+1];
            let b = this.data[idx+2];
            
            // Bright Yellow
            if (r > 200 && g > 150 && b < 50) yellowPixels++;
            // Dark Gray
            if (Math.abs(r - 105) < 15 && Math.abs(g - 105) < 15 && Math.abs(b - 105) < 15) darkGrayPixels++;
        }
    }
    
    console.log(`Analyzing GAMEPLAY AREA ONLY (y > 80):`);
    console.log(`Yellow Pixels: ${yellowPixels}`);
    console.log(`Dark Gray Pixels: ${darkGrayPixels}`);
  });
