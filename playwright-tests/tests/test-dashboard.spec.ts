import { test, expect } from '@playwright/test';

test('Navigate QA Playground homepage to Top 10 Practice Sites', async ({ page }) => {
  // Step 1: Visit the homepage
  await page.goto('https://www.qaplayground.com/');

  // Step 2: Verify the homepage title
  await expect(page).toHaveTitle(/QA Playground/);

  // Step 3: Click the link to the practice page
  await page.click('a[href*="top-10-best-automation-practice-website"]');

  // Step 4: Verify navigation to the correct page
  await expect(page).toHaveURL(/top-10-best-automation-practice-website/);
  await expect(page.locator('h1')).toContainText('Top 10 Best Automation Practice Website');
});
