
function random_color() {
    // Generate random RGB values from 0 to 255
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return r + ',' + g + ',' + b;
}
