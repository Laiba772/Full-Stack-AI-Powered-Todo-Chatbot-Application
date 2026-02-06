// frontend/e2e/chat.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Chat E2E Tests', () => {
  // Assuming a login page is at /signin and a chat page at /chat
  const chatPageUrl = '/chat';
  const signInPageUrl = '/signin';

  // Helper to log in a user for tests
  async function login(page) {
    await page.goto(signInPageUrl);
    await page.fill('input[name="email"]', 'test@example.com'); // Replace with actual test user credentials
    await page.fill('input[name="password"]', 'password'); // Replace with actual test user credentials
    await page.click('button[type="submit"]');
    await page.waitForURL(chatPageUrl); // Wait until redirected to chat page
    await expect(page).toHaveURL(chatPageUrl);
  }

  test('should allow a logged-in user to send a message and receive a response', async ({ page }) => {
    await login(page);
    await page.goto(chatPageUrl);

    const chatInput = page.getByPlaceholder('Type your message...');
    await expect(chatInput).toBeVisible();

    await chatInput.fill('Hello AI, how are you?');
    await chatInput.press('Enter');

    // Expect user message to appear
    await expect(page.locator('span', { hasText: 'Hello AI, how are you?' })).toBeVisible();

    // Expect AI response to appear (this assumes a distinct AI response text)
    // This will depend on the mocked/actual backend response from previous steps
    await expect(page.locator('span', { hasText: 'AI Echo: Hello AI, how are you?' })).toBeVisible();
  });

  test('should resume conversation on page reload', async ({ page }) => {
    await login(page);
    await page.goto(chatPageUrl);

    // Send an initial message
    const chatInput = page.getByPlaceholder('Type your message...');
    await chatInput.fill('First message');
    await chatInput.press('Enter');
    await expect(page.locator('span', { hasText: 'AI Echo: First message' })).toBeVisible();

    // Reload the page
    await page.reload();
    await page.waitForURL(chatPageUrl);

    // Expect previous messages to be visible
    await expect(page.locator('span', { hasText: 'First message' })).toBeVisible();
    await expect(page.locator('span', { hasText: 'AI Echo: First message' })).toBeVisible();

    // Send another message to confirm active conversation
    await chatInput.fill('Second message');
    await chatInput.press('Enter');
    await expect(page.locator('span', { hasText: 'AI Echo: Second message' })).toBeVisible();
  });

  test('should display access denied on non-allowlisted domain', async ({ browser }) => {
    // Manually set up a context to mock a different domain
    const context = await browser.newContext({
      baseURL: 'http://non-allowed-domain.com', // Replace with a domain not in your NEXT_PUBLIC_CHAT_DOMAIN_KEY
    });
    const page = await context.newPage();

    // Need to mock the environment variable for this test to correctly simulate
    // For local testing, you might need to run playwright with specific env vars
    // For this E2E test, we'll assume the frontend build already has the env var setup.
    // The actual domain check happens in layout.tsx.
    
    // We cannot directly mock process.env in Playwright's browser context without complex setup.
    // This test primarily checks the UI output if the check *fails*.
    // A more robust E2E test would involve deploying to actual domains.

    await page.goto(chatPageUrl);
    await expect(page.getByText('Access Denied: This chat is not available on this domain.')).toBeVisible();
  });
});
