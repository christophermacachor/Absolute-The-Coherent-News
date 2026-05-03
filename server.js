require('dotenv').config();
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static('public')); // put your index.html inside /public folder

app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  try {
    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',   // This is V4
        messages: [{ role: 'user', content: message }],
        temperature: 0.7,
        max_tokens: 500
      })
    });
    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || 'No response';
    res.json({ reply });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
