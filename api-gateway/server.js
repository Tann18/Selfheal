const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());

app.get('/health', (req, res) => {
    res.json({ status: "ok" });
});

app.get('/products', async (req, res) => {
    try {
        const response = await axios.get('http://product-service:4002/products');
        res.json(response.data);
    } catch (err) {
        if (err.response && err.response.status === 503) {
            return res.status(503).json({ error: "Overloaded" });
        }
        res.status(500).json({ error: "Product service error" });
    }
});

app.get('/orders', async (req, res) => {
    try {
        const response = await axios.get('http://order-service:4003/orders');
        res.json(response.data);
    } catch (err) {
        res.status(500).json({ error: "Order service error" });
    }
});

app.listen(4000, () => console.log("API Gateway running on 4000"));