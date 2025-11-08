// playwright-tests/test-dashboard.spec.ts
import { test, expect } from '@playwright/test';

test('Dashboard loads sensor data', async ({ page }) => {
  await page.goto('https://demo.smart-hub.io/');
  await page.fill('#username', 'demo');
  await page.fill('#password', 'demo123');
  await page.click('button[type="submit"]');
  await expect(page.locator('.sensor-card')).toHaveCount(3);
});
