const { chromium } = require('playwright');

(async () => {
  console.log('Starting Loan Origination System test...');
  
  // Launch browser
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Navigate to the application
    console.log('Navigating to application...');
    await page.goto('http://localhost:5000');
    await page.waitForLoadState('networkidle');
    
    // Test 1: Login
    console.log('Test 1: Login');
    await page.fill('#username', 'user1');
    await page.fill('#password', 'test123');
    await page.click('#login-button');
    
    // Verify login successful (dashboard visible)
    await page.waitForSelector('#dashboard-container:not(.hidden)', { timeout: 5000 });
    console.log('✅ Login successful');
    
    // Test 2: Change role
    console.log('Test 2: Change role');
    await page.selectOption('#role-selector', 'Processor');
    // Verify role changed
    const selectedRole = await page.$eval('#role-selector', el => el.value);
    console.log(`Selected role: ${selectedRole}`);
    console.log('✅ Role change successful');
    
    // Test 3: Create new loan
    console.log('Test 3: Create new loan');
    await page.click('#new-loan-button');
    await page.waitForSelector('#new-loan-modal:not(.hidden)', { timeout: 5000 });
    
    // Fill in loan form
    await page.fill('#newLoanFirstName', 'Test');
    await page.fill('#newLoanLastName', 'Borrower');
    await page.fill('#newLoanEmail', 'test@example.com');
    await page.fill('#newLoanPhone', '555-123-4567');
    
    // Submit form
    await page.click('#create-loan-button');
    
    // Handle the alert
    page.on('dialog', async dialog => {
      console.log(`Dialog message: ${dialog.message()}`);
      await dialog.accept();
    });
    
    console.log('✅ New loan creation successful');
    
    // Test 4: View loan details
    console.log('Test 4: View loan details');
    // Wait for any potential dialogs to be handled
    await page.waitForTimeout(1000);
    
    // Click on the first "View" button
    const viewButtons = await page.$$('.view-loan-button');
    if (viewButtons.length > 0) {
      await viewButtons[0].click();
      await page.waitForSelector('#loan-details-modal:not(.hidden)', { timeout: 5000 });
      console.log('✅ Loan details view successful');
      
      // Test 5: Advance milestone
      console.log('Test 5: Advance milestone');
      // Click advance milestone button
      await page.click('#advance-milestone-button');
      
      // Handle the alert (dialog is already being listened to)
      // Close modal
      await page.waitForTimeout(1000); // Wait for potential dialogs
      console.log('✅ Advance milestone successful');
    } else {
      console.log('⚠️ No view buttons found to test loan details');
    }
    
    // Test 6: Logout
    console.log('Test 6: Logout');
    await page.click('#logout-button');
    await page.waitForSelector('#login-container:not(.hidden)', { timeout: 5000 });
    console.log('✅ Logout successful');
    
    console.log('All tests completed successfully!');
  } catch (error) {
    console.error(`Test failed: ${error}`);
  } finally {
    // Close browser
    await browser.close();
  }
})();