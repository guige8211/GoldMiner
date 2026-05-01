const fs = require('fs');
const { PNG } = require('pngjs');
fs.createReadStream('game_screenshot_final4.png')
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
