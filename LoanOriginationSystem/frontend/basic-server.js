const express = require('express');
const path = require('path');
const proxy = require('express-http-proxy');
const os = require('os');

const app = express();
const PORT = 5000;

// Determine the hostname for the backend server
// This helps when running in environments where localhost may not work
const hostname = process.env.BACKEND_HOST || '127.0.0.1';
const BACKEND_URL = `http://${hostname}:8000`;

// Middleware to log all requests
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

// Middleware to parse JSON body for debugging
app.use(express.json());
app.use((req, res, next) => {
  if (req.method === 'POST' && req.body) {
    console.log('Request body:', JSON.stringify(req.body));
  }
  next();
});

// Proxy API requests to the backend
app.use('/api', (req, res, next) => {
  // Log the incoming request before proxying
  console.log(`Incoming request: ${req.method} ${req.url}`);
  
  // Add CORS headers for proxied requests
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');
  
  // Handle OPTIONS method
  if (req.method === 'OPTIONS') {
    return res.status(200).send();
  }
  
  next();
}, proxy(BACKEND_URL, {
  proxyReqPathResolver: function (req) {
    // Make sure the URL ends with a slash for proper Flask routing
    let urlPath = req.url;
    
    // Only add trailing slash for GET requests to avoid issues with file uploads
    if (req.method === 'GET') {
      urlPath = urlPath.endsWith('/') ? urlPath : `${urlPath}/`;
    }
    
    // Log the proxy destination
    const fullPath = `/api${urlPath}`;
    console.log(`Proxying request to: ${BACKEND_URL}${fullPath}`);
    return fullPath;
  },
  // Allow larger file uploads for documents
  limit: '20mb',
  // Increase timeout for slower operations
  timeout: 30000,
  // Add proper headers for file uploads
  proxyReqOptDecorator: function(proxyReqOpts, srcReq) {
    // For multipart form uploads, don't set content-type and let the browser set the boundary
    if (srcReq.headers['content-type'] && 
        srcReq.headers['content-type'].includes('multipart/form-data')) {
      proxyReqOpts.headers['content-type'] = srcReq.headers['content-type'];
    }
    return proxyReqOpts;
  },
  userResDecorator: function(proxyRes, proxyResData, userReq, userRes) {
    // Log the status code
    console.log(`Proxy response for ${userReq.method} ${userReq.url}: ${proxyRes.statusCode}`);
    
    // Copy response headers for downloads
    if (proxyRes.headers['content-disposition']) {
      userRes.setHeader('Content-Disposition', proxyRes.headers['content-disposition']);
    }
    
    return proxyResData;
  },
  proxyErrorHandler: function(err, res, next) {
    console.error('Proxy error occurred:', err.message);
    
    // Handle errors more gracefully with a user-friendly message
    let errorMessage = 'Connection to backend service failed';
    let statusCode = 502;
    
    // Different error message based on error type
    if (err.code === 'ECONNREFUSED') {
      errorMessage = 'The backend service is not available. Please check if it is running.';
    } else if (err.code === 'ETIMEDOUT') {
      errorMessage = 'The request timed out. The backend service might be overloaded.';
      statusCode = 504;
    }
    
    res.status(statusCode).json({ 
      error: errorMessage,
      details: err.message,
      // Include a suggestion
      suggestion: 'Please try again later or refresh the page.'
    });
  }
}));

// Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Default route to serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'static', 'index.html'));
});

// Calculator route
app.get('/calculator.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'static', 'calculator.html'));
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Basic server running on http://0.0.0.0:${PORT}`);
  console.log(`Proxying API requests to ${BACKEND_URL}`);
});