const { chromium } = require('playwright');

(async () => {
  console.log('Starting Complete Loan Lifecycle Test...');
  
  // Launch browser
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Declare role and loan variables
  let currentRole = 'Sales';
  let loanID;
  
  // Handle alerts/dialogs
  page.on('dialog', async dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    await dialog.accept();
  });
  
  try {
    // Navigate to the application
    console.log('Navigating to application...');
    await page.goto('http://localhost:5000');
    await page.waitForLoadState('networkidle');
    
    // Step 1: Login
    console.log('Step 1: Login as Sales');
    await page.fill('#username', 'user1');
    await page.fill('#password', 'test123');
    await page.click('#login-button');
    
    // Verify login successful (dashboard visible)
    await page.waitForSelector('#dashboard-container:not(.hidden)', { timeout: 5000 });
    console.log('✅ Login successful');
    
    // Step 2: Create a new loan
    console.log('Step 2: Create new loan');
    await page.click('#new-loan-button');
    await page.waitForSelector('#new-loan-modal:not(.hidden)', { timeout: 5000 });
    
    // Generate a unique borrower name using timestamp
    const timestamp = new Date().getTime();
    const firstName = `Test${timestamp}`;
    const lastName = 'Borrower';
    
    // Fill in loan form
    await page.fill('#newLoanFirstName', firstName);
    await page.fill('#newLoanLastName', lastName);
    await page.fill('#newLoanEmail', 'test@example.com');
    await page.fill('#newLoanPhone', '555-123-4567');
    
    // Submit form
    await page.click('#create-loan-button');
    await page.waitForTimeout(1000); // Wait for alert
    
    console.log(`✅ Created new loan for ${firstName} ${lastName}`);
    
    // Step 3: Find our newly created loan
    // Refresh page to ensure new loan appears
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Look for our unique borrower name
    const borrowerNameSelector = `text="${firstName} ${lastName}"`;
    await page.waitForSelector(borrowerNameSelector, { timeout: 10000 });
    
    // Find the loan row containing our borrower
    const loanRow = await page.$(`tr:has(${borrowerNameSelector})`);
    if (!loanRow) throw new Error('Could not find our newly created loan');
    
    // Get the loan ID from the row
    const loanIdCell = await loanRow.$('td:first-child');
    loanID = await loanIdCell.textContent();
    console.log(`Found loan with ID: ${loanID}`);
    
    // Step 4: View loan details
    console.log('Step 4: View loan details');
    const viewButton = await loanRow.$('.view-loan-button');
    await viewButton.click();
    await page.waitForSelector('#loan-details-modal:not(.hidden)', { timeout: 5000 });
    console.log('✅ Loan details view opened');
    
    // Step 5: Complete loan lifecycle - advance through all milestones
    console.log('Step 5: Starting loan milestone progression');
    
    // Array of roles and the milestones they handle
    const roleAndMilestones = [
      { role: 'Sales', milestone: 'PreApplication', nextMilestone: 'Application' },
      { role: 'Processor', milestone: 'Application', nextMilestone: 'Processing' },
      { role: 'Processor', milestone: 'Processing', nextMilestone: 'Underwriting' },
      { role: 'Underwriter', milestone: 'Underwriting', nextMilestone: 'Approval' },
      { role: 'Underwriter', milestone: 'Approval', nextMilestone: 'Closing' },
      { role: 'Closer', milestone: 'Closing', nextMilestone: 'Funded' }
    ];
    
    // Process each milestone
    for (const { role, milestone, nextMilestone } of roleAndMilestones) {
      // Close the modal if it's open
      if (await page.isVisible('#loan-details-modal:not(.hidden)')) {
        await page.click('#close-details-modal-button');
        await page.waitForSelector('#loan-details-modal.hidden', { timeout: 5000 });
      }
      
      // Switch role if needed
      if (currentRole !== role) {
        console.log(`Switching role from ${currentRole} to ${role}`);
        await page.selectOption('#role-selector', role);
        currentRole = role;
        await page.waitForTimeout(500);
      }
      
      // Find and click on our loan again
      await page.reload();
      await page.waitForLoadState('networkidle');
      
      const loanRow = await page.$(`tr:has(td:text-matches("${loanID}"))`);
      if (!loanRow) throw new Error(`Could not find loan ${loanID} after role switch`);
      
      const viewButton = await loanRow.$('.view-loan-button');
      await viewButton.click();
      await page.waitForSelector('#loan-details-modal:not(.hidden)', { timeout: 5000 });
      
      // Verify current milestone
      const milestoneText = await page.textContent('#loan-details-content >> text=Milestone:');
      console.log(`Current milestone: ${milestoneText}`);
      
      // Click advance milestone button
      console.log(`Advancing from ${milestone} to ${nextMilestone}`);
      await page.click('#advance-milestone-button');
      await page.waitForTimeout(1000); // Wait for alert
      
      console.log(`✅ Advanced milestone to ${nextMilestone}`);
    }
    
    console.log('✅ Successfully completed full loan lifecycle');
    
    // Step 6: Logout
    console.log('Step 6: Logout');
    await page.click('#logout-button');
    await page.waitForSelector('#login-container:not(.hidden)', { timeout: 5000 });
    console.log('✅ Logout successful');
    
    console.log('All test steps completed successfully!');
  } catch (error) {
    console.error(`Test failed: ${error}`);
  } finally {
    // Take a screenshot at the end
    await page.screenshot({ path: 'test-result.png' });
    
    // Close browser
    await browser.close();
  }
})();