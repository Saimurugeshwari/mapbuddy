// tests/mapbuddy.test.js
const { test, expect } = require('@playwright/test');

test('Homepage loads with map visible', async ({ page }) => {
  await page.goto('https://mapbuddy.onrender.com');

  // Check title
  await expect(page).toHaveTitle(/MapBuddy/i);

  // Check map container
  await expect(page.locator('#map')).toBeVisible();
});
