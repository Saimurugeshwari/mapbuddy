// Playwright flaky test simulation

const { test, expect } = require('@playwright/test');

test('Simulate flaky element appearance', async ({ page }) => {
  await page.goto('https://example.com/flaky');
  // Randomly delay the appearance of the element
  const delay = Math.random() > 0.5 ? 1000 : 3000;
  await page.waitForTimeout(delay);
  const element = page.locator('#sometimes-there');
  // Simulate intermittent failure
  if (delay > 2000) {
    await expect(element).toHaveText('Hello!');
  } else {
    await expect(element).not.toHaveText('Hello!');
  }
});