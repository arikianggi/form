const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse request bodies
app.use(express.urlencoded({ extended: true }));

// Login route
app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/login.html');
});

// Dashboard route (protected)
app.get('/dashboard', (req, res) => {
    // Check if user is authenticated
    if (!req.isAuthenticated()) {
        res.redirect('/login');
    } else {
        res.sendFile(__dirname + '/dashboard.html');
    }
});

// Login form submission
app.post('/login', (req, res) => {
    // Validate username and password (dummy example)
    const { username, password } = req.body;
    if (username === 'admin' && password === 'password') {
        // Authenticate user and redirect to dashboard
        req.isAuthenticated = true;
        res.redirect('/dashboard');
    } else {
        // Redirect back to login page with error message
        res.redirect('/login?error=1');
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
