// At your project root folder
const express = require('express');
const app = express();

const API_KEY = process.env.DEEPSEEK_API_KEY || "sk-fallback"; // Get from system

app.post('/api/deepseek', async (req, res) => {
  // Use API_KEY safely here
});
