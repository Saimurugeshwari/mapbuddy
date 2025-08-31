//Test Mapbuddy e2e spec.js

const { test, expect } = require('@playwright/test');

test.skip('End to end Mapbuddy trip simulation', async ({ page }) => {
    //call backend API to start trip
    const apiContext = await page.request.newContext();
    const response = await apiContext.post('http://127.0.0.1:8000/start_trip',{
        data: {destination: "Hospital", purpose: "Doctor Appointment"}

    });
    expect(response.ok()).toBeTruthy();
    const json = await response.json();
    expect(json.message).toBe("Trip started");
    //open mapbuddy web map
    await page.goto('http://127.0.0.1:8000/map');

    //verify map container
    const mapFrame = page.locator('#map');
    await expect(mapFrame).toBeVisible();
    //verify trip purpose
    const tripRemainder = page.locator('text=Doctor Appointment');
    await expect(tripRemainder).toBeVisible();

});