const express = require('express');
const app = express();

app.get('/orders', (req, res) => {
  res.json([
    { id: 1, item: "Laptop" },
    { id: 2, item: "Phone" }
  ]);
});

app.listen(4003, () => console.log("Order service running on 4003"));