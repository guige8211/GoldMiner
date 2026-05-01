const fs = require('fs');
const { PNG } = require('pngjs');

fs.createReadStream('game_screenshot_final.png')
  .pipe(new PNG({ filterType: 4 }))
  .on('parsed', function() {
    let yellowPixels = 0; // Look for bright yellow items specifically below the UI panel
    let darkGrayPixels = 0; // Look for rocks
    let cyanPixels = 0; // Look for diamonds
    let whitePixels = 0; // UI Text
    
    // UI Panel takes top 80 pixels out of 720
    for (let y = 80; y < this.height; y++) {
        for (let x = 0; x < this.width; x++) {
            let idx = (this.width * y + x) << 2;
            let r = this.data[idx];
            let g = this.data[idx+1];
            let b = this.data[idx+2];
            
            // Bright Yellow (Gold Items modulate = Color(1, 0.84, 0)) -> (255, 214, 0)
            if (r > 200 && g > 150 && b < 50) yellowPixels++;
            // Dark Gray (Rocks modulate = Color(0.41, 0.41, 0.41)) -> (105, 105, 105)
            if (Math.abs(r - 105) < 15 && Math.abs(g - 105) < 15 && Math.abs(b - 105) < 15) darkGrayPixels++;
            // Cyan (Diamonds modulate = Color(0, 0.86, 1)) -> (0, 221, 255)
            if (r < 50 && g > 200 && b > 230) cyanPixels++;
            
            if (r > 240 && g > 240 && b > 240) whitePixels++;
        }
    }
    
    console.log(`Analyzing GAMEPLAY AREA ONLY (y > 80):`);
    console.log(`Yellow Pixels (Gold items): ${yellowPixels}`);
    console.log(`Dark Gray Pixels (Rocks): ${darkGrayPixels}`);
    console.log(`Cyan Pixels (Diamonds): ${cyanPixels}`);
  });
