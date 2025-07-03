const express = require('express');
const multer = require('multer');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const app = express();
const upload = multer({ dest: 'uploads/' });
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

app.use(express.json());
app.use(express.static('public'));

// Text question endpoint
app.post('/api/ask', async (req, res) => {
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-pro" });
        const result = await model.generateContent(req.body.question);
        const response = await result.response;
        const text = response.text();
        res.json({ answer: text });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Error processing your question" });
    }
});

// File upload endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
    try {
        // Process file based on type (image or PDF)
        // This is simplified - actual implementation would need proper file processing
        const model = genAI.getGenerativeModel({ model: "gemini-pro-vision" });
        // You would need to properly format the file for the API
        const result = await model.generateContent(["Explain this image", req.file]);
        const response = await result.response;
        const text = response.text();
        res.json({ answer: text });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Error processing your file" });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
