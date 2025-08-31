test.skip('Flaky test demo: MapBuddy homepage', async ({ page }) => {
  await page.goto('https://mapbuddy.onrender.com');
  const randomFail = Math.random() < 0.5;
  expect(randomFail).toBeFalsy();
  await expect(page).toHaveTitle(/MapBuddy/i);
});

