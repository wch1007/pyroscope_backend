// 在浏览器控制台中运行这个脚本来检查 Canvas 元素

console.log('=== Checking Canvas Elements ===');

// 1. 查找所有 canvas 元素
const allCanvases = document.querySelectorAll('canvas');
console.log(`Found ${allCanvases.length} canvas elements`);

allCanvases.forEach((canvas, idx) => {
  console.log(`\nCanvas ${idx}:`);
  console.log('  Size:', canvas.width, 'x', canvas.height);
  console.log('  Parent:', canvas.parentElement?.className);
  console.log('  Z-index:', window.getComputedStyle(canvas.parentElement || canvas).zIndex);
  console.log('  Opacity:', window.getComputedStyle(canvas.parentElement || canvas).opacity);
  console.log('  Display:', window.getComputedStyle(canvas.parentElement || canvas).display);
  console.log('  Visibility:', window.getComputedStyle(canvas.parentElement || canvas).visibility);
  
  // 检查 canvas 内容
  const ctx = canvas.getContext('2d');
  const imageData = ctx.getImageData(0, 0, Math.min(canvas.width, 10), Math.min(canvas.height, 10));
  const hasContent = Array.from(imageData.data).some(v => v !== 0);
  console.log('  Has content:', hasContent);
});

// 2. 查找 leaflet 相关的容器
console.log('\n=== Leaflet Panes ===');
const overlayPane = document.querySelector('.leaflet-overlay-pane');
if (overlayPane) {
  console.log('Overlay pane found');
  console.log('  Children:', overlayPane.children.length);
  console.log('  Z-index:', window.getComputedStyle(overlayPane).zIndex);
  
  // 列出所有子元素
  Array.from(overlayPane.children).forEach((child, idx) => {
    console.log(`  Child ${idx}:`, child.className, 'z-index:', window.getComputedStyle(child).zIndex);
  });
} else {
  console.log('Overlay pane NOT found');
}

// 3. 检查是否有热力图相关的元素
console.log('\n=== Heatmap Layer ===');
const gridLayers = document.querySelectorAll('.leaflet-layer');
console.log(`Found ${gridLayers.length} leaflet layers`);

gridLayers.forEach((layer, idx) => {
  const style = window.getComputedStyle(layer);
  console.log(`Layer ${idx}:`);
  console.log('  Class:', layer.className);
  console.log('  Z-index:', style.zIndex);
  console.log('  Opacity:', style.opacity);
  console.log('  Transform:', style.transform);
  console.log('  Has canvas children:', layer.querySelectorAll('canvas').length);
});

// 4. 保存一个测试 canvas 到全局变量以便进一步检查
if (allCanvases.length > 0) {
  window.__testCanvas = allCanvases[0];
  console.log('\n✓ First canvas saved to window.__testCanvas for inspection');
  
  // 尝试导出为 data URL 看看内容
  try {
    const dataUrl = window.__testCanvas.toDataURL();
    console.log('Canvas data URL (first 100 chars):', dataUrl.substring(0, 100));
  } catch (e) {
    console.log('Cannot export canvas:', e.message);
  }
}

console.log('\n=== Check Complete ===');
