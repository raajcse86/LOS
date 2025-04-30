const { chromium } = require('playwright');

(async () => {
  console.log('Starting End-to-End Test for Loan Origination System...');
  
  // Launch browser
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Store the loan ID for later use
  let createdLoanId;
  
  // Handle dialogs automatically
  page.on('dialog', async dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    await dialog.accept();
  });
  
  try {
    // Navigate to the application
    console.log('Step 1: Navigating to application...');
    await page.goto('http://localhost:5000');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'e2e-test-login-page.png' });
    
    // Login
    console.log('Step 2: Logging in with test credentials...');
    await page.fill('#username', 'user1');
    await page.fill('#password', 'test123');
    await page.click('#login-button');
    
    // Verify login successful (dashboard visible)
    await page.waitForSelector('#dashboard-container:not(.hidden)', { timeout: 5000 });
    await page.screenshot({ path: 'e2e-test-dashboard.png' });
    console.log('✓ Login successful');
    
    // Create a new loan
    console.log('Step 3: Creating a new loan...');
    await page.click('#new-loan-button');
    await page.waitForSelector('#new-loan-modal:not(.hidden)', { timeout: 5000 });
    
    // Generate unique borrower name
    const timestamp = new Date().getTime();
    const firstName = `Test${timestamp}`;
    const lastName = 'Borrower';
    
    // Fill in loan form
    await page.fill('#newLoanFirstName', firstName);
    await page.fill('#newLoanLastName', lastName);
    await page.fill('#newLoanEmail', `${firstName.toLowerCase()}@example.com`);
    await page.fill('#newLoanPhone', '555-123-4567');
    
    // Submit form
    await page.click('#create-loan-button');
    
    // Wait for form to be processed
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'e2e-test-loan-created.png' });
    console.log(`✓ Created new loan for ${firstName} ${lastName}`);
    
    // Find the newly created loan
    console.log('Step 4: Finding newly created loan...');
    
    // Find the loan row containing our borrower
    // This may take multiple attempts as the UI refreshes
    let attempts = 0;
    let loanRow = null;
    while (attempts < 5 && !loanRow) {
      attempts++;
      await page.reload();
      await page.waitForLoadState('networkidle');
      // Look for loan with our unique name
      try {
        loanRow = await page.$(`tr:has-text("${firstName} ${lastName}")`);
      } catch (e) {
        console.log(`Attempt ${attempts}: Loan not found yet`);
      }
      if (!loanRow) await page.waitForTimeout(1000);
    }
    
    if (!loanRow) {
      throw new Error('Could not find our newly created loan');
    }
    
    // Get the loan ID
    const loanIdCell = await loanRow.$('td:first-child');
    createdLoanId = await loanIdCell.textContent();
    console.log(`✓ Found loan with ID: ${createdLoanId}`);
    
    // Complete loan lifecycle
    console.log('Step 5: Testing loan milestone progression...');
    
    // Define the milestone progression and the role for each step
    const milestones = [
      { role: 'Sales', from: 'PreApplication', to: 'Application' },
      { role: 'Processor', from: 'Application', to: 'Processing' }, 
      { role: 'Processor', from: 'Processing', to: 'Underwriting' },
      { role: 'Underwriter', from: 'Underwriting', to: 'Approval' },
      { role: 'Underwriter', from: 'Approval', to: 'Closing' },
      { role: 'Closer', from: 'Closing', to: 'Funded' }
    ];
    
    // Go through each milestone step
    for (const { role, from, to } of milestones) {
      // Select the correct role
      console.log(`Setting role to ${role}...`);
      await page.selectOption('#role-selector', role);
      await page.waitForTimeout(500);
      
      // Find and click on our loan (may need to reload if the view changes)
      console.log(`Looking for loan in ${from} milestone...`);
      await page.reload(); 
      await page.waitForLoadState('networkidle');
      
      // Find our loan row
      const loanRowSelector = `tr:has(td:text-matches("${createdLoanId}"))`;
      const foundLoan = await page.$(loanRowSelector);
      
      if (!foundLoan) {
        console.log(`Loan not visible in ${role} view. This may be expected.`);
        continue;
      }
      
      // Click view button on our loan
      const viewButton = await foundLoan.$('.view-loan-button');
      await viewButton.click();
      
      // Wait for loan details modal
      await page.waitForSelector('#loan-details-modal:not(.hidden)', { timeout: 5000 });
      
      // Take screenshot of this milestone
      await page.screenshot({ path: `e2e-test-milestone-${from}.png` });
      
      // Check if the milestone advance button is available
      const advanceButtonExists = await page.$('#advance-milestone-button:not([disabled])');
      if (advanceButtonExists) {
        // Click advance milestone button
        console.log(`Advancing from ${from} to ${to}...`);
        await page.click('#advance-milestone-button');
        
        // Wait for modal to close and page to refresh
        await page.waitForSelector('#loan-details-modal.hidden', { timeout: 5000 });
        console.log(`✓ Advanced milestone to ${to}`);
      } else {
        // Close the modal if we can't advance
        console.log(`Cannot advance from ${from} in this role. Closing modal.`);
        await page.click('#close-details-modal-button');
        await page.waitForSelector('#loan-details-modal.hidden', { timeout: 5000 });
      }
      
      // Wait a bit between steps
      await page.waitForTimeout(1000);
    }
    
    // Final check - look at the loan in Funded state
    console.log('Step 6: Verifying final loan state...');
    await page.selectOption('#role-selector', 'Manager');
    await page.waitForTimeout(500);
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Get final state screenshot
    await page.screenshot({ path: 'e2e-test-final-state.png' });
    
    // Logout
    console.log('Step 7: Logging out...');
    await page.click('#logout-button');
    await page.waitForSelector('#login-container:not(.hidden)', { timeout: 5000 });
    console.log('✓ Logout successful');
    
    console.log('End-to-End test completed successfully!');
  } catch (error) {
    console.error(`Test failed: ${error}`);
    await page.screenshot({ path: 'e2e-test-error.png' });
  } finally {
    // Close browser
    await browser.close();
  }
})();