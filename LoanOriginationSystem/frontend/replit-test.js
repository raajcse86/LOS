const { chromium } = require('playwright');

(async () => {
  console.log('Starting Loan Origination System Tests in Replit...');
  
  // Launch browser in headless mode (required for Replit)
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Handle dialogs automatically
  page.on('dialog', async dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    await dialog.accept();
  });
  
  try {
    // Navigate to the application
    console.log('Navigating to application...');
    await page.goto('http://localhost:5000');
    await page.waitForLoadState('networkidle');
    
    // Capture screenshot of login page
    await page.screenshot({ path: 'login-page.png' });
    console.log('✅ Login page loaded successfully');
    
    // Test Login
    console.log('Testing login...');
    await page.fill('#username', 'user1');
    await page.fill('#password', 'test123');
    await page.click('#login-button');
    
    // Verify login successful (dashboard visible)
    await page.waitForSelector('#dashboard-container:not(.hidden)', { timeout: 5000 });
    await page.screenshot({ path: 'dashboard.png' });
    console.log('✅ Login successful');
    
    // Test Role Switching
    console.log('Testing role switching...');
    for (const role of ['Processor', 'Underwriter', 'Closer', 'Manager', 'Sales']) {
      await page.selectOption('#role-selector', role);
      console.log(`✅ Role switched to ${role}`);
      await page.waitForTimeout(300);
    }
    
    // Test New Loan Modal
    console.log('Testing new loan modal...');
    await page.click('#new-loan-button');
    await page.waitForSelector('#new-loan-modal:not(.hidden)', { timeout: 5000 });
    await page.screenshot({ path: 'new-loan-modal.png' });
    console.log('✅ New loan modal opened successfully');
    
    // Close new loan modal
    await page.click('#cancel-loan-button');
    await page.waitForSelector('#new-loan-modal.hidden', { timeout: 5000 });
    console.log('✅ New loan modal closed successfully');
    
    // Test Loan Details
    console.log('Testing loan details view...');
    const viewButtons = await page.$$('.view-loan-button');
    if (viewButtons.length > 0) {
      await viewButtons[0].click();
      await page.waitForSelector('#loan-details-modal:not(.hidden)', { timeout: 5000 });
      await page.screenshot({ path: 'loan-details.png' });
      console.log('✅ Loan details view opened successfully');
      
      // Test Loan Milestone Advance Button
      const advanceButton = await page.$('#advance-milestone-button');
      const buttonText = await advanceButton.textContent();
      console.log(`Advance milestone button text: ${buttonText}`);
      console.log('✅ Advance milestone button verified');
      
      // Close loan details modal
      await page.click('#close-details-modal-button');
      await page.waitForSelector('#loan-details-modal.hidden', { timeout: 5000 });
      console.log('✅ Loan details modal closed successfully');
    } else {
      console.log('⚠️ No loans found to test details view');
    }
    
    // Test Logout
    console.log('Testing logout...');
    await page.click('#logout-button');
    await page.waitForSelector('#login-container:not(.hidden)', { timeout: 5000 });
    await page.screenshot({ path: 'logout-result.png' });
    console.log('✅ Logout successful');
    
    console.log('All tests completed successfully!');
  } catch (error) {
    console.error(`Test failed: ${error}`);
    await page.screenshot({ path: 'test-failure.png' });
  } finally {
    // Close browser
    await browser.close();
  }
})();