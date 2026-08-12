const { chromium } = require('playwright');

(async () => {
  const query = process.argv[2] || '"Bảng giá đất" "38 triệu" "Phù Đổng"';
  console.log(`Bắt đầu chạy trình duyệt ảo để tra cứu: ${query}...`);
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();
  
  try {
    // Navigate to Google
    await page.goto('https://www.google.com/search?q=' + encodeURIComponent(query), { waitUntil: 'networkidle' });
    
    // Wait a bit to ensure elements are loaded
    await page.waitForTimeout(2000);
    
    // Take full page screenshot
    const screenshotPath = 'result.png';
    await page.screenshot({ path: screenshotPath, fullPage: true });
    
    console.log(`Đã chụp ảnh màn hình thành công tại: ${screenshotPath}`);
    
    // Attempt to extract text from the search results
    const results = await page.evaluate(() => {
      const snippets = Array.from(document.querySelectorAll('.g, .VwiC3b, .hgKElc')).map(el => el.innerText);
      return snippets.join('\n\n--- \n\n');
    });
    
    console.log('\n--- KẾT QUẢ TEXT TRÍCH XUẤT TỪ GOOGLE ---\n');
    console.log(results);
    
  } catch (err) {
    console.error('Lỗi khi cào dữ liệu:', err);
  } finally {
    await browser.close();
  }
})();
