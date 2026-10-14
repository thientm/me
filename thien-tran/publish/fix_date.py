import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.connect_over_cdp('http://127.0.0.1:9444')
    ctx = b.contexts[0]
    p = [x for x in ctx.pages if 'studio.youtube.com' in x.url][0]
    
    print('1. Opening Scheduled popup...')
    row0 = p.locator('ytcp-video-row').first
    row0.locator('text=Scheduled').first.click()
    p.wait_for_timeout(2000)
    
    print('2. Clicking datepicker trigger...')
    trigger = p.locator('#datepicker-trigger').first
    trigger.click()
    p.wait_for_timeout(2000)
    
    print('3. Clicking day 14...')
    p.locator('ytcp-date-picker').get_by_text('14', exact=True).first.click()
    p.wait_for_timeout(1500)
    
    print('4. Reading trigger text...')
    print('Trigger text:', repr(trigger.inner_text()))
    
    print('5. Clicking Schedule/Save...')
    sch_btn = p.locator('ytcp-button#save-button, button:has-text("Schedule")').last
    print('Button text:', sch_btn.inner_text())
    sch_btn.click()
    p.wait_for_timeout(6000)
    
    p.reload(wait_until='domcontentloaded')
    p.wait_for_timeout(6000)
    row0 = p.locator('ytcp-video-row').first
    print('FINAL Row 0 text:', repr(row0.inner_text().replace('\n', ' | ')))
