const express = require('express');
const app = express();

app.get('/auth', (req, res) => {
    res.json({ message: "User authenticated" });
});

app.listen(4001, () => console.log("Auth service running on 4001"));