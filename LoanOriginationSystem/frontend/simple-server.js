const express = require('express');
const path = require('path');
const app = express();
const PORT = 5000;

// Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Simple route for testing
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Fallback route
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'static', 'index.html'));
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Simple server running on http://0.0.0.0:${PORT}`);
});