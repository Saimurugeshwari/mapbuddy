// Playwright login flow test

const { test, expect } = require('@playwright/test');

test('User can log in with valid credentials', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  await page.click('#login-button');
  await expect(page.locator('#welcome-message')).toHaveText(/Welcome/i);
});